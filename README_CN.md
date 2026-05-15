# Claude Code 科研实验室

用一个 Claude Code 会话，运行一整个科研实验室。  
22 个 Agent。37 条命令。12 个 Hook。两条路线：ML 与社会科学。

[![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square)](LICENSE)
[![Agents](https://img.shields.io/badge/agents-22-blue?style=flat-square)](.claude/agents/)
[![Commands](https://img.shields.io/badge/commands-37-blueviolet?style=flat-square)](.claude/commands/)
[![Hooks](https://img.shields.io/badge/hooks-12-red?style=flat-square)](.claude/hooks/)
[![Rules](https://img.shields.io/badge/rules-3-orange?style=flat-square)](.claude/rules/)
[![Tracks](https://img.shields.io/badge/tracks-ML%20%2B%20Social%20Science-teal?style=flat-square)](#两条路线)
[![Built for Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-black?style=flat-square)](https://claude.ai/code)

---

## 安装

```bash
git clone https://github.com/YOUR_USERNAME/claude-code-research-lab
cd claude-code-research-lab

# 一次性操作：激活实验室配置
mv lab .claude          # Mac / Linux
Move-Item lab .claude   # Windows PowerShell

claude
```

然后在 Claude Code 中输入：
```
/start
```

完成。`/start` 内置决策树，通过三个问题判断你的研究范式，并引导你进入正确的工作流程。

---

## 两条路线

`/start` 自动运行决策树并设置路线，也可以在 `CLAUDE.md` 中手动配置。

| 路线 | 适用场景 | 核心命令 |
|------|---------|---------|
| **ML** | 模型训练、基准测试、消融实验、实验流水线 | `/experiment-design`、`/implement`、`/eval-metrics`、`/team-experiments` |
| **社会科学** | 问卷调查、访谈、质性编码、伦理审查 | `/study-design`、`/survey-design`、`/irb-protocol`、`/interview-guide`、`/qual-codebook` |
| **混合方法** | 计算社会科学、混合研究设计 | 两条路线结合，由 `/study-design` 统筹编排 |

---

## 37 条命令

### 探索发现
| 命令 | 功能 |
|------|------|
| `/start` | 决策树：识别研究范式，读取项目状态，引导进入正确工作流 |
| `/help` | 根据当前上下文给出下一步建议 |
| `/status` | 快速查看项目状态 |
| `/ideate [方向]` | 从模糊想法生成 3 个具体研究方向 |
| `/hypothesis` | 引导式对话：将模糊想法转化为带有机制和量化预测的可证伪假设 |
| `/lit-review [主题]` | 系统性文献综述与差距分析 |
| `/gap-analysis` | 将贡献定位于已有工作之中 |
| `/research-proposal` | 撰写完整研究方案文档 |

### 规划阶段 — ML 路线
| 命令 | 功能 |
|------|------|
| `/eval-metrics` | 锁定评估协议——**在任何实验之前运行** |
| `/experiment-design [名称]` | 设计实验：条件、指标、基线、计算资源 |
| `/baseline-plan` | 规划并论证所有对比方法 |
| `/ablation-design [方法]` | 设计消融实验矩阵 |
| `/sprint-plan` | 到投稿截止日的 Sprint 计划 |
| `/run-plan` | 实验执行顺序与依赖关系 |
| `/milestone-review` | 里程碑进度审查 |

### 规划阶段 — 社会科学路线
| 命令 | 功能 |
|------|------|
| `/study-design` | 设计类型、变量/构念、效度威胁、IRB 标记、分析计划 |
| `/survey-design` | 设计问卷：题目措辞、量表、反应格式、预测试方案 |
| `/irb-protocol` | 完整伦理审查申请：风险分级、知情同意书、数据管理计划 |
| `/sampling-plan` | 定量研究的功效分析 / 质性研究的饱和度策略 + 招募方案 |
| `/interview-guide` | 半结构化访谈或焦点小组提纲，含逐字稿脚本和追问 |
| `/qual-codebook` | 质性编码方案，含评分者间信度协议（Cohen's κ） |

### 开发构建
| 命令 | 功能 |
|------|------|
| `/data-pipeline [数据集]` | 设计并实现数据处理流水线 |
| `/implement [规格]` | 根据规格文档实现实验代码 |
| `/code-review [路径]` | 检查代码正确性与可复现性 |
| `/reproduce [论文]` | 复现基线论文的实验结果 |

### 分析
| 命令 | 功能 |
|------|------|
| `/analyze [实验]` | 分析结果并给出解读 |
| `/stat-test [实验]` | 显著性检验、回归、Cronbach's α、Cohen's κ |
| `/visualize` | 生成发表级别图表 |
| `/failure-analysis [实验]` | 分析失败案例与局限性 |

### 写作
| 命令 | 功能 |
|------|------|
| `/outline-paper` | 论文大纲——起草章节前必须完成 |
| `/write-section [章节]` | 起草某个章节 |
| `/review-paper` | 模拟同行评审小组 |
| `/write-rebuttal` | 撰写会议 Rebuttal 回复 |
| `/camera-ready [会议]` | 针对特定会议的最终提交清单 |

### 多 Agent 流水线
| 命令 | 功能 |
|------|------|
| `/team-experiments [名称]` | 完整实验流水线：设计 → 构建 → 运行 → 复现 → 验证 |
| `/team-writing` | 完整写作流水线：大纲 → 各章节起草 → 整合 |
| `/team-review` | 3 位独立审稿人 → 领域主席元评审 |

---

## 22 个 Agent

命令会自动调用对应 Agent，也可以直接点名使用。

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
| `lead-engineer` | 代码架构、代码质量、基础设施 |
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
| `ablation-analyst` | 消融设计与解读 |
| `baseline-engineer` | 基线实现与公平比较 |
| `scientific-writer` | 章节级写作 |
| `peer-reviewer` | 模拟同行评审 |
| `ethics-reviewer` | ML 双重用途风险 / 社会科学 IRB 与参与者保护 |
| `devops-researcher` | 计算基础设施 |
| `domain-specialist` | 领域专项知识（可配置） |

---

## 典型工作流

### ML 路线

```
# 从零开始
/ideate [方向]          → 生成 3 个具体方向
/lit-review [方向]      → 调研该领域
/hypothesis             → 形式化研究问题
/eval-metrics           → 写代码之前先锁定评估协议
/experiment-design      → 设计实验规格
/team-experiments       → 设计 → 构建 → 运行 → 验证

# 有结果，需要写论文
/analyze [实验]
/stat-test
/outline-paper
/team-writing
/team-review
```

### 社会科学路线

```
# 研究设计与数据收集
/ideate [主题]          → 生成 3 个具体方向
/hypothesis             → 形式化研究问题
/study-design           → 完整研究方案（含效度分析）
/survey-design          → 问卷量表
  或 /interview-guide   → 访谈提纲
/irb-protocol           → 伦理委员会申请材料
/sampling-plan          → 样本量 / 饱和度策略

# 分析与写作
/analyze [研究]         → 执行分析
/stat-test              → 回归、信度、显著性检验
  或 /qual-codebook     → 质性编码方案
/outline-paper → /team-writing → /team-review
```

---

## 研究诚信规则

系统自动执行，任何 Agent 都无法绕过：

1. **实验前锁定评估协议。** 先运行 `/eval-metrics`，不允许事后改变评判标准。
2. **结果文件不可篡改。** 绝不手动编辑 `experiments/results/`，如有错误重新生成。
3. **基线获得同等调优预算。** 系统会拒绝稻草人式的不公平比较。
4. **研究日志只能追加。** 所有重要决策记录于 `research/research-log.md`。
5. **不允许选择性汇报。** 实验规格中的所有条件都必须在论文中报告。
6. **数据收集前完成 IRB。** 没有伦理审查方案时，`ethics-reviewer` 会阻止研究执行。

---

## 仓库结构

```
.claude/
  agents/          ← 22 个 Agent 定义
  commands/        ← 37 条斜杠命令
  docs/            ← 文档与模板
    templates/     ← 实验规格、论文大纲、Sprint 计划等
  rules/           ← 路径专属执行规则
CLAUDE.md          ← 主配置——在此设置研究范式、领域和目标会议
CONTRIBUTING.md
LICENSE
README.md
README_CN.md
.gitignore
```

启动项目后，实验室会在工作目录中创建以下文件夹：

```
research/            ← 假设、研究方案、研究日志、研究设计
literature/          ← 文献综述、差距分析、参考文献
experiments/         ← 规格、配置、结果（gitignore）
src/                 ← 模型、数据、训练、评估、工具
data/                ← 原始数据（gitignore）、处理后数据（gitignore）
baselines/
analysis/            ← 脚本、图表、输出（gitignore）
papers/              ← 大纲、草稿
production/          ← 里程碑、Sprint、会话状态
```

---

## 协作协议

每个 Agent 在写入任何文件前都会询问：

> 「我可以将此内容写入 [文件路径] 吗？」

没有你的确认，没有任何 Agent 会写入、编辑文件或运行实验。工作流始终遵循：  
**提问 → 假设 → 设计 → 展示草稿 → 你审批 → 执行**

---

## 进一步阅读

- `.claude/docs/quick-start.md` — 完整生命周期说明，四种起点路径详细操作
- `.claude/docs/agent-roster.md` — 完整 Agent 参考，含评审判决和委托地图
- `.claude/docs/coordination-rules.md` — Agent 之间如何协调交接
- `.claude/docs/research-standards.md` — 两条路线的研究质量标准
