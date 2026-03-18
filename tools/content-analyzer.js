#!/usr/bin/env node
/**
 * 竞品内容分析工具 - CRO专用
 * 用于抓取和分析竞品公众号文章、行业资讯
 * 
 * 用法: node content-analyzer.js <URL> [--type=wechat|article]
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * 抓取网页内容
 */
async function fetchContent(url) {
  const outputPath = '/tmp/cro_fetch_temp.html';
  
  // 使用 curl + 微信UA
  const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x18002628) NetType/WIFI Language/zh_CN';
  
  try {
    execSync(
      `curl -s -L -A '${UA}' --max-time 30 -o '${outputPath}' '${url}'`,
      { stdio: 'pipe' }
    );
    
    return fs.readFileSync(outputPath, 'utf-8');
  } catch (e) {
    return null;
  }
}

/**
 * 提取微信公众号文章
 */
function extractWechatArticle(html) {
  // 提取标题
  const titleMatch = html.match(/<h1[^\u003e]*class="rich_media_title[^"]*"[^\u003e]*>\s*([^<]*)/i) ||
                     html.match(/<h2[^\u003e]*class="rich_media_title[^"]*"[^\u003e]*>\s*([^<]*)/i);
  const title = titleMatch ? titleMatch[1].trim() : '未找到标题';
  
  // 提取公众号名称
  const accountMatch = html.match(/var nickname = htmlDecode\("([^"]+)"\)/) ||
                       html.match(/nick_name = '([^']+)'/);
  const account = accountMatch ? accountMatch[1] : '未知公众号';
  
  // 提取正文
  const contentMatch = html.match(/id="js_content"[^\u003e]*>([\s\S]*?)<\/div\s*\u003e/i);
  
  if (!contentMatch) {
    return { title, account, content: null, images: [] };
  }
  
  let contentHtml = contentMatch[1];
  
  // 提取图片
  const images = [];
  const imgRegex = /data-src="(https?:\/\/[^"]+)"/g;
  let match;
  while ((match = imgRegex.exec(contentHtml)) !== null) {
    images.push(match[1]);
  }
  
  // 清理HTML获取纯文本
  let content = contentHtml
    .replace(/<[^\u003e]+>/g, '\n')
    .replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/\n\s*\n/g, '\n')
    .trim();
  
  return { title, account, content, images };
}

/**
 * 分析内容结构
 */
function analyzeContent(article) {
  const analysis = {
    // 基础统计
    stats: {
      titleLength: article.title.length,
      contentLength: article.content ? article.content.length : 0,
      imageCount: article.images.length,
      paragraphCount: article.content ? article.content.split('\n').filter(p => p.trim()).length : 0
    },
    
    // 关键词提取（简单规则）
    keywords: extractKeywords(article.content || ''),
    
    // 内容结构
    structure: analyzeStructure(article.content || ''),
    
    // 可读性评分
    readability: calculateReadability(article.content || '')
  };
  
  return analysis;
}

/**
 * 提取关键词
 */
function extractKeywords(content) {
  const keywords = [];
  
  // AI/科技领域关键词
  const techTerms = [
    'AI', '人工智能', '大模型', 'GPT', 'ChatGPT', 'Claude', 'Gemini',
    '机器学习', '深度学习', '神经网络', '生成式', 'AIGC', 'AGI',
    'OpenAI', 'Google', '微软', 'Meta', '百度', '阿里', '腾讯',
    '自动驾驶', '机器人', '智能体', '多模态', 'RAG', '向量',
    '提示词', '微调', '训练', '推理', '部署'
  ];
  
  for (const term of techTerms) {
    const regex = new RegExp(term, 'gi');
    const matches = content.match(regex);
    if (matches && matches.length > 0) {
      keywords.push({ term, count: matches.length });
    }
  }
  
  // 按出现频率排序
  return keywords.sort((a, b) => b.count - a.count).slice(0, 10);
}

/**
 * 分析内容结构
 */
function analyzeStructure(content) {
  const structure = {
    hasHeading: /[一二三四五六七八九十]、/.test(content) || /^\d+[\.、]/.test(content),
    hasList: /[•·-]/.test(content),
    hasQuote: /[""''']/.test(content),
    hasNumber: /\d+%|\d+亿|\d+万/.test(content),
    hasLink: /https?:\/\//.test(content)
  };
  
  return structure;
}

/**
 * 计算可读性评分
 */
function calculateReadability(content) {
  const sentences = content.split(/[。！？.!?]/).filter(s => s.trim());
  const words = content.length;
  
  if (sentences.length === 0) return 0;
  
  const avgSentenceLength = words / sentences.length;
  
  // 简单评分：句子越短越易读
  let score = 100 - (avgSentenceLength - 20) * 2;
  score = Math.max(0, Math.min(100, score));
  
  return {
    score: Math.round(score),
    avgSentenceLength: Math.round(avgSentenceLength * 10) / 10,
    totalSentences: sentences.length,
    level: score > 80 ? '易读' : score > 60 ? '适中' : '较难'
  };
}

/**
 * 生成分析报告
 */
function generateReport(url, article, analysis) {
  return `
# 📊 竞品内容分析报告

## 基本信息
- **来源**: ${article.account}
- **标题**: ${article.title}
- **URL**: ${url}
- **分析时间**: ${new Date().toLocaleString('zh-CN')}

## 内容统计
| 指标 | 数值 |
|------|------|
| 标题长度 | ${analysis.stats.titleLength} 字 |
| 正文字数 | ${analysis.stats.contentLength} 字 |
| 段落数 | ${analysis.stats.paragraphCount} 段 |
| 图片数 | ${analysis.stats.imageCount} 张 |

## 关键词分析
${analysis.keywords.map(k => `- ${k.term}: ${k.count}次`).join('\n')}

## 内容结构
${Object.entries(analysis.structure).map(([key, val]) => `- ${key}: ${val ? '✅' : '❌'}`).join('\n')}

## 可读性评估
- **评分**: ${analysis.readability.score}/100 (${analysis.readability.level})
- **平均句长**: ${analysis.readability.avgSentenceLength} 字
- **句子总数**: ${analysis.readability.totalSentences} 句

## 💡 分析洞察

### 优点
${analysis.readability.score > 70 ? '- ✅ 可读性较好，易于理解' : '- ⚠️ 句子较长，可考虑精简'}
${analysis.structure.hasHeading ? '- ✅ 有清晰的层级结构' : '- 💡 建议增加小标题提升结构'}
${analysis.stats.imageCount > 0 ? '- ✅ 配图丰富，视觉效果好' : '- 💡 建议增加配图提升阅读体验'}

### 关键词策略
${analysis.keywords.slice(0, 3).map(k => `- "${k.term}" 出现 ${k.count} 次，是核心话题`).join('\n')}

### 可借鉴之处
1. ${analysis.structure.hasList ? '使用列表形式呈现信息，条理清晰' : '考虑使用列表提升信息密度'}
2. ${analysis.structure.hasNumber ? '善用数据支撑观点，增强说服力' : '增加具体数据提升可信度'}
3. 标题长度${analysis.stats.titleLength < 20 ? '简短有力' : analysis.stats.titleLength < 40 ? '适中' : '较长，可考虑精简'}

---
*分析 by 小羽毛 CRO 内容分析工具*
`;
}

/**
 * 主函数
 */
async function main() {
  const url = process.argv[2];
  
  if (!url) {
    console.log('❌ 用法: node content-analyzer.js <公众号文章URL>');
    console.log('示例: node content-analyzer.js "https://mp.weixin.qq.com/s/xxxxx"');
    process.exit(1);
  }
  
  console.log('🪶 CRO 竞品内容分析工具');
  console.log('======================');
  console.log(`目标: ${url}`);
  console.log('');
  
  console.log('🌐 抓取内容...');
  const html = await fetchContent(url);
  
  if (!html) {
    console.log('❌ 抓取失败');
    process.exit(1);
  }
  
  console.log('✅ 抓取成功');
  console.log('');
  
  console.log('📝 提取文章...');
  const article = extractWechatArticle(html);
  console.log(`📌 标题: ${article.title}`);
  console.log(`👤 公众号: ${article.account}`);
  console.log(`🖼️ 图片: ${article.images.length}张`);
  console.log('');
  
  if (!article.content) {
    console.log('❌ 未能提取正文内容');
    process.exit(1);
  }
  
  console.log('📊 分析内容...');
  const analysis = analyzeContent(article);
  
  console.log('');
  console.log('📈 分析结果');
  console.log('==========');
  console.log(`字数: ${analysis.stats.contentLength}`);
  console.log(`段落: ${analysis.stats.paragraphCount}`);
  console.log(`可读性: ${analysis.readability.score}/100 (${analysis.readability.level})`);
  console.log('');
  console.log('🔥 关键词:');
  analysis.keywords.slice(0, 5).forEach(k => {
    console.log(`  - ${k.term}: ${k.count}次`);
  });
  
  // 生成完整报告
  const report = generateReport(url, article, analysis);
  const reportPath = '/tmp/cro_analysis_report.md';
  fs.writeFileSync(reportPath, report);
  
  console.log('');
  console.log('✅ 分析报告已生成');
  console.log(`📄 报告: ${reportPath}`);
  console.log('');
  console.log('💡 使用建议:');
  console.log('  - 将报告保存到 Obsidian 进行长期跟踪');
  console.log('  - 对比多篇竞品文章找出内容趋势');
  console.log('  - 根据关键词优化自己的内容策略');
}

main().catch(console.error);
