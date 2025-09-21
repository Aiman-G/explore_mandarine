import streamlit as st

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Chinese Verb Explorer", layout="wide")

# ----------------------------
# Hero Section
# ----------------------------
st.title("🀄 Chinese Verb Explorer / 汉语动词探索平台")


st.markdown("""
This app is a labor of love and a way of giving back.  
It was created by a researcher who spent many years in China, studied at Chinese universities, and developed a deep fascination with **Chinese history, language, and culture**.  

It brings together tools for **students**, **teachers**, and **curious learners worldwide** to explore the hidden networks of Chinese verbs.
""")
st.markdown("""
这个应用凝聚了作者的心血，也是对中国的一种回馈。  
作者在中国生活多年，并在中国的大学学习，对**中国的历史、语言和文化**产生了深厚的兴趣。  

本平台为**学生**、**教师**以及全球范围内的学习者提供工具，用来探索汉语动词背后隐藏的网络结构。
""")

st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjY3djducnU4amticXowcjVyZjl4MGNwMTEwd2NpN3gwd2szNHZxbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohjUQgIOxqUeq1BLO/giphy.gif")
# ----------------------------
# What You Can Do (Feature Highlights)
# ----------------------------
st.markdown("---")
st.subheader("📖 Explore the App / 功能介绍")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### English
    - **Verb Network** 🕸️: See verbs as a living web of shared characters.  
    - **Verb Analytics** 📊: Study distributions across categories and phonetic components.  
    - **Future Pages** 🚧: More tools for history, etymology, and teaching materials.  

    Each page is designed to make Chinese learning **more visual, structured, and inspiring**.
    """)

with col2:
    st.markdown("""
    #### 中文
    - **动词网络** 🕸️：从汉字联系中观察动词的“网络”。  
    - **动词分析** 📊：研究动词类别分布和语音成分。  
    - **未来页面** 🚧：探索字源、历史层面和教学资源。  

    每个页面都旨在让汉语学习变得**更直观、更系统、更有启发性**。
    """)

# ----------------------------
# Data Source Section
# ----------------------------
st.markdown("---")
st.subheader("📊 Data Source & Scientific Basis / 数据来源与科学基础")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### English  
    This project is based on a trusted and peer-reviewed dataset:  

    - *A Chinese Verb Semantic Feature Dataset (CVFD)*, published in **Springer (Jan 2023)**.  
    - The dataset contains **1,140 Mandarin verbs**, annotated across **11 semantic and cognitive dimensions**.  
    - From this, we focus on the **935 most common two-character verbs** — the natural backbone of modern Chinese.  

    By combining this dataset with **graph theory and NLP techniques**, the app allows learners and teachers to:  
    - Discover **networks and clusters** of verbs.  
    - See how **characters form families of meaning**.  
    - Use scientific insights to **guide vocabulary learning**.  

    This ensures that when we say “common verbs,” they are **research-validated, widely used verbs**, not arbitrary lists.  
    """)

with col2:
    st.markdown("""
    #### 中文  
    本项目基于一个可靠的、经过同行评审的语料库：  

    - **《汉语动词语义特征数据库 (CVFD)》**，发表于 **Springer (2023年1月)**。  
    - 该数据库包含 **1140 个普通话动词**，并从 **11 个语义与认知维度**进行标注。  
    - 在此基础上，本平台聚焦于 **935 个最常见的双字动词** —— 这是现代汉语动词的核心结构。  

    结合 **图论** 与 **自然语言处理 (NLP)** 方法，本平台让学习者和教师能够：  
    - 发现动词之间的 **语义网络与聚类**。  
    - 观察汉字如何构成 **意义家族**。  
    - 借助科学研究成果，**指导词汇学习与教学**。  

    因此，当我们说“常用动词”时，它们不仅常用，而且是 **经过科学验证的常用动词**。  
    """)

# ----------------------------
# Vision
# ----------------------------
st.markdown("---")
st.subheader("🌱 Vision / 愿景")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### English  
    My goal is to create a resource where **Chinese is not just memorized, but understood** —  
    as a network of ideas shaped by history, culture, and sound.  

    With support, I plan to:  
    - Add **bilingual example sentences**.  
    - Explore **historical and etymological layers** of characters.  
    - Offer **curriculum pathways** for students.  
    - Provide **teaching tools** built from the data.  
    """)

with col2:
    st.markdown("""
    #### 中文  
    我的目标是让大家**不仅背汉语，更能理解汉语** ——  
    把它看作一个由历史、文化和语音共同构成的“思想网络”。  

    在支持下，我计划：  
    - 增加**双语例句**。  
    - 深入探索汉字的**历史和字源**。  
    - 为学习者提供**学习路线图**。  
    - 为教师开发**教学工具**。  
    """)

# ----------------------------
# Support & Contact
# ----------------------------
st.markdown("---")
st.subheader("💡 Support & Contact / 支持与联系")

col1, col2 = st.columns([2,1])

with col1:
    st.markdown("""
    **English**  
    If this project resonates with you, you can support it here:  
    [☕ Buy Me a Coffee](https://buymeacoffee.com/selenophil)  

    **中文**  
    如果您觉得这个项目有意义，可以在这里支持：  
    [☕ 请我喝杯咖啡](https://buymeacoffee.com/selenophil)  

    **Contact / 联系方式**  
    📧 aymen.omg@gmail.com  
    """)

# with col2:
#     st.image("https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png", width=180)
