import { todayNews, NewsItem } from '@/src/data/news';
import { Calendar, ExternalLink, Zap, Terminal, Globe, DollarSign, Cpu, ArrowRight, Activity, Layers, Sparkles } from 'lucide-react';
import Link from 'next/link';

const cleanText = (text: string = ''): string => {
  return text
    .replace(/<[^>]*>/g, ' ')
    .replace(/&#(\d+);/g, (_, code) => String.fromCharCode(Number(code)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, code) => String.fromCharCode(parseInt(code, 16)))
    .replace(/&(nbsp|amp|quot|lt|gt|apos|#39);/g, (entity) => {
      const map: Record<string, string> = {
        '&nbsp;': ' ',
        '&amp;': '&',
        '&quot;': '"',
        '&lt;': '<',
        '&gt;': '>',
        '&apos;': "'",
        '&#39;': "'",
      };
      return map[entity] ?? entity;
    })
    // 清理零宽空格和 KEYWORD 占位符（修复翻译引入的占位符问题）
    .replace(/\u200b/g, '')
    .replace(/\u200c/g, '')
    .replace(/\u200d/g, '')
    .replace(/__KEYWORD_\d+_\d+__/g, 'OpenAI')
    .replace(/\s+/g, ' ')
    .trim();
};

// 模拟分类（因为主数据结构没有category字段）
const getCategoryForNews = (index: number, total: number): string => {
  if (index < 2) return 'headline';
  if (index < 5) return 'tech';
  if (index < 8) return 'product';
  if (index < 11) return 'capital';
  return 'global';
};

const getCategoryStyle = (category: string) => {
  switch (category) {
    case 'headline': return { 
      icon: <Sparkles className="w-4 h-4" />, 
      bg: 'bg-gradient-to-r from-sky-500 to-blue-600 text-white',
      label: '头条'
    };
    case 'product': return { 
      icon: <Cpu className="w-4 h-4" />, 
      bg: 'bg-blue-50 text-blue-700 border border-blue-100',
      label: '产品'
    };
    case 'tech': return { 
      icon: <Terminal className="w-4 h-4" />, 
      bg: 'bg-slate-100 text-slate-700 border border-slate-200',
      label: '技术'
    };
    case 'industry': return { 
      icon: <Layers className="w-4 h-4" />, 
      bg: 'bg-slate-100 text-slate-700 border border-slate-200',
      label: '行业'
    };
    case 'capital': return { 
      icon: <DollarSign className="w-4 h-4" />, 
      bg: 'bg-violet-50 text-violet-700 border border-violet-100',
      label: '资本'
    };
    default: return { 
      icon: <Globe className="w-4 h-4" />, 
      bg: 'bg-sky-50 text-sky-700 border border-sky-100',
      label: '全球'
    };
  }
};

export default function Home() {
  const { date, aiNews, products, summary, quote, websiteUrl } = todayNews;
  
  // 分离头条和普通新闻
  const headlines = aiNews.slice(0, 2);
  const regularNews = aiNews.slice(2);

  return (
    <main className="min-h-screen bg-[#F8FAFC] text-slate-900 font-sans selection:bg-blue-100 selection:text-blue-900">
      
      {/* 顶部装饰条 - 羽毛渐变 */}
      <div className="h-1.5 w-full bg-gradient-to-r from-sky-400 via-blue-500 to-violet-500"></div>

      <div className="max-w-7xl mx-auto px-6 md:px-12 py-16 md:py-24 space-y-20">

        {/* Header Section - 宽松间距 */}
        <header className="space-y-8">
          <div className="flex items-center space-x-3">
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full text-sm font-medium text-slate-500 shadow-sm border border-slate-100">
              <Calendar className="w-4 h-4 text-blue-500" />
              {date}
            </span>
          </div>
          
          <div className="space-y-6">
            <h1 className="text-5xl md:text-7xl font-black tracking-tight text-slate-900">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-sky-500 via-blue-600 to-violet-500">
                小羽毛🪶
              </span>
              <span className="text-slate-800"> AI 新闻早报</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-slate-600 font-light leading-relaxed max-w-3xl border-l-4 border-blue-500 pl-6 italic">
              每日 AI 资讯精选，追踪全球科技动态与创新产品
            </p>
          </div>
        </header>

        {/* 每日寄语 - 深蓝卡片 */}
        <section className="bg-gradient-to-br from-slate-900 to-blue-900 rounded-2xl p-8 md:p-10 shadow-xl text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500 rounded-full blur-[120px] opacity-20 pointer-events-none"></div>
          
          <div className="relative z-10">
            <h2 className="text-xs font-bold uppercase tracking-widest text-blue-300 mb-4 flex items-center gap-2">
              <Activity className="w-4 h-4" />
              每日观察
            </h2>
            <p className="text-xl md:text-2xl font-medium leading-relaxed text-blue-50">
              {quote?.text || summary}
            </p>
          </div>
        </section>

        {/* 双头条 - 一行两个 */}
        {headlines.length > 0 && (
          <section className="space-y-8">
            <div className="flex items-center gap-2 px-1">
              <Zap className="w-6 h-6 text-sky-500" />
              <h2 className="text-2xl font-bold text-slate-800">重点头条</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {headlines.map((item, index) => {
                const style = getCategoryStyle('headline');
                return (
                  <article key={item.id} className="group bg-white rounded-2xl p-8 shadow-sm hover:shadow-xl transition-all duration-300 border border-slate-100 hover:border-sky-200 relative overflow-hidden h-full flex flex-col">
                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-sky-400 via-blue-500 to-violet-500"></div>
                    
                    <div className="flex items-center justify-between mb-4">
                      <span className={`px-3 py-1.5 rounded-full text-sm font-bold flex items-center gap-1.5 ${style.bg}`}>
                        {style.icon}
                        {style.label}
                      </span>
                      <span className="text-sm text-slate-400">来源：{cleanText(item.source)}</span>
                    </div>

                    <h3 className="text-2xl font-bold text-slate-900 mb-3 group-hover:text-blue-600 transition-colors leading-tight">
                      <Link href={item.url} target="_blank" className="hover:underline decoration-2 decoration-blue-200 underline-offset-4">
                        {cleanText(item.title)}
                      </Link>
                    </h3>
                    
                    <p className="text-slate-600 leading-relaxed flex-1">
                      {cleanText(item.summary)}
                    </p>

                    <div className="mt-6 pt-4 border-t border-slate-100 flex justify-end items-end min-h-12">
                      <Link href={item.url} target="_blank" className="text-blue-600 font-semibold flex items-center gap-1 group-hover:gap-2 transition-all">
                        阅读全文 <ArrowRight className="w-4 h-4" />
                      </Link>
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        )}

        {/* 普通新闻 - 三列网格 */}
        <section className="space-y-8">
          <div className="flex items-center justify-between px-1">
            <div className="flex items-center gap-2">
              <Globe className="w-6 h-6 text-blue-500" />
              <h2 className="text-2xl font-bold text-slate-800">全球动态</h2>
            </div>
            <span className="text-slate-400 text-sm">{regularNews.length} 条动态</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {regularNews.map((item, index) => {
              const category = getCategoryForNews(index + 2, regularNews.length);
              const style = getCategoryStyle(category);
              return (
                <article key={item.id} className="group bg-white p-6 rounded-xl border border-slate-100 hover:shadow-lg hover:border-blue-200 transition-all duration-200 flex flex-col">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-slate-300 font-mono text-xs">#{index + 3}</span>
                    <span className={`px-2 py-0.5 rounded text-xs font-semibold flex items-center gap-1 ${style.bg}`}>
                      {style.icon}
                      {style.label}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors leading-snug">
                    <Link href={item.url} target="_blank" className="hover:underline decoration-2 decoration-blue-100">
                      {cleanText(item.title)}
                    </Link>
                  </h3>
                  
                  <p className="text-slate-500 text-sm leading-relaxed line-clamp-3 flex-1">
                    {cleanText(item.summary)}
                  </p>
                  
                  <div className="mt-4 pt-3 border-t border-slate-50 flex items-center justify-between">
                    <span className="text-xs text-slate-400">{cleanText(item.source)}</span>
                    <ExternalLink className="w-4 h-4 text-slate-300 group-hover:text-blue-400 transition-colors" />
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        {/* 创新产品追踪 - 底部通栏 */}
        <section className="bg-gradient-to-br from-slate-900 via-violet-900 to-slate-900 py-16 -mx-6 md:-mx-12 rounded-3xl">
          <div className="max-w-7xl mx-auto px-6 md:px-12 space-y-8">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-violet-500 rounded-xl flex items-center justify-center shadow-lg shadow-violet-500/30">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-white">创新产品追踪</h2>
              <span className="ml-auto text-violet-300 text-sm">{products.length} 款今日热门</span>
            </div>
            
            {/* 响应式网格：超宽屏5列，宽屏自适应，窄屏1列 */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
              {products.map((product, index) => (
                <Link 
                  key={product.id} 
                  href={product.url} 
                  target="_blank" 
                  className="group block"
                >
                  <div className="bg-white/10 backdrop-blur-sm p-5 rounded-xl border border-white/10 hover:bg-white/20 hover:border-violet-400/50 hover:shadow-xl hover:shadow-violet-500/20 transition-all duration-200 h-full">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-10 h-10 flex-shrink-0 bg-violet-500 rounded-lg flex items-center justify-center text-white font-bold shadow-lg shadow-violet-500/30 group-hover:scale-105 transition-transform">
                        {index + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-bold text-white group-hover:text-violet-200 line-clamp-2 min-h-[3rem] transition-colors">{cleanText(product.title)}</h4>
                        <span className="text-xs text-violet-300">{cleanText(product.source)}</span>
                      </div>
                    </div>
                    
                    <p className="text-sm text-violet-100/80 leading-relaxed break-words whitespace-normal line-clamp-4 min-h-[5.5rem]">{cleanText(product.summary)}</p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="text-center pt-16 border-t border-slate-200">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-8 h-8 bg-gradient-to-r from-sky-400 via-blue-500 to-violet-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-bold">🪶</span>
            </div>
            <span className="text-slate-400 text-sm">小羽毛 AI 天团</span>
          </div>
          <p className="text-slate-400 text-sm">
            © 2026 · Design by CEO + CTO Collaboration
          </p>
          <p className="text-slate-300 text-xs mt-2">
            生成时间：{todayNews.generatedAt.split('T')[0]}
          </p>
        </footer>

      </div>
    </main>
  );
}
