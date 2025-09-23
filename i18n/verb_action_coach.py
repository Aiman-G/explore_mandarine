
TRANSLATIONS = {
    "en": {
        "title": "Verb Action Coach",
        "load_error": "Data could not be loaded. Please ensure the data file is available.",
        "settings": "⚙️ Settings",
        "lang": "Select Language",
        "tab_overview": "📊 Overview",
        "tab_heatmap": "🗺️ Tone Heatmap",
        "tab_coverage": "🎯 Coverage Optimizer",
        "tab_deck": "🗂️ Deck Builder",
        "tab_pitfalls": "🚩 Polyphony & Pitfalls",

        # OVERVIEW
        "ov_help_title": "What is this? How to use it",
        "ov_help_body": """
**Overview** summarizes the dataset to guide lesson planning.

- **Category distribution** shows which verb categories dominate.
- **Phonetic breakdown** reveals common initials/finals for 1st vs 2nd characters.

**How to use**
1) Pick 1–2 categories to focus on this week.
2) Note the frequent initials/finals and plan pronunciation drills to match.
""",
        "cat_dist": "Verb Category Distribution",
        "cat_desc": "Counts of verbs in each functional category.",
        "category": "Category",
        "verb_count": "Number of Verbs",
        "phon_header": "Phonetic Component Analysis (Initials & Finals)",
        "phon_desc": "Most frequent initials (声母) and finals (韵母) for the first and second characters.",
        "initial_1": "First Character — Initial",
        "final_1": "First Character — Final",
        "initial_2": "Second Character — Initial",
        "final_2": "Second Character — Final",
        "frequency": "Frequency",
        "component": "Phonetic Component",

        # HEATMAP
        "hm_help_title": "What is this? How to use it",
        "hm_help_body": """
**Tone Heatmap** shows source→destination tone transitions (1–5) as a 5×5 matrix.

**How to use**
1) Select **All** or a specific category to inspect.
2) Identify the **dominant tone pair(s)** (e.g., 3→4).
3) Design drills around those transitions and collect examples from the dataset.
""",
        "hm_header": "Tone-Pair Heatmap by Category",
        "hm_cat": "Category",
        "hm_all": "All",

        # COVERAGE
        "cov_help_title": "What is this? How to use it",
        "cov_help_body": """
**Coverage Optimizer** picks a small set of characters that covers the most verbs (greedy set cover).

**How to use**
1) Choose **how many characters** you can teach soon.
2) The optimizer lists the **best characters** and shows **coverage%** of verbs.
3) Use the covered verbs table as a quick teaching deck.
""",
        "cov_header": "Coverage Optimizer",
        "cov_caption": "Pick a small set of characters that covers the most verbs.",
        "cov_how_many": "How many characters?",
        "cov_selected": "Selected chars",
        "cov_list_prefix": "Selected:",
        "cov_coverage": "Coverage",
        "cov_verbs_covered": "Verbs covered",
        "cov_download": "Download covered verbs (CSV)",

        # DECK
        "deck_help_title": "What is this? How to use it",
        "deck_help_body": """
**Deck Builder** turns filters (tone pairs, initials/finals) into a study deck.

**How to use**
1) Choose **tone pairs** and (optionally) **phonetic components**.
2) Set **deck size** and generate.
3) Export to CSV for Anki or handouts.
""",
        "deck_header": "Pronunciation / Deck Builder",
        "deck_tone_pairs": "Tone pairs",
        "deck_position": "Position",
        "deck_any": "Any",
        "deck_first_init": "1st: initial",
        "deck_first_final": "1st: final",
        "deck_second_init": "2nd: initial",
        "deck_second_final": "2nd: final",
        "deck_components": "Components",
        "deck_size": "Deck size",
        "deck_no_items": "No items under current filters.",
        "deck_download": "Download deck (CSV)",

        # PITFALLS
        "pit_help_title": "What is this? How to use it",
        "pit_help_body": """
**Polyphony & Pitfalls** surfaces characters with many tone roles and 3→3 items (sandhi talking points).

**How to use**
1) Pre-teach the **polyphonic** characters (many tone roles).
2) Show learners the **3→3** list and remind them of third-tone sandhi (speak as 2+3).
""",
        "pit_header": "Polyphony & Pitfalls",
        "pit_poly_caption": "Characters with many tone roles (watch for confusion)",
        "pit_sandhi_caption": "3→3 (underlying) — remember 2+3 in speech",
        "no_data": "No data available."
    },

    "zh": {
        "title": "动词教学助理",
        "load_error": "无法加载数据。请确保数据文件可用。",
        "settings": "⚙️ 设置",
        "lang": "选择语言",
        "tab_overview": "📊 概览",
        "tab_heatmap": "🗺️ 声调热图",
        "tab_coverage": "🎯 覆盖率优化",
        "tab_deck": "🗂️ 清单生成",
        "tab_pitfalls": "🚩 多音与易错",

        # OVERVIEW
        "ov_help_title": "这是做什么的？如何使用",
        "ov_help_body": """
**概览** 帮你快速了解数据，指导备课。

- **类别分布**：哪些动词类别占比高。
- **语音成分**：第一/第二字常见的声母与韵母。

**使用建议**
1）选定本周重点的 1–2 个类别；
2）根据常见声母/韵母设计对应的发音训练。
""",
        "cat_dist": "动词类别分布",
        "cat_desc": "各功能类别中的动词数量。",
        "category": "类别",
        "verb_count": "动词数量",
        "phon_header": "语音成分分析（声母/韵母）",
        "phon_desc": "第一、第二字最常见的声母（shēngmǔ）和韵母（yùnmǔ）。",
        "initial_1": "第一字 — 声母",
        "final_1": "第一字 — 韵母",
        "initial_2": "第二字 — 声母",
        "final_2": "第二字 — 韵母",
        "frequency": "频率",
        "component": "语音成分",

        # HEATMAP
        "hm_help_title": "这是做什么的？如何使用",
        "hm_help_body": """
**声调热图** 展示首→尾的声调转移（1–5）5×5 矩阵。

**使用建议**
1）选择 **全部** 或某个类别；
2）找出 **主要声调模式**（如 3→4）；
3）围绕它设计训练并从数据中收集例词。
""",
        "hm_header": "按类别的声调转移热图",
        "hm_cat": "类别",
        "hm_all": "全部",

        # COVERAGE
        "cov_help_title": "这是做什么的？如何使用",
        "cov_help_body": """
**覆盖率优化器** 用少量汉字覆盖尽可能多的动词（贪心集合覆盖）。

**使用建议**
1）选择你近期可教学的 **汉字数量**；
2）查看推荐的 **最优汉字** 及 **覆盖率**；
3）使用被覆盖的动词表作为快速教学清单。
""",
        "cov_header": "覆盖率优化器",
        "cov_caption": "选择少量汉字覆盖尽可能多的动词。",
        "cov_how_many": "选择多少个汉字？",
        "cov_selected": "已选汉字数",
        "cov_list_prefix": "已选：",
        "cov_coverage": "覆盖率",
        "cov_verbs_covered": "覆盖的动词数量",
        "cov_download": "下载覆盖动词（CSV）",

        # DECK
        "deck_help_title": "这是做什么的？如何使用",
        "deck_help_body": """
**清单生成器** 将筛选条件（声调、声母/韵母）变成学习清单。

**使用建议**
1）选择 **声调模式** 与（可选）**语音成分**；
2）设定 **清单大小** 并生成；
3）导出 CSV 用于 Anki 或讲义。
""",
        "deck_header": "发音/清单生成器",
        "deck_tone_pairs": "声调模式",
        "deck_position": "位置",
        "deck_any": "任意",
        "deck_first_init": "第一字：声母",
        "deck_first_final": "第一字：韵母",
        "deck_second_init": "第二字：声母",
        "deck_second_final": "第二字：韵母",
        "deck_components": "成分",
        "deck_size": "清单大小",
        "deck_no_items": "当前筛选无结果。",
        "deck_download": "下载清单（CSV）",

        # PITFALLS
        "pit_help_title": "这是做什么的？如何使用",
        "pit_help_body": """
**多音与易错**：找出声调角色多的汉字，以及 3→3 词（讲解三声变调）。

**使用建议**
1）预先讲解 **多音多角色** 的汉字；
2）展示 **3→3** 列表，提醒口语常读为 2+3。
""",
        "pit_header": "多音与易错点",
        "pit_poly_caption": "声调角色多的汉字（易混）",
        "pit_sandhi_caption": "3→3（底层）— 口语一般读作 2+3",
        "no_data": "没有可用数据。"
    }
}


