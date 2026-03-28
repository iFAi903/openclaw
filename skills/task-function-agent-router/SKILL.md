---
name: task-function-agent-router
description: Route work to the right agent persona based on task type, function, domain, deliverable, and channel. Use when the user needs help choosing an agent, defining a role/persona for an agent, mapping tasks to functional owners, building multi-agent workflows, or adapting agency-agents-zh roles into a practical operating roster.
---

# Task Function Agent Router

Map a request to the most suitable agent persona by **task + function**, not by job title alone.

## Core rule

Always classify the request on these five axes before choosing an agent:
1. **Task type**: research / strategy / execution / review / operations / coordination
2. **Function**: engineering / product / design / marketing / sales / support / compliance / finance / PM
3. **Domain**: Feishu / WeChat / Xiaohongshu / web app / B2B SaaS / China market / etc.
4. **Deliverable**: plan / PRD / code / content / audit / report / workflow / dashboard
5. **Working mode**: single expert / paired experts / orchestrated workflow

## Output format

When asked to recommend or define an agent, return a compact block:

```markdown
## 推荐 Agent
- 主 Agent：<name>
- 协作 Agent：<optional>
- 为什么：<1-2 句>
- 典型产出：<deliverable>
- 不适合做：<boundary>
```

## Routing logic

### Prefer by function first
- **Engineering**: building, debugging, architecture, integration, performance, security, review
- **Product**: discovery, prioritization, PRD, roadmap, feedback synthesis
- **Design**: UI, UX, visual system, brand, storytelling, image prompting
- **Marketing**: content strategy, platform ops, growth, SEO, social, private domain
- **Sales**: discovery, proposal, pipeline, outbound, deal strategy
- **PM / Operations**: execution tracking, cross-team coordination, studio ops, experiment tracking
- **Compliance / Legal / Risk**: contract, policy, audit, governance
- **Support / Summary / Reporting**: executive summary, analytics report, responder

### Prefer by domain second
Use domain-specific agents when the platform or market matters.
Examples:
- Feishu integration → `engineering-feishu-integration-developer`
- WeChat Official Account ops → `marketing-wechat-operator` or `marketing-wechat-official-account`
- Xiaohongshu growth → `marketing-xiaohongshu-operator`
- China ecommerce → `marketing-china-ecommerce-operator`
- Compliance-heavy healthcare marketing → `healthcare-marketing-compliance`

### Prefer by deliverable third
If multiple agents fit, choose the one whose typical output most closely matches the request.
Examples:
- Need PRD / prioritization → product agents
- Need working code / API / integration → engineering agents
- Need operating playbook / campaign plan → marketing or PM agents
- Need audit / review → reviewer, auditor, compliance agents

## Pairing patterns

Use two-agent pairing when one role creates and another validates.

Common pairs:
- Product Manager + UX Researcher
- Product Manager + Software Architect
- Feishu Integration Developer + Compliance Auditor
- Xiaohongshu Operator + Content Creator
- Backend Architect + Code Reviewer
- Studio Producer + Project Shepherd

## Orchestration trigger

Use an orchestrated workflow when all are true:
- more than one function is involved
- dependencies exist across steps
- the output of one role becomes the input of another
- quality gates matter

In that case, choose **Agents Orchestrator** as lead and attach specialist roles.

## Suggested roster for Leo's team

Use this compact operating roster as default:
- **Strategy / structure** → `product-manager`, `project-manager-senior`, `agents-orchestrator`
- **Technical build** → `engineering-software-architect`, `engineering-backend-architect`, `engineering-feishu-integration-developer`, `engineering-ai-engineer`, `engineering-code-reviewer`
- **Experience / design** → `design-ux-architect`, `design-ui-designer`, `design-brand-guardian`, `design-visual-storyteller`
- **Growth / China platforms** → `marketing-xiaohongshu-operator`, `marketing-wechat-operator`, `marketing-weixin-channels-strategist`, `marketing-zhihu-strategist`, `marketing-growth-hacker`
- **Ops / delivery** → `project-management-studio-producer`, `project-management-project-shepherd`, `project-management-experiment-tracker`
- **Risk / governance** → `compliance-auditor`, `legal-contract-reviewer`, `specialized-risk-assessor`

## References

Read these only when needed:
- `references/agent-mapping.md` for the curated mapping table
- `references/persona-roster.md` for the recommended team roster and usage boundaries
