// 自动生成 - 站点运行状态

export type SiteRunStatus = 'unknown' | 'full_success' | 'degraded_success' | 'failed';

export interface SiteRuntimeStatusPayload {
  runStatus: SiteRunStatus;
  degraded: boolean;
  statusLabel: string;
  contentDate: string;
  statusUpdatedAt: string;
  failureSummary: string;
  lastSuccessfulRunAt?: string;
  lastSuccessfulContentDate?: string;
}

export const siteRuntimeStatus: SiteRuntimeStatusPayload = {
  "runStatus": "full_success",
  "degraded": false,
  "statusLabel": "完整成功版本",
  "contentDate": "2026年05月04日 周一",
  "statusUpdatedAt": "2026-05-04T22:23:54.962252+08:00",
  "failureSummary": "",
  "lastSuccessfulRunAt": "2026-05-04T22:23:54.962252+08:00",
  "lastSuccessfulContentDate": "2026年05月04日 周一"
};

export default siteRuntimeStatus;
