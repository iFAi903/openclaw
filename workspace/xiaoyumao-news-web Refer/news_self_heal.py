#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


TIMEZONE = ZoneInfo('Asia/Taipei')
PROJECT_DIR = Path(__file__).resolve().parent
LOG_DIR = PROJECT_DIR / 'logs'
STATUS_DIR = PROJECT_DIR / 'status'
ALERT_DIR = STATUS_DIR / 'alerts'
BACKUP_BASE_DIR = PROJECT_DIR / 'backups'
SITE_STATUS_TS = PROJECT_DIR / 'src' / 'data' / 'siteRuntimeStatus.ts'
LAST_STATUS_FILE = STATUS_DIR / 'last_run_status.json'
STATUS_ALIAS_FILE = STATUS_DIR / 'news-status.json'
RUN_HISTORY_FILE = STATUS_DIR / 'run_history.jsonl'
LAST_ALERT_FILE = ALERT_DIR / 'last_alert.json'
ALERT_HISTORY_FILE = ALERT_DIR / 'alert_history.jsonl'
LOCK_FILE = STATUS_DIR / 'self_heal.lock.json'
RUNTIME_LOG_FILE = Path('/tmp/xiaoyumao-news-cron.log')
PIPELINE_SCRIPT = PROJECT_DIR / 'run-news-pipeline.sh'
UPDATE_TS_SCRIPT = PROJECT_DIR / 'update_news_ts.py'
DAILY_DATA_FILE = PROJECT_DIR / 'daily_data.json'
PRODUCTION_URL = 'https://xiaoyumao-news-web.vercel.app'
VERCEL_DEPLOY_TIMEOUT_SECONDS = 180
RETRY_DELAY_SECONDS = 5
MAX_FULL_ATTEMPTS = 2
LOCK_STALE_SECONDS = 4 * 60 * 60


class ExitCode:
    FULL_SUCCESS = 0
    DEGRADED_SUCCESS = 11
    FAILED = 20
    SKIPPED = 30


@dataclass
class StepFailure(Exception):
    step: str
    message: str

    def __str__(self) -> str:
        return f'{self.step}: {self.message}'


def now() -> datetime:
    return datetime.now(TIMEZONE)


def now_iso() -> str:
    return now().isoformat()


def mkdirs() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    STATUS_DIR.mkdir(parents=True, exist_ok=True)
    ALERT_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_BASE_DIR.mkdir(parents=True, exist_ok=True)
    SITE_STATUS_TS.parent.mkdir(parents=True, exist_ok=True)


def json_dump(data: Any, path: Path) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def jsonl_append(data: Any, path: Path) -> None:
    with path.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(data, ensure_ascii=False) + '\n')


class Orchestrator:
    def __init__(self) -> None:
        mkdirs()
        self.started_at = now_iso()
        self.persistent_log = LOG_DIR / f'cron-{now().strftime("%Y-%m-%d")}.log'
        self.status: dict[str, Any] = {
            'status': 'running',
            'runMode': 'full',
            'step': 'init',
            'message': '初始化自我兜底编排器',
            'startedAt': self.started_at,
            'endedAt': '',
            'attempt': 0,
            'maxAttempts': MAX_FULL_ATTEMPTS,
            'retryTriggered': False,
            'degraded': False,
            'alertRaised': False,
            'alertCount': 0,
            'failureSummary': '',
            'failureHistory': [],
            'generatedDate': '',
            'onlineDate': '',
            'contentDate': '',
            'newsCount': 0,
            'productsCount': 0,
            'buildOk': False,
            'deployOk': False,
            'verifyOk': False,
            'backupPath': '',
            'backupTsPath': '',
            'deployUrl': '',
            'productionUrl': PRODUCTION_URL,
            'persistentLog': str(self.persistent_log),
            'statusFile': str(LAST_STATUS_FILE),
            'alertFile': str(LAST_ALERT_FILE),
            'historyFile': str(RUN_HISTORY_FILE),
            'lockFile': str(LOCK_FILE),
            'lastSuccessfulRunAt': '',
            'lastSuccessfulContentDate': '',
            'siteStatus': 'unknown',
        }
        self.vercel_token = os.environ.get('VERCEL_TOKEN', '').strip()
        self.backup_dir: Path | None = None
        self.lock_acquired = False

    def log(self, message: str, level: str = 'INFO') -> None:
        prefix = {'INFO': '', 'SUCCESS': '✅ ', 'ERROR': '❌ ', 'WARN': '⚠️ '}.get(level, '')
        line = f'[{now().strftime("%Y-%m-%d %H:%M:%S")}] {prefix}{message}'
        print(line)
        with RUNTIME_LOG_FILE.open('a', encoding='utf-8') as fh:
            fh.write(line + '\n')
        with self.persistent_log.open('a', encoding='utf-8') as fh:
            fh.write(line + '\n')

    def redact_command(self, command: list[str]) -> str:
        redacted: list[str] = []
        skip_next = False
        for index, item in enumerate(command):
            if skip_next:
                skip_next = False
                continue
            if item == '--token' and index + 1 < len(command):
                redacted.extend(['--token', '***REDACTED***'])
                skip_next = True
                continue
            if self.vercel_token and self.vercel_token in item:
                redacted.append(item.replace(self.vercel_token, '***REDACTED***'))
                continue
            redacted.append(item)
        return ' '.join(redacted)

    def write_status(self) -> None:
        payload = dict(self.status)
        payload['endedAt'] = now_iso()
        json_dump(payload, LAST_STATUS_FILE)
        json_dump(payload, STATUS_ALIAS_FILE)

    def append_history(self) -> None:
        jsonl_append(dict(self.status, endedAt=now_iso()), RUN_HISTORY_FILE)

    def acquire_lock(self) -> bool:
        if LOCK_FILE.exists():
            try:
                data = json.loads(LOCK_FILE.read_text(encoding='utf-8'))
            except Exception:
                data = {}
            pid = int(data.get('pid', 0) or 0)
            acquired_at = data.get('acquiredAt', '')
            ts = 0.0
            if acquired_at:
                try:
                    ts = datetime.fromisoformat(acquired_at).timestamp()
                except Exception:
                    ts = 0.0
            alive = False
            if pid > 0:
                try:
                    os.kill(pid, 0)
                    alive = True
                except OSError:
                    alive = False
            if alive and (time.time() - ts) < LOCK_STALE_SECONDS:
                self.status.update({
                    'status': 'skipped_locked',
                    'step': 'lock',
                    'message': f'检测到已有实例运行中（pid={pid}），本次跳过',
                    'siteStatus': 'unknown',
                })
                self.write_status()
                self.append_history()
                self.log(self.status['message'], 'WARN')
                return False
            self.log('发现陈旧锁，已自动清理', 'WARN')
            LOCK_FILE.unlink(missing_ok=True)

        lock_data = {
            'pid': os.getpid(),
            'hostname': socket.gethostname(),
            'acquiredAt': now_iso(),
        }
        json_dump(lock_data, LOCK_FILE)
        self.lock_acquired = True
        return True

    def release_lock(self) -> None:
        if self.lock_acquired:
            LOCK_FILE.unlink(missing_ok=True)
            self.lock_acquired = False

    def update_site_runtime_status(
        self,
        *,
        run_status: str,
        degraded: bool,
        status_label: str,
        content_date: str,
        failure_summary: str = '',
    ) -> None:
        payload = {
            'runStatus': run_status,
            'degraded': degraded,
            'statusLabel': status_label,
            'contentDate': content_date,
            'statusUpdatedAt': now_iso(),
            'failureSummary': failure_summary,
            'lastSuccessfulRunAt': self.status.get('lastSuccessfulRunAt', ''),
            'lastSuccessfulContentDate': self.status.get('lastSuccessfulContentDate', ''),
        }
        content = f"""// 自动生成 - 站点运行状态\n\nexport type SiteRunStatus = 'unknown' | 'full_success' | 'degraded_success' | 'failed';\n\nexport interface SiteRuntimeStatusPayload {{\n  runStatus: SiteRunStatus;\n  degraded: boolean;\n  statusLabel: string;\n  contentDate: string;\n  statusUpdatedAt: string;\n  failureSummary: string;\n  lastSuccessfulRunAt?: string;\n  lastSuccessfulContentDate?: string;\n}}\n\nexport const siteRuntimeStatus: SiteRuntimeStatusPayload = {json.dumps(payload, ensure_ascii=False, indent=2)};\n\nexport default siteRuntimeStatus;\n"""
        SITE_STATUS_TS.write_text(content, encoding='utf-8')

    def run_command(self, command: list[str], *, step: str, env: dict[str, str] | None = None, cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
        self.log(f'执行命令[{step}]: {self.redact_command(command)}')
        with self.persistent_log.open('a', encoding='utf-8') as log_fh:
            log_fh.write(f"\n--- {step} @ {now_iso()} ---\n")
        if capture:
            result = subprocess.run(
                command,
                cwd=str(cwd or PROJECT_DIR),
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            with self.persistent_log.open('a', encoding='utf-8') as log_fh:
                if result.stdout:
                    log_fh.write(result.stdout)
                if result.stderr:
                    log_fh.write(result.stderr)
            with RUNTIME_LOG_FILE.open('a', encoding='utf-8') as log_fh:
                if result.stdout:
                    log_fh.write(result.stdout)
                if result.stderr:
                    log_fh.write(result.stderr)
            return result
        with self.persistent_log.open('a', encoding='utf-8') as log_fh, RUNTIME_LOG_FILE.open('a', encoding='utf-8') as runtime_fh:
            proc = subprocess.run(
                command,
                cwd=str(cwd or PROJECT_DIR),
                env=env,
                text=True,
                stdout=log_fh,
                stderr=subprocess.STDOUT,
                check=False,
            )
            runtime_fh.write(f'[{now().strftime("%Y-%m-%d %H:%M:%S")}] {step} exit={proc.returncode}\n')
            return proc

    def create_backup(self) -> None:
        self.backup_dir = BACKUP_BASE_DIR / now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        copied_daily_data = ''
        if DAILY_DATA_FILE.exists():
            shutil.copy2(DAILY_DATA_FILE, self.backup_dir / 'daily_data.json')
            copied_daily_data = str(self.backup_dir / 'daily_data.json')
        news_ts = PROJECT_DIR / 'src' / 'data' / 'news.ts'
        if news_ts.exists():
            shutil.copy2(news_ts, self.backup_dir / 'news.ts')
        if SITE_STATUS_TS.exists():
            shutil.copy2(SITE_STATUS_TS, self.backup_dir / 'siteRuntimeStatus.ts')
        self.status['backupPath'] = copied_daily_data
        self.status['backupTsPath'] = str(self.backup_dir / 'news.ts')
        self.log(f'已创建备份目录：{self.backup_dir}', 'SUCCESS')

    def read_daily_data_summary(self) -> tuple[str, int, int]:
        data = json.loads(DAILY_DATA_FILE.read_text(encoding='utf-8'))
        date_text = data.get('date', '')
        news_count = len(data.get('news', []))
        products_count = len(data.get('products', []))
        return date_text, news_count, products_count

    def format_content_date(self, raw_date: str) -> str:
        if raw_date and '周' in raw_date:
            return raw_date
        if not raw_date:
            raw_date = now().strftime('%Y年%m月%d日')
        try:
            dt = datetime.strptime(raw_date, '%Y年%m月%d日').replace(tzinfo=TIMEZONE)
            weekday = '一二三四五六日'[dt.weekday()]
            return f'{raw_date} 周{weekday}'
        except Exception:
            return raw_date

    def record_failure(self, *, attempt: int, stage: str, message: str, retryable: bool) -> None:
        failure = {
            'attempt': attempt,
            'stage': stage,
            'message': message,
            'retryable': retryable,
            'at': now_iso(),
        }
        self.status['failureHistory'].append(failure)
        self.status['failureSummary'] = f'[{stage}] {message}'
        self.status['message'] = self.status['failureSummary']
        self.status['step'] = stage

    def emit_alert(self, *, severity: str, stage: str, message: str, attempt: int) -> None:
        alert = {
            'severity': severity,
            'stage': stage,
            'message': message,
            'attempt': attempt,
            'at': now_iso(),
            'persistentLog': str(self.persistent_log),
            'statusFile': str(LAST_STATUS_FILE),
            'productionUrl': PRODUCTION_URL,
        }
        json_dump(alert, LAST_ALERT_FILE)
        jsonl_append(alert, ALERT_HISTORY_FILE)
        self.status['alertRaised'] = True
        self.status['alertCount'] = int(self.status.get('alertCount', 0)) + 1
        self.log(f'已写入告警产物：{stage} / {message}', 'ERROR')

    def restore_backup_for_degraded(self) -> str:
        candidates = []
        if self.backup_dir is not None:
            candidates.append(self.backup_dir / 'daily_data.json')
        candidates.extend(sorted(BACKUP_BASE_DIR.glob('*/daily_data.json'), reverse=True))

        for candidate in candidates:
            if not candidate.exists():
                continue
            try:
                data = json.loads(candidate.read_text(encoding='utf-8'))
            except Exception:
                continue
            news = data.get('news', [])
            products = data.get('products', [])
            if len(news) >= 10 and len(products) >= 3:
                shutil.copy2(candidate, DAILY_DATA_FILE)
                result = self.run_command(['python3', str(UPDATE_TS_SCRIPT)], step='degraded-restore-news-ts')
                if result.returncode != 0:
                    raise StepFailure('degraded', '恢复备份后 news.ts 重建失败')
                return data.get('date', '')
        raise StepFailure('degraded', '没有找到可用的最近成功数据用于降级发布')

    def verify_production_site(self, *, expected_status: str, expected_content_date: str) -> str:
        deadline = time.time() + VERCEL_DEPLOY_TIMEOUT_SECONDS
        while time.time() < deadline:
            result = subprocess.run(
                ['curl', '-fsSL', '--max-time', '30', PRODUCTION_URL],
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode != 0:
                time.sleep(5)
                continue
            html = result.stdout

            status_match = re.search(r'data-run-status="([^"]+)"', html)
            date_match = re.search(r'data-content-date="([^"]+)"', html)
            online_status = status_match.group(1) if status_match else ''
            online_date = date_match.group(1) if date_match else ''
            if online_status == expected_status and online_date == expected_content_date:
                return online_date
            time.sleep(5)

        raise StepFailure(
            'verify',
            f'主域名验收未达标，期望 status={expected_status} / date={expected_content_date}'
        )

    def build_and_deploy(self, *, site_status: str, content_date: str, failure_summary: str = '') -> str:
        self.status['step'] = 'build'
        self.status['message'] = '构建项目'
        self.write_status()
        self.update_site_runtime_status(
            run_status=site_status,
            degraded=(site_status == 'degraded_success'),
            status_label='降级兜底已上线' if site_status == 'degraded_success' else '完整成功',
            content_date=content_date,
            failure_summary=failure_summary,
        )
        build_result = self.run_command(['npm', 'run', 'build'], step='build')
        if build_result.returncode != 0:
            raise StepFailure('build', '构建失败')
        self.status['buildOk'] = True
        self.log('构建完成', 'SUCCESS')

        self.status['step'] = 'deploy'
        self.status['message'] = '部署到 Vercel'
        self.write_status()
        deploy_result = self.run_command(
            ['npx', 'vercel', '--prod', '--token', self.vercel_token, '--yes'],
            step='deploy',
            capture=True,
        )
        if deploy_result.returncode != 0:
            raise StepFailure('deploy', '部署失败')
        deploy_output = (deploy_result.stdout or '') + '\n' + (deploy_result.stderr or '')
        deploy_url_match = re.search(r'https://[^\s]+vercel\.app', deploy_output)
        self.status['deployUrl'] = deploy_url_match.group(0) if deploy_url_match else ''
        self.status['deployOk'] = True
        self.log(f'部署完成：{self.status["deployUrl"] or "未解析到 deployment url"}', 'SUCCESS')

        self.status['step'] = 'verify'
        self.status['message'] = '主域名验收'
        self.write_status()
        online_date = self.verify_production_site(expected_status=site_status, expected_content_date=content_date)
        self.status['onlineDate'] = online_date
        self.status['verifyOk'] = True
        self.log(f'主域名验收通过：{online_date} / {site_status}', 'SUCCESS')
        return online_date

    def run_full_attempt(self, attempt: int) -> None:
        self.status['attempt'] = attempt
        self.status['runMode'] = 'full'
        self.status['step'] = 'pipeline'
        self.status['message'] = f'执行完整流程（attempt {attempt}/{MAX_FULL_ATTEMPTS}）'
        self.write_status()
        pipeline_result = self.run_command(['bash', str(PIPELINE_SCRIPT)], step=f'pipeline-attempt-{attempt}')
        if pipeline_result.returncode != 0:
            raise StepFailure('pipeline', f'新闻内容生成流水线失败（attempt {attempt}）')

        raw_date, news_count, products_count = self.read_daily_data_summary()
        content_date = self.format_content_date(raw_date)
        self.status['generatedDate'] = raw_date
        self.status['contentDate'] = content_date
        self.status['newsCount'] = news_count
        self.status['productsCount'] = products_count
        self.log(f'内容生成完成：{content_date} / {news_count} 条新闻 / {products_count} 个产品', 'SUCCESS')

        online_date = self.build_and_deploy(site_status='full_success', content_date=content_date)
        self.status.update({
            'status': 'full_success',
            'runMode': 'full',
            'degraded': False,
            'message': '完整流程成功，并通过主域名验收',
            'step': 'done',
            'siteStatus': 'full_success',
            'onlineDate': online_date,
            'lastSuccessfulRunAt': now_iso(),
            'lastSuccessfulContentDate': content_date,
        })

    def run_degraded_publish(self) -> None:
        self.status['runMode'] = 'degraded'
        self.status['degraded'] = True
        self.status['step'] = 'degraded_prepare'
        self.status['message'] = '启动降级兜底发布'
        self.write_status()
        content_date = self.format_content_date(self.restore_backup_for_degraded())
        self.status['contentDate'] = content_date
        self.status['message'] = f'降级数据已恢复：{content_date}'
        self.write_status()

        online_date = self.build_and_deploy(
            site_status='degraded_success',
            content_date=content_date,
            failure_summary=self.status.get('failureSummary', ''),
        )
        self.status.update({
            'status': 'degraded_success',
            'runMode': 'degraded',
            'degraded': True,
            'message': '完整流程失败，已用最近成功数据完成降级兜底发布并通过主域名验收',
            'step': 'done',
            'siteStatus': 'degraded_success',
            'onlineDate': online_date,
        })

    def finalize(self, exit_code: int) -> int:
        self.write_status()
        self.append_history()
        self.release_lock()
        return exit_code

    def run(self) -> int:
        self.log('========================================')
        self.log('开始执行每日新闻更新（自我兜底版）')
        self.log(f'持久日志: {self.persistent_log}')
        self.log(f'状态文件: {LAST_STATUS_FILE}')
        self.log('========================================')
        if not self.acquire_lock():
            return ExitCode.SKIPPED

        self.write_status()

        if not self.vercel_token:
            self.record_failure(attempt=0, stage='preflight', message='未设置 VERCEL_TOKEN 环境变量', retryable=False)
            self.emit_alert(severity='critical', stage='preflight', message=self.status['failureSummary'], attempt=0)
            self.status.update({'status': 'failed', 'siteStatus': 'failed'})
            return self.finalize(ExitCode.FAILED)

        self.create_backup()
        self.write_status()

        for attempt in range(1, MAX_FULL_ATTEMPTS + 1):
            try:
                self.run_full_attempt(attempt)
                return self.finalize(ExitCode.FULL_SUCCESS)
            except StepFailure as exc:
                retryable = attempt < MAX_FULL_ATTEMPTS
                self.record_failure(attempt=attempt, stage=exc.step, message=exc.message, retryable=retryable)
                self.emit_alert(
                    severity='critical' if attempt == 1 else 'high',
                    stage=exc.step,
                    message=exc.message,
                    attempt=attempt,
                )
                if retryable:
                    self.status.update({
                        'status': 'retrying',
                        'message': f'首次失败，{RETRY_DELAY_SECONDS} 秒后自动补跑一次',
                        'retryTriggered': True,
                        'step': 'retry_wait',
                    })
                    self.write_status()
                    self.log(self.status['message'], 'WARN')
                    time.sleep(RETRY_DELAY_SECONDS)
                    self.log('开始自动补跑', 'WARN')
                    continue
                self.log('完整流程两次均失败，转入降级兜底', 'WARN')

        try:
            self.run_degraded_publish()
            return self.finalize(ExitCode.DEGRADED_SUCCESS)
        except StepFailure as exc:
            self.record_failure(attempt=MAX_FULL_ATTEMPTS + 1, stage=exc.step, message=exc.message, retryable=False)
            self.emit_alert(severity='critical', stage=exc.step, message=exc.message, attempt=MAX_FULL_ATTEMPTS + 1)
            self.status.update({
                'status': 'failed',
                'runMode': 'degraded',
                'degraded': False,
                'message': '完整流程与降级兜底均失败',
                'step': exc.step,
                'siteStatus': 'failed',
            })
            return self.finalize(ExitCode.FAILED)


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def main() -> int:
    load_env_file(PROJECT_DIR / '.env.cron')
    orchestrator = Orchestrator()
    try:
        return orchestrator.run()
    except KeyboardInterrupt:
        orchestrator.record_failure(attempt=orchestrator.status.get('attempt', 0), stage='signal', message='任务被中断', retryable=False)
        orchestrator.emit_alert(severity='critical', stage='signal', message='任务被中断', attempt=orchestrator.status.get('attempt', 0))
        orchestrator.status.update({'status': 'failed', 'siteStatus': 'failed'})
        return orchestrator.finalize(ExitCode.FAILED)


if __name__ == '__main__':
    raise SystemExit(main())
