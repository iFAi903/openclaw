#!/usr/bin/env node

/**
 * OpenClaw Skill: Team Dispatcher (HTTP Edition)
 * Description: CEO 调度 CRO/CTO 的专用通道 (使用 OpenAI 兼容协议)
 */

const http = require('http');

// 团队花名册
const TEAM = {
  cro: {
    host: '127.0.0.1',
    port: 18766,
    token: '76fb289bb8e07ad6aa1f09255e506d551e67f63ffcacecee',
    role: 'CRO (首席营收/创意官)',
    model: 'anthropic/claude-opus-4-6'
  },
  cto: {
    host: '127.0.0.1',
    port: 18793,
    token: '81dc212c3da1a8c9ee272e8030cab897f159d7d0f0374f49',
    role: 'CTO (首席技术官)',
    model: 'anthropic/claude-opus-4-6'
  }
};

const [,, targetAgent, message] = process.argv;

if (!targetAgent || !TEAM[targetAgent]) {
  console.error(`❌ 目标错误。可用目标: ${Object.keys(TEAM).join(', ')}`);
  process.exit(1);
}

const agentConfig = TEAM[targetAgent];
console.log(`📡 正在呼叫 ${agentConfig.role} (via HTTP)...`);

const payload = JSON.stringify({
  model: agentConfig.model,
  messages: [
    { role: 'system', content: `你是 ${agentConfig.role}。请以专业、精炼的风格回答。` },
    { role: 'user', content: message }
  ],
  stream: false
});

const req = http.request({
  hostname: agentConfig.host,
  port: agentConfig.port,
  path: '/v1/chat/completions', // 标准兼容接口
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${agentConfig.token}`,
    'Content-Length': Buffer.byteLength(payload)
  }
}, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    if (res.statusCode === 200) {
      try {
        const result = JSON.parse(data);
        const reply = result.choices?.[0]?.message?.content || "无内容返回";
        console.log(`\n💬 ${targetAgent.toUpperCase()} 回复:\n`);
        console.log(reply);
        console.log("\n✅ 任务完成");
      } catch (e) {
        console.error("❌ 解析失败:", data);
      }
    } else {
      console.error(`❌ 请求失败 (Status: ${res.statusCode}):`, data);
    }
  });
});

req.on('error', (e) => {
  console.error(`❌ 连接错误: ${e.message}`);
});

req.write(payload);
req.end();
