---
name: project-digital-nuwa
description: 数字女娲项目图表输出路径、样式规范和数据结构
metadata:
  type: project
---

图表脚本路径：`digital-nuwa/analysis/generate_figures.py`
图表输出目录：`digital-nuwa/analysis/outputs/figures/`

**Why:** 项目使用 digital-nuwa/ 前缀隔离多项目输出，analysis/outputs/figures/ 是可视化工程师的标准输出位置。

**How to apply:** 所有图表脚本写入 analysis/figures/，输出保存至 analysis/outputs/figures/，不直接读取 experiments/results/。

已生成图表（2026-05-19）：
- figure1_dimension_results.png — 四维度物理特征→观感映射横向条形图
- figure2_scene_matching.png — 四大场景适配验证横向条形图
- figure3_cohens_h_comparison.png — 全部假设 Cohen's h 效应量点状比较图
