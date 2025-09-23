import streamlit as st

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Chinese Verb Network Explorer | 汉语动词网络探索者",
    page_icon="🀄",
    layout="wide"
)

# ----------------------------
# Hero Section
# ----------------------------
st.title("Chinese Verb Network Explorer")
st.title("汉语动词网络探索者", anchor=False) # anchor=False prevents duplicate #chinese-verb-network-explorer

st.markdown("""
**Unlock Mandarin vocabulary through the power of networks.**
**利用网络的力量，解锁汉语词汇。**
""")


# Use a column layout to make the GIF smaller and more integrated
st.markdown("""
<style>
.row { display:flex; align-items:center; gap:.6rem; }
.row img { width:140px; height:auto; border-radius:8px; }
.row .txt p { margin:0 0 .35rem 0; line-height:1.35; }

/* --- Key Notes styles --- */
.notes { display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap:12px; margin: 14px 0 6px; }
.note {
  background:linear-gradient(180deg,#f8fbff,#ffffff);
  border:1px solid #e9eef9;
  border-radius:14px;
  padding:14px 16px;
  box-shadow:0 2px 8px rgba(0,0,0,.04);
}
.note .tag {
  display:inline-flex; align-items:center; gap:.4rem;
  font-size:.85rem; font-weight:700; padding:.2rem .5rem; border-radius:999px;
  background:#e0e7ff; color:#1e3a8a; margin-bottom:.5rem;
}
.note .tag .dot { width:8px; height:8px; border-radius:999px; background:#2563eb; }
.note p { margin:.25rem 0 .35rem; line-height:1.45; }

/* Mobile responsive */
@media (max-width: 900px){
  .notes{ grid-template-columns: 1fr; }
}
</style>
<div class="row">
  <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGU3aW9tMWhrYXF4ZmhmaWI5eXQ2amtlaDV6bnEwaXBnOW4wcmF6aiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKD5CIdlhoQo2Mo/giphy.gif" />
  <div class="txt">
    <p>Stop memorizing vocabulary lists. Start understanding the system.</p>
    <p>This interactive platform uses data science and graph theory to reveal how Chinese verbs are connected, helping you learn smarter, not harder.</p>
    <p>告别死记硬背。开始理解系统。</p>
    <p>这个互动平台利用数据科学和图论，揭示汉语动词之间的联系，帮助您更聪明地学习，而不是更费力。</p>
  </div>
</div>

<!-- === Key Notes / 重要说明 === -->
<div class="notes">
  <div class="note">
    <span class="tag"><span class="dot"></span> Coverage</span>
    <p><strong>953 two-character verbs</strong> out of <strong>1140</strong> total (the rest are single-character) — a big portion of everyday usage.</p>
    <p><strong>在 1140 个动词中，953 个为双字动词</strong>（其余为单字动词），覆盖度高、实用性强。</p>
  </div>
  <div class="note">
    <span class="tag"><span class="dot"></span> Ready to speak</span>
    <p>Verbs are extracted with <strong>third-tone sandhi applied</strong>, so pronunciations are classroom-ready.</p>
    <p>数据已按<strong>三声变调</strong>规则处理，<strong>直接可用于口语教学/练习</strong>。</p>
  </div>
  <div class="note">
    <span class="tag"><span class="dot"></span> Tone labeling</span>
    <p><strong>Neutral tone = 5</strong> in our data (tone pairs are like 3-4, 2-5, etc.).</p>
    <p>本数据中<strong>轻声记作 5</strong>（声调对示例：3-4、2-5 等）。</p>
  </div>
</div>
""", unsafe_allow_html=True)


st.markdown("---") # Horizontal line for separation

# ----------------------------
# Who is it for? (Audience Callout)
# ----------------------------
st.subheader("🗣️ Designed For / 为谁设计")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **👨‍🎓 Students & Self-Learners**
    - Discover the most important characters to learn first.
    - See words as part of a family, not in isolation.
    - Build your vocabulary strategically.
    **👨‍🎓 学生与自学者**
    - 发现应该优先学习的最重要汉字。
    - 在词族中理解单词，而不是孤立记忆。
    - 战略性地构建你的词汇库。
    """)

with col2:
    st.markdown("""
    **👩‍🏫 Teachers & Tutors**
    - Design data-driven lesson plans.
    - Create thematic units based on word families.
    - Show students the "why" behind the vocabulary.
    **👩‍🏫 教师与导师**
    - 设计数据驱动的教学计划。
    - 基于词族创建主题单元。
    - 向学生展示词汇背后的逻辑。
    """)

with col3:
    st.markdown("""
    **👩‍🔬 Researchers & Linguists**
    - Explore the morphological structure of Mandarin.
    - Access a research-grade dataset and analytical tools.
    - Validate linguistic theories with network science.
    **👩‍🔬 研究者与语言学家**
    - 探索汉语的形态结构。
    - 使用研究级数据集和分析工具。
    - 用网络科学验证语言学理论。
    """)

st.markdown("---")

# ----------------------------
# How It Works / Features
# ----------------------------
st.subheader("🔍 How It Works / 功能特点")

feature_desc_en = """
1.  **The Interactive Network (`🌐 Network Graph`)**
    Visualize the hidden connections between verbs. Each character is a node, and each verb is a link. See the core "hub" characters that form the backbone of the language.

2.  **Data-Driven Learning Paths (`📖 Learning Pathways`)**
    Don't guess what to learn next. Our algorithms identify the most powerful "super-connector" characters to learn first for maximum efficiency.

3.  **Discover Thematic Word Families (`🧩 Word Families`)**
    Automatically find clusters of characters that belong together. Learn related vocabulary in context, the way the language is actually structured.
"""

feature_desc_zh = """
1.  **互动网络图 (`🌐 网络图`)**
    可视化动词间的隐藏联系。每个汉字是一个节点，每个动词是一条连接线。一眼看清构成语言核心的“枢纽”汉字。

2.  **数据驱动的学习路径 (`📖 学习路径`)**
    无需猜测下一步该学什么。我们的算法能识别出最应该优先学习的“超级连接字”，实现最高效率的学习。

3. 探索主题词族 (`🧩 词族`)
    自动发现意义上相关的汉字集群。按照语言真实的结构，在语境中学习相关词汇。
"""

st.markdown(feature_desc_en)
st.markdown(feature_desc_zh)

st.markdown("---")

# ----------------------------
# Scientific Basis - MORE CONCISE AND POWERFUL
# ----------------------------
st.subheader("🧪 Built on Research / 科研基础")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    This isn't just another vocabulary app. It's a research platform.

    the app uses **935 of the most common two-character verbs**, extracted from the peer-reviewed:
    - **A Chinese Verb Semantic Feature Dataset (CVFD)** (Springer, 2023)

    The network analysis provides **empirical, data-driven answers** to fundamental questions:
    - "Which characters are the most important?"
    - "How are words semantically connected?"
    - "What is the most efficient path to fluency?"
    """)

with col2:
    st.markdown("""
    这不仅是另一个单词应用。这是一个研究平台。

    APP 分析了 **935 个最常用的双字动词**，这些动词提取自经过同行评审的：
    - **《汉语动词语义特征数据库 (CVFD)》** (Springer, 2023)

    网络分析为一些根本性问题提供了**经验性的、数据驱动的答案**：
    - “哪些汉字最重要？”
    - “词语在语义上是如何连接的？”
    - “实现流利表达的最有效路径是什么？”
    """)

st.markdown("---")

# ----------------------------
# Call to Action & Vision
# ----------------------------
st.subheader("🚀 Start Exploring / 开始探索")

st.markdown("""
**Ready to transform how you learn or teach Chinese?**
**准备好改变你学习或教授汉语的方式了吗？**

Navigate to the **Verb Network Explorer** in the sidebar to begin your discovery.
请使用侧边栏导航到 **动词网络探索者** 开始您的探索。
""")

# Optional: You can add a button that links to the main app page
# st.page_link("pages/1_Verb_Network_Explorer.py", label="Go to the Explorer → / 前往探索平台", icon="🌐")

st.markdown("""
---
**Vision / 愿景**
To move beyond rote memorization and provide a window into the beautiful, logical architecture of the Chinese language.
我们的愿景是超越死记硬背，为您打开一扇窗，窥见汉语优美而逻辑严密的结构。
""")

# ----------------------------
# Support & Contact - Moved to sidebar for better layout
# ----------------------------
with st.sidebar:
    st.header("💝 Support / 支持")
    st.markdown("""
    If this tool helps you, consider supporting its development.
    如果这个工具对您有帮助，请考虑支持它的持续开发。
    """)
    st.markdown("[☕ Buy Me a Coffee / 请我喝杯咖啡](https://buymeacoffee.com/selenophil)")
    st.header("📬 Contact / 联系")
    st.markdown("""
    Feedback? Questions? Collaboration ideas?
    有反馈？问题？合作想法？
    """)
    st.markdown("**📧 aymen.omg@gmail.com**")