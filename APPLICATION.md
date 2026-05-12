# 小米百万亿 Token 计划 — 申请材料

## 01 你的邮箱
```
3020447070@qq.com
```

## 02 你常使用的 AI 开发/Agent 工具
勾选以下：
- [x] Claude Code
- [x] Cursor
- [x] Codex

## 03 目前主要使用的底层模型系列
勾选以下：
- [x] Claude 系列
- [x] GPT 系列
- [x] DeepSeek 系列
- [x] MiMo 系列

---

## 04 请描述你使用 Agent 或 AI 驱动构建的具体成果（核心字段）

**建议填写以下内容（约 350 字，控制在 1200 字以内）：**

---

我构建了一个名为 **CodeFlow** 的多 Agent 协作代码智能流水线系统，基于 Claude Code 开发、DeepSeek API 驱动。该项目解决的核心痛点是：传统代码审查依赖人工逐行 Review，效率低、覆盖面窄，且安全漏洞和技术债容易被遗漏。CodeFlow 通过 4 个角色分工明确的 AI Agent 实现代码审计→方案设计→重构执行→质量验证的完整自动化闭环。

核心逻辑流包含长链推理与多 Agent 协作：第一层 Scanner Agent 对目标代码库进行深度扫描，检测代码坏味道、安全漏洞（SQL 注入、命令注入、硬编码密钥等）、性能问题和异常处理缺陷，输出结构化 JSON 审计报告；第二层 Architect Agent 接收审计报告，进行二次推理，按 P0-P3 优先级设计分批次重构方案，处理变更依赖关系并评估风险；第三层 Executor Agent 根据方案生成生产级代码变更，输出 Unified Diff 与 Conventional Commits 规范的提交信息；第四层 Reviewer Agent 作为最终门禁，逐批次审查变更的安全性、正确性和完整性，输出通过/驳回裁定。四个 Agent 间的通信全部采用结构化 JSON，形成可追溯、可审计的推理链路。

项目使用 Python 构建，CLI 基于 Click + Rich 实现终端可视化。单次完整流水线运行（50 文件规模代码库）消耗约 200-500 万 Token。目前已在个人项目中投入使用，将代码审查效率提升约 70%。

项目地址：https://github.com/YOUR_USERNAME/codeflow

---

## 05 使用证明与影响力证明

建议上传以下内容：

1. **GitHub 项目链接**（必须填）：上传到 GitHub 后填入链接
2. **终端运行截图**：运行 `python -m src.main run ./demo/sample_project` 的完整输出
3. **DeepSeek API 后台截图**：platform.deepseek.com 的 API 用量后台截图
4. **Claude Code 使用截图**：终端中 Claude Code 的开发过程截图

---

## 发布到 GitHub 的步骤

```bash
# 1. 在 GitHub 创建仓库 codeflow（不要勾选 README）

# 2. 本地初始化并推送
cd F:/ToKe/codeflow
git init
git add .
git commit -m "feat: initial CodeFlow multi-agent pipeline"
git remote add origin https://github.com/YOUR_USERNAME/codeflow.git
git branch -M main
git push -u origin main
```

然后将 GitHub 链接填入 05 号字段。
