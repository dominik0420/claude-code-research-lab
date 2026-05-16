<div align="center">

# Claude Code 科研实验室

**用一个 Claude Code 会话，运行一整个科研实验室。**  
22 个 Agent · 38 条命令 · 13 个 Hook · ML 与社会科学双轨

[![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square)](LICENSE)
[![Agents](https://img.shields.io/badge/agents-22-blue?style=flat-square)](.claude/agents/)
[![Commands](https://img.shields.io/badge/commands-38-blueviolet?style=flat-square)](.claude/commands/)
[![Hooks](https://img.shields.io/badge/hooks-13-red?style=flat-square)](.claude/hooks/)
[![Rules](https://img.shields.io/badge/rules-3-orange?style=flat-square)](.claude/rules/)
[![Tracks](https://img.shields.io/badge/tracks-ML%20%2B%20Social%20Science-teal?style=flat-square)](#两条路线)
[![Built for Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-black?style=flat-square)](https://claude.ai/code)

[English](README.md) · [中文](README_CN.md)

</div>

---

## 安装

```bash
git clone https://github.com/YOUR_USERNAME/claude-code-research-lab
cd claude-code-research-lab

# 激活实验室配置（仅需一次）
mv lab .claude          # Mac / Linux
Move-Item lab .claude   # Windows PowerShell

claude
```

进入 Claude Code 后，运行 `/start`。该命令通过三个问题判断研究范式，并将你引导至对应的工作流程，无需手动配置。

**Hook 前置条件：** 13 个生命周期 Hook 需要在 Claude Code 使用的 shell 中能够调用 `bash` 和 `python3`。Mac 和 Linux 用户开箱即用；Windows 用户请安装 [Git for Windows](https://git-scm.com/download/win)（提供 Git Bash），或使用 [WSL](https://learn.microsoft.com/zh-cn/windows/wsl/install) 并在 WSL 内运行 Claude Code。若 `bash` 不可用，Hook 会静默跳过——Agent 和命令功能不受影响。

---

## 两条路线

`/start` 自动运行决策树并设置当前路线，也可在 `CLAUDE.md` 中手动指定。

| 路线 | 适用场景 | 核心命令 |
|------|---------|---------|
| **ML** | 模型训练、基准测试、消融实验、实验流水线 | `/experiment-design`、`/implement`、`/eval-metrics`、`/team-experiments` |
| **社会科学** | 问卷调查、访谈、质性编码、伦理审查 | `/study-design`、`/survey-design`、`/irb-protocol`、`/interview-guide`、`/qual-codebook` |
| **混合方法** | 计算社会科学、混合研究设计 | 两条路线结合，由 `/study-design` 统筹编排 |

---

## 命令

### 探索发现
| 命令 | 说明 |
|------|------|
| `/start` | 决策树：识别研究范式，读取项目状态，引导进入对应工作流程 |
| `/help` | 基于当前项目状态给出下一步建议 |
| `/status` | 项目状态快照 |
| `/ideate [方向]` | 从模糊想法生成 3 个具体研究方向 |
| `/hypothesis` | 引导式对话：将模糊想法转化为带有机制和量化预测的可证伪假设 |
| `/lit-review [主题]` | 系统性文献综述与差距分析 |
| `/gap-analysis` | 将研究贡献定位于已有工作之中 |
| `/research-proposal` | 撰写完整研究方案文档 |

### 规划阶段 — ML 路线
| 命令 | 说明 |
|------|------|
| `/eval-metrics` | 锁定评估协议——**任何实验前必须运行** |
| `/experiment-design [名称]` | 设计实验：条件、指标、基线、计算资源预算的完整规格 |
| `/baseline-plan` | 规划并论证所有对比方法 |
| `/ablation-design [方法]` | 设计消融实验矩阵 |
| `/sprint-plan` | 到投稿截止日的 Sprint 计划 |
| `/run-plan` | 实验执行顺序与依赖关系 |
| `/milestone-review` | 对照里程碑检查进度 |

### 规划阶段 — 社会科学路线
| 命令 | 说明 |
|------|------|
| `/study-design` | 研究设计：设计类型、变量、效度威胁、IRB 标记、分析计划 |
| `/survey-design` | 问卷量表：题目措辞、量表选择、反应格式、预测试方案 |
| `/irb-protocol` | 伦理委员会申请：风险分级、知情同意书、数据管理计划 |
| `/sampling-plan` | 定量研究的功效分析 / 质性研究的饱和度策略，含招募方案 |
| `/interview-guide` | 半结构化访谈或焦点小组提纲，含逐字脚本和追问设计 |
| `/qual-codebook` | 质性编码方案，含评分者间信度协议（Cohen's κ） |

### 开发构建
| 命令 | 说明 |
|------|------|
| `/data-pipeline [数据集]` | 设计并实现数据处理流水线 |
| `/implement [规格]` | 根据规格文档实现实验代码 |
| `/code-review [路径]` | 检查代码正确性与可复现性 |
| `/reproduce [论文]` | 复现基线论文的实验结果 |

### 分析
| 命令 | 说明 |
|------|------|
| `/analyze [实验]` | 对结果进行结构化解读 |
| `/stat-test [实验]` | 显著性检验、回归、Cronbach's α、Cohen's κ |
| `/visualize` | 生成发表级别图表 |
| `/failure-analysis [实验]` | 分析失败案例，刻画研究局限性 |

### 写作
| 命令 | 说明 |
|------|------|
| `/outline-paper` | 论文大纲——章节起草前必须完成 |
| `/write-section [章节]` | 起草某个章节 |
| `/compile-paper [会议]` | 将所有章节草稿整合为 `papers/main.tex` 并编译为 PDF |
| `/review-paper` | 模拟同行评审小组 |
| `/write-rebuttal` | 对审稿人意见的作者回复 |
| `/camera-ready [会议]` | 针对特定会议的最终提交清单 |

### 多 Agent 编排
| 命令 | 说明 |
|------|------|
| `/team-experiments [名称]` | 完整实验流水线：设计 → 构建 → 运行 → 复现 → 验证 |
| `/team-writing` | 完整写作流水线：大纲 → 各章节起草 → 整合 |
| `/team-review` | 3 位独立审稿人 → 领域主席元评审 |

---

## Agent

所有 Agent 均可由命令自动调用，也可直接按名称使用。

### 第一层——研究领导（Opus）
| Agent | 职责 |
|-------|------|
| `research-director` | 科学愿景、贡献定位、发表决策 |
| `principal-investigator` | 假设形成、日常科研判断、结果解读 |
| `project-manager` | Sprint 计划、里程碑、截止日期、风险管理 |

### 第二层——部门负责人（Sonnet）
| Agent | 职责 |
|-------|------|
| `lead-researcher` | 实验设计、评估协议、消融实验——ML 路线 |
| `social-researcher` | 研究设计、问卷方法论、质性方法、IRB——社会科学路线 |
| `lead-engineer` | 代码架构、质量标准、基础设施 |
| `data-scientist` | 统计分析、数据质量、可视化策略 |
| `paper-author` | 写作策略、叙事结构、会议格式规范 |
| `literature-lead` | 文献综述、差距分析、相关工作定位 |

### 第三层——专家（Sonnet / Haiku）
| Agent | 职责 |
|-------|------|
| `ml-engineer` | 模型实现 |
| `data-engineer` | 数据流水线 |
| `stats-analyst` | ML 基准测试、问卷统计、回归、信度分析 |
| `viz-engineer` | 图表生成 |
| `code-reviewer` | 代码正确性与可复现性 |
| `reproducibility-engineer` | 端到端实验复现 |
| `ablation-analyst` | 消融设计与结果解读 |
| `baseline-engineer` | 基线实现与公平比较 |
| `scientific-writer` | 章节级学术写作 |
| `peer-reviewer` | 模拟同行评审 |
| `ethics-reviewer` | ML 双重用途风险 / 社会科学 IRB 与参与者保护 |
| `devops-researcher` | 计算基础设施 |
| `domain-specialist` | 领域专项知识（可按项目配置） |

---

## Hook

13 个 Hook 在整个会话生命周期中自动执行研究诚信规则。

| Hook | 触发事件 | 行为 |
|------|---------|------|
| `guard-results` | PreToolUse: Write\|Edit | **阻断**对 `experiments/results/` 的任何写入——结果不可篡改 |
| `guard-eval-protocol` | PreToolUse: Bash | 未锁定评估协议时，禁止运行实验并给出警告 |
| `guard-irb` | PreToolUse: Write | 无 IRB 协议时，写入数据收集路径前给出警告 |
| `validate-experiment-command` | PreToolUse: Bash | 验证实验命令是否包含配置文件和输出目录 |
| `log-research-activity` | PostToolUse: Write | 将关键写入操作自动追加到 `research/research-log.md` |
| `validate-experiment-spec` | PostToolUse: Write | 验证 `experiments/specs/` 中的规格文档是否包含所有必填字段 |
| `update-session-state` | PostToolUse: Write | 每次里程碑写入后更新 `production/session-state/active.md` |
| `capture-git-hash` | PostToolUse: Bash | 实验运行后将 Git Hash 和分支记录到 `experiments/run-log.md` |
| `check-hardcoded-paths` | PostToolUse: Write | 扫描 Python 源文件中的硬编码路径、超参数和缺失随机种子 |
| `track-paper-sections` | PostToolUse: Write | 写入任何章节草稿后，重建 `papers/STATUS.md` 的进度看板 |
| `check-config-yaml` | PostToolUse: Write | 验证实验 YAML 配置文件包含 `seed`、`output_dir` 和模型参数 |
| `experiment-complete-notify` | PostToolUse: Bash | 实验运行后检测新结果文件，建议后续分析命令 |
| `session-summary` | Stop | 会话结束时输出完整的项目状态清单 |

---

## 工作流

### ML 路线

```
# 从零开始到完成实验
/ideate [方向]          → 生成 3 个具体研究方向
/lit-review [方向]      → 系统性文献调研
/hypothesis             → 形式化研究问题
/eval-metrics           → 写任何代码之前锁定评估协议
/experiment-design      → 生成完整实验规格文档
/team-experiments       → 设计 → 构建 → 运行 → 复现 → 验证

# 从结果到投稿论文
/analyze [实验]         → 对结果进行结构化解读
/stat-test              → 显著性检验与效应量
/outline-paper          → 构建论文论证结构
/team-writing           → 起草所有章节
/compile-paper [会议]   → 整合 main.tex，编译为 PDF
/team-review            → 模拟同行评审小组
```

### 社会科学路线

```
# 研究设计
/ideate [主题]          → 生成 3 个具体研究方向
/hypothesis             → 形式化研究问题
/study-design           → 完整研究方案（含效度分析）
/irb-protocol           → 伦理委员会申请材料包
/sampling-plan          → 样本量论证与招募方案

# 量表与工具制作
/survey-design          → 问卷量表（题目、量表类型、反应格式）
/export-survey [格式]   → 导出为 HTML（可分享）、Qualtrics 导入文件
                          或本地 Flask 数据收集服务器
/interview-guide        → 半结构化访谈或焦点小组提纲

# 数据收集（在实验室外部完成——实验室负责生成工具）
#   → 发送 HTML 链接、上传至 Qualtrics/Google Forms
#     或运行本地 Flask 服务器用于现场采集
#   → 采集完成后，导出 CSV 数据

# 分析与写作
/analyze [研究]         → 对导入的问卷数据执行预定分析
/stat-test              → 回归、信度分析、显著性检验
/qual-codebook          → 质性编码方案与信度协议
/outline-paper → /team-writing → /compile-paper → /team-review
```

---

## 研究诚信规则

以下规则在整个工作流中由 Hook 和 Agent 共同强化执行，并标注各规则的执行力度。

1. **结果文件不可篡改。**（硬阻断）`guard-results` Hook 对任何写入 `experiments/results/` 的操作返回非零退出码。如需修正，须使用更新后的配置文件重新运行实验。
2. **实验前须锁定评估协议。**（警告 + 日志）若 `experiments/eval-protocol.md` 不存在或未标记为 `LOCKED`，`guard-eval-protocol` Hook 会在任何实验命令执行前发出警告并记录违规。不阻断执行。
3. **数据收集前须完成 IRB。**（警告 + 日志）若 `research/irb-protocol.md` 不存在，向数据收集路径写入前将触发警告并记录。不阻断执行，因各机构 IRB 时间安排不同。
4. **基线获得同等调优预算。**（Agent 门控）`baseline-engineer` Agent 会标记使所提方法获得不公平优势的配置，由研究者作最终决定。
5. **所有条件均须汇报。**（Agent 门控）`lead-researcher` 门控会在批准论文草稿前，核查实验规格中定义的每个条件是否均出现在结果章节。
6. **研究日志自动维护。**（被动）`log-research-activity` Hook 在每次重要写入后自动追加带时间戳的条目到 `research/research-log.md`。
4. **研究日志只能追加。** `research/research-log.md` 由 `log-research-activity` Hook 自动写入，不允许事后修改。
---

## 仓库结构

```
.claude/
  agents/          ← 22 个 Agent 定义
  commands/        ← 39 条斜杠命令
  hooks/           ← 13 个生命周期 Hook
  scripts/         ← compile_paper.py、export_survey.py
  docs/            ← 文档与模板
    templates/     ← hypothesis、research-idea、论文大纲
  rules/           ← 路径专属执行规则
  settings.json    ← Hook 配置
CLAUDE.md          ← 主配置：范式、领域、框架、目标会议
CONTRIBUTING.md
LICENSE
README.md
README_CN.md
.gitignore
```

运行时创建的项目目录：

```
research/            ← 假设、研究方案、研究设计、研究日志
literature/          ← 文献综述、差距分析、参考文献库
experiments/         ← 规格、配置、评估协议、运行日志、结果
src/                 ← 模型、数据加载器、训练、评估、工具函数
data/                ← 原始数据（gitignore）、处理后数据（gitignore）
baselines/
analysis/            ← 脚本、图表、输出（gitignore）
papers/              ← 大纲、章节草稿、STATUS.md
production/          ← 里程碑、Sprint、会话状态
```

---

## 协作协议

每个 Agent 在写入任何文件前都会请求确认：

> 「我可以将此内容写入 `[文件路径]` 吗？」

没有明确授权，任何 Agent 都不会写入、编辑文件或执行实验。所有工作流遵循同一序列：

**提问 → 假设 → 设计 → 起草 → 评审 → 确认 → 执行**

---

## 贡献

添加 Agent、命令或新路线的规范，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

[MIT](LICENSE)
