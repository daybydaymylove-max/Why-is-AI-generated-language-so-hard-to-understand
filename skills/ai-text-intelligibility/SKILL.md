---
name: ai-text-intelligibility
description: 心理语言学对齐与反极端压缩工程技能（Psycholinguistic Alignment & Anti-Compression Protocol）。基于前沿论文 arXiv:2610.29162v1，系统性阻断大语言模型在后训练（RLVR/GRPO/长度惩罚）中异化生成的 6 类高认知负荷病态语言特征，将 AI 文本重构为符合人类工作记忆容量（DLT）与统一信息密度（UID）的高可理解性工业级文本。
---

# 人类语言可理解性与反极端压缩工程规范 (Psycholinguistic Intelligibility & Anti-Compression Engineering Protocol)

本技能基于认知心理语言学与前沿大模型后训练实证研究（arXiv:2610.29162v1: *Why is AI-generated language so hard to understand?*），是指导所有 AI 生成文本、技术报告、架构文档与人机协作交付物的易读性质量规范。

---

## 1. 物理病因与理论对齐基线 (Etiological Background & Theoretical Foundations)

### 1.1 人类语言进化的生物物理约束
- **有限工作记忆容量 (Lossy Working Memory)**：人脑在阅读时依赖递增式在线解析（Incremental Online Processing）。根据**依存局部性理论 (Dependency Locality Theory, DLT; Gibson 1998/2000)**，长距离句法依赖会急剧消耗工作记忆，引发理解延迟与认知中断。
- **统一信息密度假设 (Uniform Information Density, UID; Levy & Jaeger 2007)**：人类自然交流在传输通道上保持相对平稳的信息传输速率。说话者会自发在信息量大或难预测处增加语法标记（如补全关系代词 `that`）、提供认知缓冲词；在信息量低处做适度压缩。
- **交流成功率优化 (Optimization for Communicative Success)**：人类语言演化的目标是在“发话成本”与“受话理解成本”之间取得帕累托最优平衡。

### 1.2 大模型后训练的目标异化与病理压缩
- **解耦交流压力的强化学习 (RLVR / GRPO Decoupling)**：在前沿模型后训练（如代码生成、数学推理与沙盒任务）中，引入了可验证奖励（RLVR）与长度惩罚（Length Penalty, $\lambda > 0$）。模型的目标被极化为：**在有限 Token 预算与长上下文开销下，仅优化答案正确性，彻底脱离人类理解反馈**。
- **病态信息密度的泛化迁移**：实验证明，微小的长度惩罚会迫使模型在句法交替（Syntactic Alternations）中以接近 100% 的极值倒向短变体，并产生向未知句式的近迁移与远迁移。
- **语法合法但超出认知分布 (Grammatically Valid but OOD for Human Cognition)**：模型生成的文本虽然符合句法规则，但在统计分布上严重偏离自然语言，充斥着极端压缩的短构式，造成人类读者的严重认知过载（Cognitive Overload）。

---

## 2. 六大病态语言特征检测红线与绝对禁令 (The 6 Pathological Features Redline)

所有文本生成与代码注释输出，必须严格排查并杜绝以下 6 类被证实击穿人类认知预算的特征：

| 编号 | 病态语言学特征 (Feature) | 认知损伤机理 (Cognitive Impact) | 典型违规样例 (Paper Table 2) | 标准重构模式 (Remediation) |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **无生命主语配合生命动词**<br>*(Inanimate Subject + Animate Verb)* | 违背选择限制（Selectional Restriction），破坏人脑生命度解析线索，诱发 **P600 冲突重构电位**。 | `"The docstring promises they are skipped..."`<br>`"...asymmetry bites."` | 解耦为客观状态陈述：<br>`"According to the docstring, they are skipped..."`<br>`"...asymmetry causes an error."` |
| **02** | **连续名词三连堆叠**<br>*(Stacked Noun Compounds $\ge 3$)* | 触发**括号歧义 (Bracketing Ambiguity)** 与层级解析断层，读者无法即时判定修饰层级与核心词。 | `"dotfile backup path handling"`<br>`"reader-patience budget"` | 引入介词短语拆解层级：<br>`"handling paths for dotfile backups"`<br>`"the patient attention of readers"` |
| **03** | **切除关系词的缩略宾从**<br>*(Reduced Object Relative Clause)* | 强制省略 `that`/`which` 诱发**花园路径效应 (Garden-Path Effect)**，造成语序逆转时的瞬间阅读停顿。 | `"...leave the job you hate money."`<br>`"...activities they care about."` | 强制显式补齐关系引导词：<br>`"...the job that you hate..."`<br>`"...activities that they care about."` |
| **04** | **临时活化名词为动词**<br>*(Ad-hoc Denominal Verbs)* | 迫使受话者在心理词库中执行非常规**词性重构 (Syntactic Re-evaluation)**，打断心流。 | `"footnote it."`<br>`"Austin cushions price spikes."` | 替换为规范动宾短语：<br>`"Add a footnote to explain it."`<br>`"Austin mitigates price spikes."` |
| **05** | **超长句法依存跨度**<br>*(Long Dependency Length)* | 主谓、动宾跨越超长修饰成分，击穿人脑**工作记忆缓冲上限**。 | `"The guitar sitting in the corner because you are still deciding teaches you zero chords."` | 遵循依存局部性（DLM），拆分为逻辑连贯的短复合句。 |
| **06** | **罕见 N-gram 与高困惑度搭配**<br>*(Unattested N-grams & High Trigram PPL)* | 激进跳过人类交流依赖的高频可预测过渡词，制造生硬、突兀的非常规双词/三词拼贴。 | 制造非常规术语搭配以省 Token。 | 恢复人类自然的语言惯用搭配与认知过渡垫片。 |

---

## 3. 人类认知对齐的四步解耦重构流水线 (The 4-Step Decoupling Protocol)

当检测到高认知负荷文本时，必须无条件执行以下四步解耦流水线进行物理重构：

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

### 3.1 第一步：名词堆叠解耦规程 (Noun De-stacking)
- 扫描任何由 3 个及以上连续实义词构成的复合修饰组；
- 提取右侧核心名词（Head Noun），将其余修饰成分依照从属逻辑重构为带前置介词的修饰语。
- *反例*：`"class-time shutdown requirement"`
- *正例*：`"the requirement to shut down devices during class time"`

### 3.2 第二步：主体生命度还原规程 (Animacy Realignment)
- 严禁让代码、文档、配置、算法“承诺 (promise)”、“吃掉 (swallow/eat)”、“咬住 (bite)”、“忘记 (forget)”、“希望 (hope)”；
- 还原真实动作发起者，或采用客观指示动词（`indicates`, `specifies`, `results in`, `triggers`）。
- *反例*：`"The test suite hates unmocked external requests."`
- *正例*：`"The test suite fails when external requests are not mocked."`

### 3.3 第三步：补齐认知冗余算子 (Cognitive Buffer Restoration)
- 坚决抵制大模型在 RL 中学到的“节约 Token 捷径”；
- 在宾语从句、定语从句中，一律显式包含连接词 `that` 或 `which`；
- 在因果或目的表述中，显式保留引导短语（如 `so that`, `in order to`），避免读者在递增解析时误判为主句核心宾语。

### 3.4 第四步：依存跨度压缩 (Dependency Length Minimization)
- 严格遵循 DLM 定律：核心谓语动词与其主语、直接宾语之间的线型词距原则上不超过 4 个词；
- 若主语带有冗长从句或介词短语，应优先采用**先行词前置**、**分裂句**或**主动句拆分**。

---

## 4. 实战对比重构案例库 (Contrastive Benchmark Corpus)

### 案例 1：代码审查与沙盒技术报告 (Coding Sandbox Context)
- **AI 极限压缩病态原句 (Frontier LLM Output)**:
  > `"The docstring promises they're skipped when they appear anywhere in the source_dir path, but the dotfile backup path handling forgot dotfolder handling."`
- **病态特征剖析**:
  - `docstring promises`: 无生命主语配合生命动词（选择限制冲突，P600）；
  - `dotfile backup path handling`: 四连名词堆叠（括号歧义）；
  - `forgot dotfolder handling`: 拟人化动词 + 复合词堆叠。
- **工业级认知重构 (Human-Intelligible Rewrite)**:
  > `"According to the docstring, items located anywhere within the source directory should be skipped. However, the routine that processes backup paths for dotfiles failed to account for dot-prefixed directories."`

### 案例 2：技术建议与日常工程沟通 (Chat / Advice Context)
- **AI 极限压缩病态原句 (Frontier LLM Output)**:
  > `"Your convoluted implementation is quietly eating your team-patience budget footnote it before deployment."`
- **病态特征剖析**:
  - `eating your team-patience budget`: 拟人化隐喻 + 三连名词堆叠；
  - `footnote it`: 临时名词活化为动词（Denominal Verb）；
  - 缺乏标点与逻辑从属连接词。
- **工业级认知重构 (Human-Intelligible Rewrite)**:
  > `"This complex implementation risks exhausting your team's patience. Please add explanatory documentation before deploying it."`

### 案例 3：学术分析与论述文 (Essay / Persuasive Context)
- **AI 极限压缩病态原句 (Frontier LLM Output)**:
  > `"Second, the time objection misunderstands how the community service honor cord requirement functions in practice."`
- **病态特征剖析**:
  - `time objection misunderstands`: 抽象概念拟人化配合主观认知动词；
  - `community service honor cord requirement`: 五连名词极限堆叠。
- **工业级认知重构 (Human-Intelligible Rewrite)**:
  > `"Second, opponents who raise concerns about time fail to understand how the graduation honor cord requirement for community service operates in practice."`

---

## 5. 出厂易读性终检清单 (Outgoing Quality Control - OQC)

在交付任何文档、代码注释、设计架构或解释性回复前，强制对照以下清单进行排查：

- [ ] **[无生命拟人清零]**：文本中无将代码、文档、抽象概念作为行为主体并施加拟人化动词（promise, bite, swallow, forget 等）的现象。
- [ ] **[名词堆叠清零]**：不存在 3 个及以上连续实义名词无介词连接的复合串。
- [ ] **[引导词补全]**：所有从句与逻辑从属结构均包含完整的引导词（`that`, `which`, `in order to`），无突兀的省略。
- [ ] **[动词规范性]**：无生僻/自造的名词活用动词（denominal verbs），动宾结构语义明晰。
- [ ] **[依存跨度合理]**：核心主谓宾距离紧凑，单句无超长修饰造成的跨度断层（DLM 合规）。
- [ ] **[信息密度平滑]**：语言表述具备合理的认知缓冲垫，语流符合人类自然交流节奏，严禁因追求简短而制造高负荷黑话。

---

## 6. 自动化审查脚手架集成 (Tooling & Verification)

本技能配套提供开箱即用的自动化检测与评分脚本，位于：
`scripts/audit_intelligibility.py`

### 快速执行命令：
```powershell
python scripts/audit_intelligibility.py
```
该脚手架能够自动化解析待测文本，定位名词堆叠、生命度错配、名词动化与省略从句，并给出标准评分与重构建议。
