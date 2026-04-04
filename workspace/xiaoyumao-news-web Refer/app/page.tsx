import Link from 'next/link';
import { todayNews, NewsCard } from '@/src/data/news';
import { siteRuntimeStatus } from '@/src/data/siteRuntimeStatus';
import { ArrowUpRight, BadgeCheck, Boxes, Flame, Orbit, Radar, Sparkles } from 'lucide-react';

const cn = (...values: Array<string | false | null | undefined>) => values.filter(Boolean).join(' ');

function CardLink({ item, mode = 'news' }: { item: NewsCard; mode?: 'news' | 'product' }) {
  return (
    <Link
      href={item.url}
      target="_blank"
      className={cn(
        'group block rounded-[28px] border border-white/10 bg-[rgba(8,13,30,0.72)] backdrop-blur-xl',
        'transition duration-300 hover:-translate-y-0.5 hover:border-cyan-300/40 hover:shadow-[0_24px_80px_rgba(38,208,255,0.14)]'
      )}
    >
      <div className="flex h-full flex-col gap-4 p-6 md:p-7">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] text-white/45">
            <span className="inline-flex h-7 min-w-7 items-center justify-center rounded-full border border-white/10 bg-white/5 px-2 text-white/80">
              {item.rank}
            </span>
            <span>{mode === 'news' ? item.source : item.platform || item.source}</span>
          </div>
          <ArrowUpRight className="h-4 w-4 text-cyan-300/70 transition group-hover:text-cyan-200" />
        </div>

        <h3 className="text-lg font-semibold leading-7 text-white md:text-[21px] md:leading-8">
          {item.title}
        </h3>

        <p className="flex-1 text-sm leading-7 text-white/72 md:text-[15px]">
          {item.summary}
        </p>

        <div className="flex items-center justify-between gap-3 border-t border-white/8 pt-4 text-xs text-white/38">
          <span>{mode === 'news' ? item.source : `${item.platform} / ${item.source}`}</span>
          <span className="truncate text-right">{item.reason}</span>
        </div>
      </div>
    </Link>
  );
}

export default function Home() {
  const top = todayNews.aiNews[0];
  const lead = todayNews.aiNews.slice(1, 5);
  const grid = todayNews.aiNews.slice(5, 15);
  const isDegraded = siteRuntimeStatus.runStatus === 'degraded_success';
  const statusText = isDegraded
    ? `当前为降级交付：内容日期 ${siteRuntimeStatus.contentDate || todayNews.date}`
    : siteRuntimeStatus.runStatus === 'full_success'
      ? '当前为完整成功版本'
      : siteRuntimeStatus.statusLabel;

  return (
    <main className="min-h-screen bg-[#060816] text-white">
      <div className="feather-mesh pointer-events-none fixed inset-0 opacity-90" />
      <div className="pointer-events-none fixed inset-x-0 top-0 h-[280px] feather-glow" />

      <div className="relative mx-auto flex max-w-[1460px] flex-col gap-10 px-5 pb-16 pt-6 md:px-8 lg:px-10">
        <header className="rounded-[32px] border border-white/10 bg-[linear-gradient(135deg,rgba(14,20,44,0.94),rgba(7,10,25,0.82))] p-6 shadow-[0_40px_120px_rgba(0,0,0,0.35)] md:p-10">
          <div className="mb-8 flex flex-wrap items-center gap-3 text-[11px] uppercase tracking-[0.22em] text-white/55">
            <span className="inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-4 py-2 text-cyan-100/90">
              <Sparkles className="h-3.5 w-3.5" />
              XiaoYuMao AI Briefing
            </span>
            <span className="inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-2">{todayNews.date}</span>
            <span className="inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-2">
              {todayNews.aiNews.length} NEWS / {todayNews.products.length} PRODUCTS
            </span>
            <span
              className={cn(
                'inline-flex rounded-full border px-4 py-2',
                isDegraded
                  ? 'border-amber-300/30 bg-amber-300/10 text-amber-100'
                  : 'border-emerald-300/20 bg-emerald-300/10 text-emerald-100/90'
              )}
            >
              {siteRuntimeStatus.statusLabel}
            </span>
          </div>

          {isDegraded && (
            <div className="mb-8 rounded-[24px] border border-amber-300/25 bg-amber-300/10 px-5 py-4 text-sm leading-7 text-amber-50/92">
              <div className="font-semibold text-amber-100">降级兜底已生效</div>
              <div>{statusText}</div>
              {siteRuntimeStatus.failureSummary && (
                <div className="mt-2 text-amber-50/80">失败摘要：{siteRuntimeStatus.failureSummary}</div>
              )}
            </div>
          )}

          <div className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr] lg:items-end">
            <div className="space-y-6">
              <div className="space-y-4">
                <h1 className="max-w-4xl text-4xl font-semibold leading-tight tracking-[-0.04em] md:text-6xl md:leading-[1.02]">
                  小羽毛 <span className="feather-text">AI 新闻早报</span>
                </h1>
                <p className="max-w-3xl text-base leading-8 text-white/70 md:text-xl">
                  国际 AI 创新新闻每日定版。只留关键事件，不留空洞总结；只保留值得你花时间点开的那 20 条。
                </p>
              </div>

              <div className="grid gap-3 md:grid-cols-3">
                <div className="stat-panel">
                  <div className="stat-label">今日摘要</div>
                  <div className="stat-value">{todayNews.summary}</div>
                </div>
                <div className="stat-panel">
                  <div className="stat-label">验收门禁</div>
                  <div className="stat-value">
                    {todayNews.aiNews.length} 新闻 / {todayNews.products.length} 平台产品 / 近 3 天去重
                  </div>
                </div>
                <div className="stat-panel">
                  <div className="stat-label">每日寄语</div>
                  <div className="stat-value">{todayNews.quote.text}</div>
                </div>
              </div>
            </div>

            <div className="glass-grid rounded-[28px] border border-white/10 p-5 md:p-7">
              <div className="mb-5 flex items-center gap-3 text-sm text-white/80">
                <BadgeCheck className="h-4 w-4 text-cyan-300" />
                自动验收上线门禁
              </div>
              <div className="grid gap-3 text-sm text-white/65">
                {[
                  '标题必须是具体事件，不允许“新动态 / 新能力”',
                  '摘要必须补充标题之外的信息',
                  '产品平台严格一日五源各一条',
                  '当日与前三天双重去重',
                ].map((rule) => (
                  <div key={rule} className="inline-flex items-start gap-3 rounded-2xl border border-white/8 bg-white/5 px-4 py-3">
                    <span className="mt-1 h-2 w-2 rounded-full bg-gradient-to-r from-cyan-300 to-violet-400" />
                    <span>{rule}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </header>

        {top && (
          <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
            <Link
              href={top.url}
              target="_blank"
              className="group overflow-hidden rounded-[34px] border border-cyan-300/20 bg-[linear-gradient(135deg,rgba(17,28,58,0.98),rgba(8,12,30,0.92))] p-7 shadow-[0_28px_120px_rgba(20,120,255,0.18)] md:p-10"
            >
              <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-cyan-300/15 bg-cyan-300/10 px-4 py-2 text-xs uppercase tracking-[0.22em] text-cyan-100">
                <Flame className="h-4 w-4" />
                Lead Story
              </div>
              <h2 className="max-w-4xl text-3xl font-semibold leading-tight tracking-[-0.03em] text-white md:text-5xl md:leading-[1.06]">
                {top.title}
              </h2>
              <p className="mt-6 max-w-3xl text-base leading-8 text-white/72 md:text-lg">
                {top.summary}
              </p>
              <div className="mt-8 flex items-center justify-between gap-4 border-t border-white/10 pt-5 text-sm text-white/45">
                <span>{top.source}</span>
                <span className="inline-flex items-center gap-2 text-cyan-200/90">
                  查看原文 <ArrowUpRight className="h-4 w-4 transition group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
                </span>
              </div>
            </Link>

            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-1">
              {lead.map((item) => (
                <CardLink key={item.id} item={item} />
              ))}
            </div>
          </section>
        )}

        <section className="rounded-[32px] border border-white/10 bg-[rgba(7,11,28,0.78)] p-5 backdrop-blur-xl md:p-8">
          <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="mb-2 inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] text-white/45">
                <Radar className="h-3.5 w-3.5 text-cyan-300" />
                Global AI Signals
              </div>
              <h2 className="text-2xl font-semibold tracking-[-0.03em] text-white md:text-3xl">15 条新闻固定版面</h2>
            </div>
            <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.2em] text-white/50">
              热度 × 影响力 × 行业权重
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
            {grid.map((item) => (
              <CardLink key={item.id} item={item} />
            ))}
          </div>
        </section>

        <section className="rounded-[32px] border border-violet-300/15 bg-[linear-gradient(135deg,rgba(18,10,40,0.9),rgba(8,10,28,0.95))] p-5 shadow-[0_26px_100px_rgba(128,92,255,0.16)] md:p-8">
          <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="mb-2 inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] text-violet-200/70">
                <Orbit className="h-3.5 w-3.5 text-violet-300" />
                Product Radar
              </div>
              <h2 className="text-2xl font-semibold tracking-[-0.03em] text-white md:text-3xl">5 平台产品雷达</h2>
            </div>
            <div className="rounded-full border border-violet-200/15 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.2em] text-violet-100/55">
              Product Hunt / GitHub / Toolify / Hacker News / Trustmrr
            </div>
          </div>

          <div className="grid gap-4 xl:grid-cols-5">
            {todayNews.products.map((item) => (
              <CardLink key={item.id} item={item} mode="product" />
            ))}
          </div>
        </section>

        <footer className="flex flex-col gap-4 rounded-[28px] border border-white/8 bg-white/5 px-6 py-5 text-sm text-white/45 md:flex-row md:items-center md:justify-between">
          <div className="inline-flex items-center gap-2">
            <Boxes className="h-4 w-4 text-cyan-300" />
            小羽毛 AI 天团 · 科技简洁前卫版面
          </div>
          <div className="flex flex-col gap-1 text-right">
            <span>生成时间：{todayNews.generatedAt}</span>
            <span>运行状态：{statusText}</span>
          </div>
        </footer>

        <div
          id="site-run-status-marker"
          className="hidden"
          data-run-status={siteRuntimeStatus.runStatus}
          data-content-date={siteRuntimeStatus.contentDate || todayNews.date}
          data-status-updated-at={siteRuntimeStatus.statusUpdatedAt}
          data-failure-summary={siteRuntimeStatus.failureSummary}
        />
      </div>
    </main>
  );
}
