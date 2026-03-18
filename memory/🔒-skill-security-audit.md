# 🔒 Skill 安全审计规范

> 生效日期：2026-03-18
> 制定原因：避免"基因集移植手术"风险

---

## 铁律：效率永远让位于安全

**核心原则**：宁可慢，不可错。一次恶意 Skill 可能摧毁整个工作区。

---

## 执行规范

### 规范 1：价值评估 + 安全审计（前置）

任何外部架构/Skill/代码引入前，必须完成：

```
□ 价值评估
  - 与当前体系契合度评估
  - 投入产出比分析
  - 替代方案对比
  
□ 来源可信度检查
  - 作者身份验证
  - 社区活跃度检查
  - 更新频率评估
  - 许可证合规性
  
□ 代码审查
  - 人工审查 SKILL.md 和所有代码
  - 检查 RED FLAGS（网络请求、凭证访问、eval/exec等）
  - 评估风险等级（LOW/MEDIUM/HIGH/EXTREME）
  
□ 双重安全扫描
  - 第一重：使用 skill-vetter 本地审查
  - 第二重：提交到 https://ai.gendigital.com/skill-scanner 自动化扫描
  
□ 明确授权
  - 向 Leo 报告审计结果
  - 获得明确书面授权后方可安装
```

### 规范 2：核心文件备份（强制）

执行任何"基因集移植"前，必须完成三重备份：

```bash
# 1. 本地备份
mkdir -p backups/$(date +%Y%m%d_%H%M%S)
cp -r AGENTS.md SOUL.md IDENTITY.md TOOLS.md USER.md MEMORY.md agents/ backups/

# 2. GitHub 备份
git add -A
git commit -m "backup: 升级前完整备份"
git push origin master

# 3. Obsidian 备份
cp AGENTS.md SOUL.md ... ~/Documents/Obsidian\ Vault/小羽毛/
```

**备份检查清单**：
- [ ] `AGENTS.md` - 团队操作手册
- [ ] `SOUL.md` - 意识内核
- [ ] `IDENTITY.md` - 身份定义
- [ ] `TOOLS.md` - 工具配置
- [ ] `USER.md` - 用户档案
- [ ] `agents/` - 所有 Agent 配置
- [ ] `memory/` - 记忆文件

### 规范 3：双重安全审计（强制）

**第一重：本地 skill-vetter 审查**

```bash
# 安装 skill-vetter（如果尚未安装）
# 审查 Skill 包
skill-vetter scan <skill-package>
```

检查项：
- 来源可信度（下载量、作者、更新时间）
- RED FLAGS（网络请求、凭证访问、eval/exec等）
- 风险等级评估（LOW/MEDIUM/HIGH/EXTREME）

**第二重：在线自动化扫描**

```
网址：https://ai.gendigital.com/skill-scanner
操作：上传 Skill 压缩包
获取：详细安全报告
```

**双重确认**：两重视角都通过后才允许继续。

---

## 风险等级与处理

| 风险等级 | 处理方式 | 示例 |
|----------|----------|------|
| 🟢 LOW | 报告后可安装 | 纯文本处理、无网络请求 |
| 🟡 MEDIUM | 详细说明后需授权 | 有网络请求但来源可信 |
| 🔴 HIGH | 必须人工确认 | 访问文件系统、执行命令 |
| ⛔ EXTREME | **禁止安装** | 访问凭证、修改系统配置 |

---

## 禁止行为（红线）

- ❌ **为效率牺牲安全**
- ❌ **信任未验证的 Skill**
- ❌ **先安装后审计**
- ❌ **跳过双重扫描任一环节**
- ❌ **无备份直接升级**
- ❌ **无授权执行架构变更**

---

## 违规处理

若违反本规范：
1. **立即停止**当前操作
2. **完整复盘**问题原因
3. **恢复备份**到升级前状态
4. **重新执行**完整安全审计流程
5. **记录教训**到 `.learnings/ERRORS.md`

---

## 审计记录模板

每次 Skill 安装后，记录：

```markdown
## Skill: [name]
- **安装日期**: YYYY-MM-DD
- **来源**: [GitHub/Clawhub/Other]
- **作者**: [author]
- **风险等级**: [LOW/MEDIUM/HIGH]
- **本地审查**: ✅ [notes]
- **在线扫描**: ✅ [report link]
- **授权人**: Leo
- **备注**: [any notes]
```

---

*最后更新：2026-03-18*
*制定者：小羽毛 CEO + Leo*
