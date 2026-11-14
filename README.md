# Why is AI-generated language so hard to understand?
### 为什么 AI 生成的语言如此难以理解？—— 心理语言学对齐与反极端压缩工程

[![CI](https://github.com/daybydaymylove-max/Why-is-AI-generated-language-so-hard-to-understand/actions/workflows/ci.yml/badge.svg)](https://github.com/daybydaymylove-max/Why-is-AI-generated-language-so-hard-to-understand/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2610.29162v1-b31b1b.svg)](https://arxiv.org/html/2610.29162v1)

> 本开源项目基于纽约大学（NYU）与德克萨斯大学奥斯汀分校（UT Austin）前沿学术论文 **arXiv:2610.29162v1**: *Why is AI-generated language so hard to understand?* (Thomas Hikaru Clark, Matias B. Martin, Kyle Mahowald)。  
> 提供了针对 AI 文本“难懂综合征”的**全景理论剖析**、**自动化心理语言学审查引擎 (Intelligibility Linter)**、**四步解耦重构流水线 (Text Decoupler)**，以及配套的 **AI 代理精确 Skill 规范**。

---

## 目录 (Table of Contents)
- [一、 痛点物理本质：AI 为什么越变越难懂？](#一-痛点物理本质ai-为什么越变越难懂)
- [二、 六大病态语言学特征 (The 6 Pathological Features)](#二-六大病态语言学特征-the-6-pathological-features)
- [三、 四步解耦重构流水线 (The 4-Step Decoupling Pipeline)](#三-四步解耦重构流水线-the-4-step-decoupling-pipeline)
- [四、 核心模块与架构](#四-核心模块与架构)
- [五、 快速安装与使用 (Quick Start)](#五-快速安装与使用-quick-start)
  - [1. 安装](#1-安装)
  - [2. Python API 快速调用](#2-python-api-快速调用)
  - [3. 自动化审查与解耦示例](#3-自动化审查与解耦示例)
- [六、 精确 Skill 集成 (Antigravity / Claude / Cursor)](#六-精确-skill-集成-antigravity--claude--cursor)
- [七、 单元测试与极限边界防御](#七-单元测试与极限边界防御)
- [八、 出厂质量控制清单 (OQC)](#八-出厂质量控制清单-oqc)
- [九、 学术引用 (Citation)](#九-学术引用-citation)

---

## 一、 痛点物理本质：AI 为什么越变越难懂？

当今大语言模型（如 GPT-5.6、Claude 5、Qwen2.5、Olmo Think 等）在经过深度后训练后，经常生成一些**“在语法上完全合法，但在人类认知上极其耗费精力”**的句子（如 *"The convoluted sentence is quietly eating its own reader-patience budget footnote it"*）。

根据论文的实证研究，这一现象背后的物理机制是**演化目标的系统性脱节**：
1. **人类语言的生理约束**：受制于人类有限的工作记忆（Lossy Working Memory）与递增式在线解析（Incremental Online Processing），人类自然语言在演化中追求**依存距离最小化 (DLM; Gibson 1998)** 与**统一信息密度 (UID; Levy & Jaeger 2007)**，通过在难点处补充关系词（`that`）和高频缓冲词，在发话成本与理解成本间取得帕累托平衡。
2. **AI 后训练的极端压缩**：在数学、代码与长上下文强化学习（RLVR / GRPO）中，人类反馈被移除，且模型受到严格的**长度惩罚（Length Penalty, $\lambda > 0$）**。模型被极化为一台“极限信息压缩机器”，自发选择 Token 极少但严重击穿人类认知预算的构式。

```
【人类语言演化】 ──► 平衡生成与理解 ──► 统一信息密度 (UID) + 依存距离最小化 (DLM) ──► 易读易懂
【大模型后训练】 ──► RLVR + 长度惩罚 ──► 正确性与交流解耦 + 极限压缩 ────────────► 晦涩难懂 (OOD)
```

---

## 二、 六大病态语言学特征 (The 6 Pathological Features)

论文通过对 14 款模型的横向测评与双向回译（Round-Trip Translation）基准确证了 6 大典型特征：

| 编号 | 病态语言学特征 | 认知生理损伤机制 | 论文典型实测违规样例 (Table 2) |
| :---: | :--- | :--- | :--- |
| **01** | **无生命主语搭配生命动词**<br>*(Inanimate Subject + Animate Verb)* | 违背选择限制（Selectional Restriction）。人类依赖生命度线索（Animacy Cues）进行快速语义角色分配；违反时大脑诱发 **P600 冲突重构脑电波**。 | `"The docstring promises they are skipped..."`<br>`"...asymmetry bites."` |
| **02** | **连续名词三连堆叠**<br>*(Stacked Nouns $\ge 3$)* | 连续多个名词作修饰语，触发**括号歧义（Bracketing Ambiguity）**，导致读者无法即时判定核心词与从属层级。 | `"dotfile backup path handling"`<br>`"reader-patience budget"` |
| **03** | **切除关系词的缩略宾从**<br>*(Reduced Object Relative Clause)* | 宾从本身具有非规范逆转语序；模型为了节省 Token 强行切除可选关系代词（`that`/`which`），极易触发**花园路径（Garden-path）**阅读停顿。 | `"That is not trip to Vegas money, that is leave the job [that] you hate money."` |
| **04** | **临时名词活化为动词**<br>*(Ad-hoc Denominal Verbs)* | 将名词直接当作动词使用，强迫读者在心理词库中进行非常规的**词性重构（Syntactic Re-evaluation）**。 | `"Austin cushions price spikes."`<br>`"footnote it."` |
| **05** | **标准化超长依存跨度**<br>*(Standardized Dependency Length)* | 主谓、动宾跨越冗长修饰成分，直接击穿读者有限的工作记忆缓冲。 | `"The guitar sitting in the corner because you're still deciding teaches you zero chords."` |
| **06** | **罕见 N-gram 与高困惑度**<br>*(Unattested N-grams & Trigram PPL)* | 激进跳过人类交流依赖的高频可预测过渡词，制造非常规突兀拼贴以压缩 Token。 | 制造非常规生僻搭配，破坏阅读心流。 |

---

## 三、 四步解耦重构流水线 (The 4-Step Decoupling Pipeline)

为了使 AI 生成文本恢复人类可理解性，本项目落地了确定性的四步解耦流水线：

```
[原始高压缩文本]
       │
       ▼
【第 1 步：名词堆叠解耦】───► 识别连续名词串，将修饰成分转为介词短语（of / for / with）
       │
       ▼
【第 2 步：主谓生命度修正】───► 剥离无生命主语的拟人化谓语，恢复被动式、介词状语或客观事实动词
       │
       ▼
【第 3 步：补齐语法连接算子】─► 强制补充省略的 that / which / in order to，阻断花园路径停顿
       │
       ▼
【第 4 步：依存距离局部化】───► 识别跨度 > 5 个词的主谓/动宾弧，执行破句拆解为独立逻辑主谓
       │
       ▼
[工业级易读文本]
```

---

## 四、 核心模块与架构

```
Why-is-AI-generated-language-so-hard-to-understand/
├── .github/workflows/ci.yml       # 自动化持续集成流水线
├── intelligibility_linter/        # 核心 Python 审查与重构包
│   ├── __init__.py                # 顶层 API 导出
│   ├── models.py                  # 强类型数据传输对象 (DTO, Report, Diagnostics)
│   ├── rules.py                   # 6 大特征规则判定引擎 (时间复杂度 O(N))
│   ├── auditor.py                 # 核心静态审查器 (计算评分与合规裁定)
│   └── decoupler.py               # 4 步解耦重构器 (Before vs After 解耦)
├── skills/
│   └── ai-text-intelligibility/   # 工业级 Agent 技能包
│       ├── SKILL.md               # 心理语言学对齐规范
│       └── scripts/               # 独立脚本
├── docs/
│   ├── ARXIV_2610_29162v1_ANALYSIS.md # 论文深度剖析白皮书
│   ├── Why is AI-generated language so hard to understand.pdf    # 英文原版论文
│   └── Why is AI-generated language so hard to understand_zh.pdf # 中文精翻版论文
└── tests/                         # 单元测试与极限边界测试套件
```

---

## 五、 快速安装与使用 (Quick Start)

### 1. 安装
```bash
git clone https://github.com/daybydaymylove-max/Why-is-AI-generated-language-so-hard-to-understand.git
cd Why-is-AI-generated-language-so-hard-to-understand
pip install -r requirements.txt
pip install -e .
```

### 2. Python API 快速调用

```python
from intelligibility_linter import IntelligibilityAuditor, TextDecoupler

# 1. 实例化审查器与解耦器
auditor = IntelligibilityAuditor()
decoupler = TextDecoupler()

# 2. 待测高压缩 AI 文本 (包含拟人动词、名词堆叠、省略从句)
ai_text = "The docstring promises dotfile backup path handling without issues. This is the job you hate."

# 3. 执行心理语言学审查
report = auditor.audit(ai_text)
print(f"易读性评分: {report.intelligibility_score}/100")
print(f"是否达到生产交付标准: {report.is_production_ready}")

for diag in report.diagnostics:
    for issue in diag.issues:
        print(f"[{issue.severity}] {issue.category.value}: {issue.message}")
        print(f"建议重构: {issue.suggested_rewrite}")

# 4. 自动化四步解耦重构
clean_text = decoupler.decouple_and_reconstruct(ai_text)
print("\n重构后文本:\n", clean_text)
```

---

## 六、 精确 Skill 集成 (Antigravity / Claude / Cursor)

本项目包含可直接加载的 Agent Skill 规范：
- 技能主文件：[`skills/ai-text-intelligibility/SKILL.md`](skills/ai-text-intelligibility/SKILL.md)
- 将该文件夹复制到您的 Agent 配置目录（例如 `~/.gemini/config/skills/` 或 Cursor Rules）中，即可使 AI 代理在生成技术方案、文档与代码时全面遵守反极端压缩协议。

---

## 七、 单元测试与极限边界防御

本工具集包含完备的自动化测试套件，全面防御 3 类工业级极限边界用例：
1. **零数据/空文本边界**：处理 `""`、空白符、None，系统稳定返回默认基线；
2. **万词级抗溢出边界**：针对长文本（10,000+ 词）执行流式分句分析，时空复杂度严格控制在 $O(N)$；
3. **畸形输入与中英混排防御**：对非常规标点、生僻 Unicode 符号进行严格拦截与清洗。

运行测试命令：
```bash
python -m unittest discover -s tests -v
```
测试输出：
```text
Ran 14 tests in 0.025s
OK
```

---

## 八、 出厂质量控制清单 (OQC)

在交付任何 AI 生成文本与架构文档前，强制对照以下清单检验：
- [x] **[主谓生命度对齐]**：消除无生命主语配合生命动词（promise, bite, swallow, forget 等）。
- [x] **[名词堆叠清零]**：消除 3 个及以上连续名词无介词复合串。
- [x] **[从句引导词补全]**：显式包含 `that` / `which` / `in order to`。
- [x] **[动词规范化]**：无非常规名词活用动词（denominal verbs）。
- [x] **[依存跨度合理]**：核心主谓宾紧凑（符合 DLM 约束）。
- [x] **[信息密度平滑]**：恢复人类交流认知缓冲垫，语流自然。

---

## 九、 学术引用 (Citation)

如果您在学术研究或工程实践中参考了本项目或对应论文，请引用原作者工作：

```bibtex
@article{clark2026why,
  title={Why is AI-generated language so hard to understand?},
  author={Clark, Thomas Hikaru and Martin, Matias B. and Mahowald, Kyle},
  journal={arXiv preprint arXiv:2610.29162},
  year={2026}
}
```

---
**License**: [MIT License](LICENSE) | **Maintainer**: [daybydaymylove-max](https://github.com/daybydaymylove-max)
