# FEATURE_REQUESTS.md — 功能请求

> 记录用户请求的新功能
> 用于规划和优先级排序

---

## [FEAT-20250308-001] voice-wakeup-integration

**Logged**: 2026-03-08T03:56:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Requested Capability
语音唤醒功能，支持唤醒词："小羽毛"、"CEO"、"贾维斯"

### User Context
用户希望实现类似贾维斯的语音交互体验，可以随时打断、随时响应

### Complexity Estimate
complex

### Suggested Implementation
- 需要硬件级别的音频监听
- 需要集成语音识别引擎（Whisper/Vosk）
- 需要与OpenClaw Gateway集成
- 可能需要独立的守护进程

### Metadata
- Frequency: first_time
- Related Features: jarvis-mode, persistent-agent
- System Limitation: 当前AI助手无法直接配置系统级语音监听

---

## [FEAT-20250308-002] persistent-daemon-process

**Logged**: 2026-03-08T03:56:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Requested Capability
后台常驻守护进程，开机自动启动，崩溃自动重启，24/7持续运行

### User Context
确保AI助手始终可用，不受会话中断影响

### Complexity Estimate
complex

### Suggested Implementation
- 需要系统级服务配置（systemd/launchd）
- 需要进程监控和自动重启机制
- 需要与OpenClaw Gateway深度集成

### Metadata
- Frequency: first_time
- Related Features: voice-wakeup, heartbeat
- System Limitation: 当前AI助手无法直接配置系统守护进程

---

## [FEAT-20250308-003] auto-learning-optimization

**Logged**: 2026-03-08T03:56:00+08:00
**Priority**: high
**Status**: in_progress
**Area**: config

### Requested Capability
自动优化响应逻辑：贴合用户说话风格、懂用户需求、预判下一步操作

### User Context
用户希望AI能自动学习其偏好和习惯，实现个性化响应

### Complexity Estimate
medium

### Suggested Implementation
- 使用已安装的 self-learning 技能
- 每日自动分析对话历史
- 提取偏好、禁忌、常用操作
- 更新 USER.md 和记忆文件

### Metadata
- Frequency: first_time
- Related Features: self-learning, elite-longterm-memory
- Implementation Status: 技能已安装，配置中

---
