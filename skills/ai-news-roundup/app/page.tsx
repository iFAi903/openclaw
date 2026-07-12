import Link from 'next/link';
import { todayNews, NewsCard } from '@/src/data/news';
import { siteRuntimeStatus } from '@/src/data/siteRuntimeStatus';
import { ArrowUpRight, BadgeCheck, Boxes, Flame, Orbit, Radar, Sparkles } from 'lucide-react';

const cn = (...values: Array<string | false | null | undefined>) => values.filter(Boolean).join(' ');

/** 新闻/产品卡片 */
function CardLink({ item, mode = 'news' }: { item: NewsCard; mode?: 'news' | 'product' }) {
  return (
    <Link
      href={item.url}
      target="_blank"
      className="card group block p-5 md:p-6"
    >
      <div className="flex flex-col gap-3">
        {/* 顶部：来源 + 箭头 */}
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="inline-flex h-6 w-6 items-center justify-center rounded-md bg-gray-100 text-xs font-semibold text-gray-500">
              {item.rank}
            </span>
            <span className="text-[11px] font-medium uppercase tracking-wider text-gray-400">
              {mode === 'news' ? item.source : item.platform || item.source}
            </span>
          </div>
          <ArrowUpRight className="h-3.5 w-3.5 text-gray-300 transition group-hover:text-blue-500" />
        </div>

        {/* 标题 */}
        <h3 className="text-[17px] font-semibold leading-7 text-gray-900">
          {item.title}
        </h3>

        {/* 摘要 */}
        <p className="text-sm leading-6 text-gray-500">
          {item.summary}
        </p>

        {/* 底部：标签 */}
        {item.tags && item.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 pt-1">
            {item.tags.map((tag: string) => (
              <span key={tag} className="tag-badge">{tag}</span>
            ))}
          </div>
        )}
      </div>
    </Link>
  );
}

export default function Home() {
  const top = todayNews.aiNews[0];
  const lead = todayNews.aiNews.slice(1, 5);
  const grid = todayNews.aiNews.slice(5, 15);
  const isDegraded = siteRuntimeStatus.runStatus === 'degraded_success';

  return (
    <main className="min-h-screen bg-[#f6f6f8] text-gray-900">
      <div className="mx-auto flex max-w-[1280px] flex-col gap-8 px-5 pb-20 pt-8 md:px-6 lg:px-8">

        {/* ═══ Header ═══ */}
        <header className="flex flex-col gap-5 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-gray-200/60 md:p-8">
          <div className="flex flex-wrap items-center gap-2 text-xs font-medium uppercase tracking-wider text-gray-400">
            <span className="tag-badge-accent inline-flex items-center gap-1.5">
              <Sparkles className="h-3 w-3" />
              XiaoYuMao AI Briefing
            </span>
            <span className="text-gray-300">·</span>
            <span>{todayNews.date}</span>
            <span className="text-gray-300">·</span>
            <span>{todayNews.aiNews.length} NEWS / {todayNews.products.length} PRODUCTS</span>
          </div>

          <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr] lg:items-end">
            <div className="space-y-5">
              <div className="space-y-3">
                <h1 className="max-w-3xl text-[38px] font-bold leading-[1.12] tracking-[-0.03em] md:text-[52px]">
                  小羽毛 <span className="feather-text">AI 新闻早报</span>
                </h1>
                <p className="max-w-2xl text-base leading-7 text-gray-500">
                  国际 AI 创新新闻每日定版。只留关键事件，不留空洞总结。
                </p>
              </div>

              {/* 统计面板 */}
              <div className="grid gap-3 md:grid-cols-3">
                <div className="stat-panel">
                  <div className="stat-label">今日寄语</div>
                  <div className="stat-value">{todayNews.quote.text}</div>
                </div>
                <div className="stat-panel">
                  <div className="stat-label">验收门禁</div>
                  <div className="stat-value">
                    {todayNews.aiNews.length} 新闻 / {todayNews.products.length} 平台产品 / 近 3 天去重
                  </div>
                </div>
                <div className="stat-panel">
                  <div className="stat-label">运行状态</div>
                  <div className="stat-value">
                    {isDegraded ? '⚠️ 降级交付' : '✅ 完整成功'}
                  </div>
                </div>
              </div>
            </div>

            {/* 质量门禁面板 */}
            <div className="rounded-xl bg-gray-50 p-5 ring-1 ring-gray-200/50">
              <div className="mb-4 flex items-center gap-2 text-sm font-semibold text-gray-700">
                <BadgeCheck className="h-4 w-4 text-blue-500" />
                自动验收上线门禁
              </div>
              <div className="grid gap-2 text-[13px] leading-relaxed text-gray-500">
                {[
                  '标题必须是具体事件，不允许"新动态 / 新能力"',
                  '摘要必须补充标题之外的信息',
                  '产品平台严格一日五源各一条',
                  '当日与前三天双重去重',
                ].map((rule) => (
                  <div key={rule} className="flex items-start gap-2.5 rounded-lg bg-white px-3.5 py-2.5 ring-1 ring-gray-100">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full feather-text" />
                    <span>{rule}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </header>

        {/* ═══ Lead Story ═══ */}
        {top && (
          <section className="grid gap-5 xl:grid-cols-[1.2fr_0.8fr]">
            <Link
              href={top.url}
              target="_blank"
              className="lead-card group p-7 md:p-9"
            >
              <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-50 to-sky-50 px-4 py-1.5 text-[11px] font-semibold uppercase tracking-wider text-blue-600 ring-1 ring-blue-100">
                <Flame className="h-3.5 w-3.5" />
                Lead Story
              </div>
              <h2 className="max-w-3xl text-[28px] font-bold leading-[1.14] tracking-[-0.02em] text-gray-900 md:text-[36px]">
                {top.title}
              </h2>
              <p className="mt-5 max-w-2xl text-base leading-7 text-gray-500">
                {top.summary}
              </p>
              <div className="mt-7 flex items-center justify-between gap-4 border-t border-gray-100 pt-5 text-sm">
                <span className="text-gray-400">{top.source}</span>
                <span className="inline-flex items-center gap-1.5 font-medium text-blue-600 transition group-hover:gap-2">
                  查看原文 <ArrowUpRight className="h-3.5 w-3.5" />
                </span>
              </div>
            </Link>

            {/* Lead 辅助卡片列 */}
            <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-1">
              {lead.map((item) => (
                <CardLink key={item.id} item={item} />
              ))}
            </div>
          </section>
        )}

        {/* ═══ 15 条新闻网格 ═══ */}
        <section className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-gray-200/60 md:p-8">
          <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="mb-1.5 flex items-center gap-2 section-heading">
                <Radar className="h-3.5 w-3.5 text-blue-400" />
                全球 AI 信号
              </div>
              <h2 className="text-2xl font-bold tracking-[-0.02em] text-gray-900">{todayNews.aiNews.length} 条新闻固定版面</h2>
            </div>
            <span className="tag-badge">热度 × 影响力 × 行业权重</span>
          </div>

          <div className="grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
            {grid.map((item) => (
              <CardLink key={item.id} item={item} />
            ))}
          </div>
        </section>

        {/* ═══ 5 平台产品 ═══ */}
        <section className="product-section rounded-2xl p-6 shadow-sm md:p-8">
          <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="mb-1.5 flex items-center gap-2 section-heading">
                <Orbit className="h-3.5 w-3.5 text-violet-400" />
                产品雷达
              </div>
              <h2 className="text-2xl font-bold tracking-[-0.02em] text-gray-900">5 平台产品雷达</h2>
            </div>
            <span className="tag-badge">Product Hunt / GitHub / Toolify / Hacker News / Trustmrr</span>
          </div>

          <div className="grid gap-4 xl:grid-cols-5">
            {todayNews.products.map((item) => (
              <CardLink key={item.id} item={item} mode="product" />
            ))}
          </div>
        </section>

        {/* ═══ Footer ═══ */}
        <footer className="flex flex-col gap-3 rounded-2xl bg-white px-6 py-5 text-sm text-gray-400 shadow-sm ring-1 ring-gray-200/60 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-2">
            <Boxes className="h-4 w-4 text-blue-400" />
            小羽毛 AI 天团 · 高级灰科技版面
          </div>
          <div className="flex flex-col gap-0.5 text-right">
            <span>生成时间：{todayNews.generatedAt}</span>
            <span>运行状态：{isDegraded ? '⚠️ 降级交付' : '✅ 完整成功'}</span>
          </div>
        </footer>

        {/* 隐藏状态标记（供诊断用） */}
        <div
          id="site-run-status-marker"
          className="hidden"
          data-run-status={siteRuntimeStatus.runStatus}
          data-content-date={siteRuntimeStatus.contentDate || todayNews.date}
        />
      </div>
    </main>
  );
}
