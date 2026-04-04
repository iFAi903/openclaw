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
  "runStatus": "degraded_success",
  "degraded": true,
  "statusLabel": "降级兜底已上线",
  "contentDate": "2026年04月04日 周六",
  "statusUpdatedAt": "2026-04-04T13:19:04.370790+08:00",
  "failureSummary": "[pipeline] 新闻内容生成流水线失败（attempt 2）",
  "lastSuccessfulRunAt": "",
  "lastSuccessfulContentDate": ""
};

export default siteRuntimeStatus;
