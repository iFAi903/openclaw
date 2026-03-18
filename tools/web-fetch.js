#!/usr/bin/env node
/**
 * 网页抓取工具 - Node.js 版本
 * 支持: curl方式(快速) / Playwright方式(JS渲染)
 * 
 * 用法: node web-fetch.js <URL> [--method=curl|playwright]
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  // 移动端 User-Agent 列表
  userAgents: {
    iphone: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    android: 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    wechat: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x18002628) NetType/WIFI Language/zh_CN'
  },
  // 超时时间
  timeout: 30000,
  // 最小有效页面大小
  minSize: 1000
};

/**
 * 使用 curl 抓取
 */
async function fetchWithCurl(url, outputPath) {
  console.log('🌐 方法: curl + 移动端UA');
  
  const uas = [CONFIG.userAgents.iphone, CONFIG.userAgents.android, CONFIG.userAgents.wechat];
  
  for (let i = 0; i < uas.length; i++) {
    const ua = uas[i];
    const uaName = ['iPhone', 'Android', 'WeChat'][i];
    console.log(`  📱 尝试 ${uaName} UA...`);
    
    try {
      execSync(
        `curl -s -L -A '${ua}' \
         -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
         -H 'Accept-Language: zh-CN,zh;q=0.9' \
         --compressed \
         --max-time ${CONFIG.timeout / 1000} \
         -o '${outputPath}' \
         '${url}'`,
        { stdio: 'pipe' }
      );
      
      // 检查结果
      const stats = fs.statSync(outputPath);
      if (stats.size > CONFIG.minSize) {
        console.log(`  ✅ 成功: ${stats.size} bytes`);
        return true;
      }
    } catch (e) {
      console.log(`  ❌ ${uaName} 失败`);
    }
  }
  
  return false;
}

/**
 * 使用 Playwright 抓取 (需要安装 @playwright/test)
 */
async function fetchWithPlaywright(url, outputPath) {
  console.log('🖥️  方法: Playwright (Chrome Headless)');
  
  try {
    // 检查是否安装了 playwright
    require.resolve('@playwright/test');
  } catch {
    console.log('  ⚠️  Playwright 未安装，尝试安装...');
    console.log('  运行: npm install -g @playwright/test');
    console.log('  然后: npx playwright install chromium');
    return false;
  }
  
  try {
    const { chromium } = require('@playwright/test');
    
    const browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage({
      userAgent: CONFIG.userAgents.iphone
    });
    
    await page.goto(url, { waitUntil: 'networkidle', timeout: CONFIG.timeout });
    
    // 等待页面加载
    await page.waitForTimeout(2000);
    
    // 获取HTML
    const html = await page.content();
    
    fs.writeFileSync(outputPath, html);
    
    await browser.close();
    
    const stats = fs.statSync(outputPath);
    console.log(`  ✅ 成功: ${stats.size} bytes`);
    
    return stats.size > CONFIG.minSize;
  } catch (e) {
    console.log(`  ❌ Playwright 失败: ${e.message}`);
    return false;
  }
}

/**
 * 提取微信公众号内容
 */
function extractWechatContent(htmlPath, outputPath) {
  console.log('📝 提取微信公众号内容...');
  
  const html = fs.readFileSync(htmlPath, 'utf-8');
  
  // 提取标题
  const titleMatch = html.match(/<h1[^\u003e]*class="rich_media_title[^"]*"[^\u003e]*>([^<]*)/i) ||
                     html.match(/<title>([^<]*)/i);
  const title = titleMatch ? titleMatch[1].trim() : '未找到标题';
  
  // 提取正文 (js_content)
  const contentMatch = html.match(/id="js_content"[^\u003e]*>([\s\S]*?)<\/div\s*\u003e/i);
  
  if (!contentMatch) {
    console.log('  ⚠️  未找到 js_content，尝试提取 body');
    return null;
  }
  
  let content = contentMatch[1];
  
  // 清理HTML标签
  content = content
    .replace(/<[^\u003e]+>/g, '\n')
    .replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/\n\s*\n/g, '\n')
    .trim();
  
  // 保存
  const output = `标题: ${title}\n\n${content}`;
  fs.writeFileSync(outputPath, output);
  
  console.log(`  ✅ 已提取: ${outputPath}`);
  console.log(`  📌 标题: ${title.substring(0, 50)}${title.length > 50 ? '...' : ''}`);
  console.log(`  📊 内容: ${content.length} 字符`);
  
  return { title, content };
}

/**
 * 主函数
 */
async function main() {
  const url = process.argv[2];
  const methodFlag = process.argv.find(arg => arg.startsWith('--method='));
  const method = methodFlag ? methodFlag.split('=')[1] : 'auto';
  
  if (!url) {
    console.log('❌ 用法: node web-fetch.js <URL> [--method=curl|playwright|auto]');
    console.log('');
    console.log('示例:');
    console.log('  node web-fetch.js "https://example.com"');
    console.log('  node web-fetch.js "https://mp.weixin.qq.com/s/xxxxx" --method=curl');
    process.exit(1);
  }
  
  console.log('🪶 小羽毛网页抓取工具 (Node.js)');
  console.log('================================');
  console.log(`URL: ${url}`);
  console.log(`方法: ${method}`);
  console.log('');
  
  const outputPath = path.join(process.cwd(), 'fetched_page.html');
  
  let success = false;
  
  // 按顺序尝试
  if (method === 'auto' || method === 'curl') {
    success = await fetchWithCurl(url, outputPath);
  }
  
  if (!success && (method === 'auto' || method === 'playwright')) {
    console.log('');
    success = await fetchWithPlaywright(url, outputPath);
  }
  
  if (success) {
    console.log('');
    console.log('✅ 抓取完成!');
    console.log(`📄 文件: ${outputPath}`);
    
    // 如果是微信公众号，提取内容
    if (url.includes('mp.weixin.qq.com')) {
      console.log('');
      const contentPath = path.join(process.cwd(), 'wechat_content.txt');
      extractWechatContent(outputPath, contentPath);
    }
    
    process.exit(0);
  } else {
    console.log('');
    console.log('❌ 所有方法均失败');
    console.log('建议:');
    console.log('  1. 检查网络连接');
    console.log('  2. 确认URL可访问');
    console.log('  3. 安装 Playwright: npm install -g @playwright/test && npx playwright install chromium');
    process.exit(1);
  }
}

main().catch(console.error);
