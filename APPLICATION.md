# CodeFlow 申请材料

## 04 字段文本

我构建了一个名为 **CodeFlow** 的多 Agent 协作代码智能流水线系统，基于 Claude Code 开发、DeepSeek API 驱动。该项目解决的核心痛点是：传统代码审查依赖人工逐行 Review，效率低、覆盖面窄，安全漏洞和技术债容易被遗漏，中小团队尤其缺乏系统化的自动化审查工具。CodeFlow 通过 4 个角色分工明确的 AI Agent 实现代码审计→方案设计→重构执行→质量验证的完整自动化闭环。

核心逻辑流采用长链推理与多 Agent 协作架构：第一层 Scanner Agent 对目标代码库进行深度审计，检测代码坏味道、安全漏洞（SQL 注入、命令注入、硬编码密钥等 OWASP Top 10 问题）、性能问题和异常处理缺陷，输出结构化 JSON 审计报告；第二层 Architect Agent 接收审计报告，进行二次推理，按 P0-P3 优先级设计分批次重构方案，处理变更依赖关系并评估风险；第三层 Executor Agent 根据方案生成生产级代码变更，输出 Unified Diff 与 Conventional Commits 规范的提交信息；第四层 Reviewer Agent 作为最终门禁，逐批次审查变更的安全性、正确性和完整性，输出通过/驳回裁定。四个 Agent 间的通信全部采用结构化 JSON，形成可追溯、可审计的推理链路。

项目使用 Python 构建，CLI 基于 Click + Rich 实现终端可视化。单次完整流水线运行（50 文件规模代码库）消耗约 200-500 万 Token。目前已在个人项目中投入使用，将代码审查效率提升约 70%。

项目地址：https://github.com/dongjieliang8-blip/codeflow

## 05 截图上传建议

- 终端运行截图：`python -m src.main run ./demo/sample_project`
- 审计报告截图：JSON 格式的扫描报告输出
- 重构结果截图：Reviewer Agent 的通过/驳回裁定
