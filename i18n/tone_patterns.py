TRANSLATIONS = {
    'en': {
        'page_title': "Tone Explorer",
        'load_error': "Data could not be loaded. Please ensure the data file is available.",
        'settings_header': "⚙️ Settings",
        'language_select': "Select Language",
        'controls_header': "🔍 Filters",
        'filter_by_tonepair': "Tone Pair (src→dst)",
        'filter_src_tone': "Source Tone",
        'filter_dst_tone': "Destination Tone",
        'filter_class': "Classification",
        'legend_header': "Tone Legend",
        'tab_network': "🌐 Tone Network",
        'tab_pathways': "🧭 Tone Pathways",
        'tab_families': "🗂️ Tone in Families",
        'tab_minpairs': "🧪 Minimal Tone-Contrast Sets",
        'tab_charprof': "👤 Character Tone Profiles",
        'tab_curriculum': "📚 Curriculum Builder",
        'no_match_warning': "No data to display for the current selection.",
        'generating_network': "Generating network graph...",
        'fade_unselected': "Fade unselected tones (instead of hiding)",
        'network_desc': """
        Explore the character network through tone patterns.
        - **Nodes:** Characters (size by degree).
        - **Edges:** Verbs (A→B means 'AB'), **colored by tone pair (src→dst)**, thickness by frequency.
        Use the filters to focus on specific tone transitions.
        """,
        'path_target_pair': "Target Tone Pair",
        'path_start_char': "Start Character",
        'path_len': "Path length",
        'path_make': "Make Path",
        'path_desc': "Build a short learning route that prefers edges matching the chosen tone pair.",
        'verbs_on_path': "Verbs on this Path",
        'download_csv': "Download CSV",
        'families_header': "Word Family Explorer (with tone)",
        'families_desc': "Select a community to inspect its tone distribution. Edges are colored by tone pair.",
        'family_select': "Select a Family",
        'family_members': "Family Members",
        'tone_distribution': "Tone-Pair Distribution (this family)",
        'minpairs_header': "Minimal Tone-Contrast Sets",
        'minpairs_desc': "Find sets where **letters are the same** (pinyin without tone digits), but **tones differ**.",
        'minpairs_contrast': "Contrast focus",
        'contrast_any': "Any tone difference",
        'contrast_src': "Different source tone (first syllable)",
        'contrast_dst': "Different destination tone (second syllable)",
        'minpairs_make': "Find Minimal Pairs",
        'charprof_select': "Select Character",
        'charprof_desc': "Tone distribution for this character and all its verbs.",
        'src_count': "As first char",
        'dst_count': "As second char",
        'tone_profile': "Tone Profile",
        'quick_show': "Quick filters",
        'show_src_to_any': "Show X→* verbs",
        'show_any_to_dst': "Show *→X verbs",
        'curriculum_desc': "Build a tone-focused deck from the current filters.",
        'deck_size': "Deck size",
        'deck_pairs': "Select tone pairs to include",
        'weighting': "Selection weighting",
        'weight_degree': "Favor high-degree characters",
        'weight_uniform': "Uniform",
        'make_deck': "Build Deck",
        'deck_table': "Deck Preview",

        # NEW: Help expanders (titles + content)
        'help_network_title': "What is this? How to use it",
        'help_network_body': """
**This tab shows the whole character graph through tone.**  
- Use the **Filters** on the left to narrow by **tone pair**, **source/destination tone**, and **classification**.  
- **Node size** reflects how many connections a character has (degree).  
- **Edge color** = tone pair; **thickness** ≈ frequency.  
- **Fade unselected tones** to keep context while focusing your target.  
**How to use:**  
1) Start broad, then filter to one or two tone pairs (e.g., **3→4**).  
2) Hover edges to see **verb · pinyin · English**.  
3) Screenshot a subgraph for class slides, or note high-degree nodes for practice.  
**Tip:** Use the network to pick 1–3 **“hub” characters** to study deeply before drills.
""",

        'help_pathways_title': "What is this? How to use it",
        'help_pathways_body': """
**This tab builds a short learning route through the graph** that prefers your chosen **tone pair**.  
- Choose a **Target Tone Pair**, a **Start Character**, and a **Path length**.  
- We score edges that match the target tone pair higher and prefer well-connected next steps.  
**How to use:**  
1) Pick a **start** you already know.  
2) Choose a **tone pair** you want to train.  
3) Generate a route → study the **verbs on the path**; export as CSV for spaced practice.  
**Tip:** If the path is short, try another start character or relax filters.
""",

        'help_families_title': "What is this? How to use it",
        'help_families_body': """
**Communities (“families”) are clusters of characters that interconnect densely.**  
- Select a **family** to see its **tone-pair distribution** and an **intra-family graph**.  
**How to use:**  
1) Pick a family, skim the **top tone pairs** in the bar chart.  
2) Explore the mini network; hover edges for examples.  
3) Use this to build a **coherent practice set** within one semantic/morphological neighborhood.
""",

        'help_minpairs_title': "What is this? How to use it",
        'help_minpairs_body': """
**Minimal tone-contrast sets** share the same **pinyin letters** (digits removed) but have **different tones**.  
- Choose a contrast focus (any difference / different source tone / different destination tone).  
**How to use:**  
1) Generate pairs → use them for **listening** or **production** drills.  
2) Export CSV for a quick in-class worksheet.  
**Tip:** Great for spotlighting **2 vs 3** and **third-tone sandhi** contexts.
""",

        'help_charprof_title': "What is this? How to use it",
        'help_charprof_body': """
**Character tone profile** shows how one character appears across tones and which verbs it forms.  
- Bar chart = how often this char carries each tone (as first/second).  
- Tables list all verbs when it’s **first** (A→•) or **second** (•→B).  
**How to use:**  
1) Pick a character you’re learning.  
2) Review its common partners and tones.  
3) Use **Quick filters** to focus e.g. **3→*** or ***→4** sets for targeted practice.
""",

        'help_curriculum_title': "What is this? How to use it",
        'help_curriculum_body': """
**Build a tone-focused deck** from your current filters.  
- Choose tone pairs and **deck size**; pick weighting (**Uniform** or **Favor high-degree characters**).  
**How to use:**  
1) Set filters on the left (topic/tones).  
2) Generate a deck and **export CSV** (Anki-friendly).  
**Tip:** Favoring high-degree nodes gives broad coverage quickly; Uniform keeps variety.
""",
    },

    'zh': {
        'page_title': "声调探索",
        'load_error': "无法加载数据。请确保数据文件可用。",
        'settings_header': "⚙️ 设置",
        'language_select': "选择语言",
        'controls_header': "🔍 筛选",
        'filter_by_tonepair': "声调模式（首→尾）",
        'filter_src_tone': "首字声调",
        'filter_dst_tone': "尾字声调",
        'filter_class': "动词类别",
        'legend_header': "声调图例",
        'tab_network': "🌐 声调网络图",
        'tab_pathways': "🧭 学习路径",
        'tab_families': "🗂️ 词族中的声调",
        'tab_minpairs': "🧪 最小对立组",
        'tab_charprof': "👤 汉字声调画像",
        'tab_curriculum': "📚 课程生成器",
        'no_match_warning': "没有符合当前筛选条件的数据。",
        'generating_network': "正在生成网络图...",
        'fade_unselected': "将未选声调淡化显示（不隐藏）",
        'network_desc': """
        从声调视角探索汉字网络。
        - **节点：** 汉字（大小=度数）。
        - **边：** 动词（A→B 表示“AB”），**按声调模式着色**，粗细与出现频次相关。
        使用筛选器来聚焦某些声调转移。
        """,
        'path_target_pair': "目标声调模式",
        'path_start_char': "起始汉字",
        'path_len': "路径长度",
        'path_make': "生成路径",
        'path_desc': "优先经过所选声调模式的边，构成一条短学习路线。",
        'verbs_on_path': "路径上的动词",
        'download_csv': "下载 CSV",
        'families_header': "词族浏览（含声调）",
        'families_desc': "选择一个社群，查看其声调分布。边按声调模式着色。",
        'family_select': "选择词族",
        'family_members': "词族成员",
        'tone_distribution': "该词族的声调分布",
        'minpairs_header': "最小对立组",
        'minpairs_desc': "查找 **字母相同**（拼音去掉声调数字），但**声调不同**的词组。",
        'minpairs_contrast': "对比焦点",
        'contrast_any': "任意声调差异",
        'contrast_src': "首字声调不同",
        'contrast_dst': "尾字声调不同",
        'minpairs_make': "查找对立组",
        'charprof_select': "选择汉字",
        'charprof_desc': "该汉字的声调分布及其所有相关动词。",
        'src_count': "作首字次数",
        'dst_count': "作尾字次数",
        'tone_profile': "声调画像",
        'quick_show': "快速筛选",
        'show_src_to_any': "显示 X→* 动词",
        'show_any_to_dst': "显示 *→X 动词",
        'curriculum_desc': "基于当前筛选构建声调训练清单。",
        'deck_size': "清单大小",
        'deck_pairs': "选择包含的声调模式",
        'weighting': "选择权重",
        'weight_degree': "倾向高连接度汉字",
        'weight_uniform': "均匀",
        'make_deck': "生成清单",
        'deck_table': "预览清单",

        # NEW: Help expanders (titles + content)
        'help_network_title': "这是做什么的？如何使用",
        'help_network_body': """
**本页以“声调”为视角展示整张汉字网络。**  
- 左侧 **筛选** 可按 **声调模式**、**首/尾字声调**、**类别** 精准聚焦。  
- **节点大小** 代表连接多少（度数）；**边颜色** 表示声调模式；**粗细** 约等于频次。  
- 选择“**淡化未选声调**”可在保留全貌的同时突出重点。  
**使用建议：**  
1）先整体浏览，再缩小到 1–2 个重点声调（如 **3→4**）。  
2）将鼠标悬停查看 **动词·拼音·释义**。  
3）记录几个 **高连接度** 的汉字，作为后续练习的“枢纽”。  
""",

        'help_pathways_title': "这是做什么的？如何使用",
        'help_pathways_body': """
**本页根据你的“目标声调模式”生成一条短学习路径。**  
- 选择 **目标声调**、**起始汉字** 和 **路径长度**。  
- 算法优先经过匹配该声调模式的边，并倾向连接度更高的下一步。  
**使用建议：**  
1）挑选你熟悉的起始字；  
2）选择想训练的声调模式；  
3）生成路径 → 学习路径中的动词，并导出 CSV 复习。  
提示：路径过短可更换起点或放宽筛选。
""",

        'help_families_title': "这是做什么的？如何使用",
        'help_families_body': """
**“词族/社群”是网络里彼此紧密相连的汉字群。**  
- 选择一个词族查看其 **声调分布** 和 **内部网络图**。  
**使用建议：**  
1）先看柱状图里最常见的声调模式；  
2）在小网络中悬停查看例词；  
3）据此在同一语义/构词邻域内，构建一组连贯的练习清单。
""",

        'help_minpairs_title': "这是做什么的？如何使用",
        'help_minpairs_body': """
**“最小对立”** 指 **拼音字母相同**（去掉声调数字），但 **声调不同** 的词组。  
- 选择对比焦点（任意差异/首字不同/尾字不同）。  
**使用建议：**  
1）生成对立组 → 做 **听辨** 或 **跟读** 训练；  
2）导出 CSV 制作课堂练习。  
提示：特别适合练 **二声 vs 三声** 及 **三声变调** 场景。
""",

        'help_charprof_title': "这是做什么的？如何使用",
        'help_charprof_body': """
**“汉字声调画像”** 展示某个汉字在不同声调下的出现频次及其常见搭配。  
- 柱状图显示该字各声调的出现次数；  
- 下方表格列出其作为 **首字** 与 **尾字** 的全部动词。  
**使用建议：**  
1）选择你在学的汉字；  
2）查看常见搭配与声调；  
3）用“快速筛选”生成如 **3→*** 或 ***→4** 的针对性练习集。
""",

        'help_curriculum_title': "这是做什么的？如何使用",
        'help_curriculum_body': """
**从当前筛选构建一套“声调训练清单”。**  
- 选择声调模式与 **清单大小**，并设定权重（**倾向高连接度** / **均匀**）。  
**使用建议：**  
1）先在左侧设定主题/声调；  
2）生成清单并 **导出 CSV**（兼容 Anki）。  
提示：倾向高连接度 → 覆盖面更广；均匀 → 多样性更好。
""",
    }
}
