# CodeFlow — Multi-Agent Code Intelligence Pipeline

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

**CodeFlow** is a multi-agent AI pipeline that orchestrates 4 specialized agents to analyze, refactor, and validate codebases through structured long-chain reasoning.

```
Scanner → Architect → Executor → Reviewer
   │           │            │           │
   ▼           ▼            ▼           ▼
  Audit    Design Plan   Generate    Validate
  Code     Refactoring   Code        & Review
  Issues   Strategy      Changes     Changes
```

### Architecture

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Scanner** | Deep code audit — detects code smells, security holes, performance issues | Raw source files | Structured JSON issue report |
| **Architect** | Designs prioritized refactoring plan with dependency ordering | Scanner report | Batched refactoring plan with risk assessment |
| **Executor** | Generates concrete, production-ready code changes | Architect plan + source code | Diffs, commit messages, full file contents |
| **Reviewer** | Validates safety, correctness, and completeness of changes | Executor output + scanner context | Verdict + structured review report |

### Key Features

- **Long-chain reasoning**: Each agent consumes the previous agent's structured output, building a reasoning chain across 4 stages
- **Multi-agent collaboration**: 4 agents with distinct system prompts, roles, and output schemas
- **Structured inter-agent communication**: All agent outputs are JSON-serializable, enabling pipelining and audit trails
- **Security-first**: Scanner detects SQL injection, command injection, hardcoded secrets, unsafe eval
- **Git-native**: Executor generates conventional commit messages for each change batch

### Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/codeflow.git
cd codeflow

# Install
pip install -r requirements.txt

# Configure (get your key at https://platform.deepseek.com)
cp .env.example .env
# Edit .env: set DEEPSEEK_API_KEY=sk-xxx

# Run full pipeline on a project
python -m src.main run ./demo/sample_project

# Run scanner only (dry run)
python -m src.main scan ./demo/sample_project

# Check config
python -m src.main config
```

### Demo Output

```
╭──────────────────────────────────────────╮
│ STAGE 1/4: Scanner Agent — auditing      │
│ codebase                                 │
╰──────────────────────────────────────────╯
┌─────────────── Scanner Results ──────────┐
│ Total Files      │ 2                     │
│ Total Lines      │ 48                    │
│ Critical Issues  │ 3                     │
│ High Issues      │ 2                     │
│ Medium Issues    │ 3                     │
│ Low Issues       │ 2                     │
└──────────────────────────────────────────┘

╭──────────────────────────────────────────╮
│ STAGE 2/4: Architect Agent — designing   │
│ refactoring plan                         │
╰──────────────────────────────────────────╯
Strategy: Fix critical security issues first...
Batches planned: 4
  • P0 Fix hardcoded credentials and command injection
  • P1 Resolve SQL injection vulnerability
  • P2 Improve error handling
  • P3 Code style improvements

... (Stages 3 & 4) ...

Pipeline Complete — Time: 23.4s — Verdict: APPROVED
```

### Requirements

- Python 3.10+
- DeepSeek API key ([platform.deepseek.com](https://platform.deepseek.com))
- OpenAI Python SDK (works with DeepSeek's compatible API)

### Token Consumption

A full pipeline run on a ~50-file codebase consumes approximately 2-5 million tokens across all 4 agents, depending on codebase size and issue count.

---

<a name="chinese"></a>
## 中文

**CodeFlow** 是一个多 Agent 协作的 AI 代码智能流水线，通过 4 个角色分工明确的 Agent 实现代码审计→方案设计→代码重构→质量验证的完整闭环。

### 架构

```
Scanner（扫描员） → Architect（架构师） → Executor（执行者） → Reviewer（审查员）
    │                    │                    │                  │
    ▼                    ▼                    ▼                  ▼
  深度审计            制定重构方案         生成代码变更       验证变更质量
  代码质量问题        排优先级与依赖       输出Diff与        批准/驳回
  与安全隐患          关系                 提交信息          变更
```

### Agent 职责

| Agent | 核心能力 |
|-------|---------|
| **Scanner** | 检测代码坏味道、安全漏洞（SQL注入/命令注入/硬编码密钥）、性能问题、异常处理缺陷 |
| **Architect** | 基于扫描报告制定分批次的重构计划，处理依赖关系，评估风险 |
| **Executor** | 根据方案生成生产级代码变更，输出完整Diff和Conventional Commits |
| **Reviewer** | 逐批次审查变更的安全性、正确性、完整性，输出通过/驳回结论 |

### 核心亮点

- **长链推理**：每个 Agent 消费上一个 Agent 的结构化输出，形成跨 4 阶段的推理链路
- **多 Agent 协作**：4 个 Agent 拥有独立的系统提示词、角色定义和输出 Schema
- **结构化通信**：所有 Agent 间通信均为 JSON 格式，可追溯、可审计
- **安全保障**：扫描器覆盖 OWASP Top 10 常见漏洞类型
- **Git 原生**：执行器输出符合 Conventional Commits 规范的提交信息

### 快速开始

```bash
git clone https://github.com/YOUR_USERNAME/codeflow.git
cd codeflow
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填入 DEEPSEEK_API_KEY=sk-xxx
python -m src.main run ./demo/sample_project
```

### 技术栈

- **LLM**: DeepSeek API（兼容 OpenAI SDK）
- **CLI**: Click + Rich
- **语言**: Python 3.10+
- **Token 消耗**: 完整流水线运行约消耗 200-500 万 Token（50 文件规模）

---

## License

MIT
