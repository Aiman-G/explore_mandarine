import streamlit as st
import pandas as pd
import plotly.express as px
from utils import page_header, load_data
from pyvis.network import Network
import networkx as nx
import os
import streamlit.components.v1 as components
import json

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(layout="wide")

# ----------------------------
# Translation Strings
# ----------------------------
translations = {
    'en': {
        'page_title': "Character Hub",
        'load_error': "Data could not be loaded. Please ensure the data file is available.",
        'settings_header': "⚙️ Settings",
        'language_select': "Select Language",
        'controls_header': "🔍 Controls",
        'filter_by_class': "Filter by Verb Class",
        'highlight_char': "Select Character to Analyze",
        'no_match_warning': "No data to display for the current selection.",
        'network_header': "Interactive Character Network",
        'network_desc': """
        This graph visualizes how characters form verbs. Use the sidebar to **filter by verb class**.
        - **Nodes:** Single Chinese characters, colored by class.
        - **Edges:** An arrow indicates a verb is formed (e.g., A → B means the verb is 'AB').
        """,
        'generating_network': "Generating network graph...",
        'char_stats_header': "Character Statistics Explorer",
        'select_char_prompt': "Please select a character to see its statistics.",
        'starts_verbs_metric': "Starts Verbs",
        'ends_verbs_metric': "Ends Verbs",
        'total_verbs_metric': "Total Connections",
        'verbs_list_expander': "Show list of verbs containing this character",
        'tab_network': "🌐 Network Graph",
        'tab_pathways': "📖 Learning Pathways",
        'tab_families': "🧩 Word Families",
        'tab_stats': "🔢 Character Statistics",
        'learning_pathways_header': "Data-Driven Learning Pathways",
        'learning_pathways_desc': "Use network science to find the most important characters to learn first. Analysis uses the current class filter.",
        'centrality_expander': "🔑 Most Connected Characters (Degree Centrality)",
        'centrality_desc': "**Why it matters:** These are 'super-connector' characters. Learning them first helps you recognize and form the largest number of verbs quickly.",
        'betweenness_expander': "🌉 Key Bridging Characters (Betweenness Centrality)",
        'betweenness_desc': "**Why it matters:** These characters act as bridges connecting different groups of words (word families). Mastering them helps link different vocabulary sets together.",
        'character_col': "Character",
        'score_col': "Score",
        'in_degree_col': "Ends",
        'out_degree_col': "Starts",
        'families_header': "Word Family Explorer",
        'families_desc': "Using community detection algorithms, we can find clusters of characters that are highly interconnected. Learning these 'word families' together can be an effective strategy.",
        'family_select': "Select a Word Family to Explore",
        'family_members': "Family Members",
        'family_verbs_header': "Verbs within this Family",
        'family_graph_header': "Family Network Graph",
        'family_label': "Family",
    },
    'zh': {
        'page_title': "汉字中心",
        'load_error': "无法加载数据。请确保数据文件可用。",
        'settings_header': "⚙️ 设置",
        'language_select': "选择语言",
        'controls_header': "🔍 控制面板",
        'filter_by_class': "按动词类别筛选",
        'highlight_char': "选择要分析的汉字",
        'no_match_warning': "没有符合当前筛选条件的数据。",
        'network_header': "互动汉字网络",
        'network_desc': """
        此图展示汉字如何构成动词。请使用侧栏按**动词类别**进行筛选。
        - **节点：** 单个汉字，按类别着色。
        - **边：** 箭头表示构成一个动词（例如 A → B 表示“AB”）。
        """,
        'generating_network': "正在生成网络图...",
        'char_stats_header': "汉字统计浏览器",
        'select_char_prompt': "请选择一个汉字以查看其统计数据。",
        'starts_verbs_metric': "作为首字",
        'ends_verbs_metric': "作为尾字",
        'total_verbs_metric': "总连接数",
        'verbs_list_expander': "显示包含此汉字的动词列表",
        'tab_network': "🌐 网络图",
        'tab_pathways': "📖 学习路径",
        'tab_families': "🧩 词族",
        'tab_stats': "🔢 汉字统计",
        'learning_pathways_header': "数据驱动的学习路径",
        'learning_pathways_desc': "利用网络科学找出最重要的汉字，优先学习。分析基于当前的类别筛选。",
        'centrality_expander': "🔑 连接最多的核心字（度中心性）",
        'centrality_desc': "**重要性：** 这些是“超级连接词”。优先学习它们有助于快速识别和构成更多动词。",
        'betweenness_expander': "🌉 关键桥梁字（中介中心性）",
        'betweenness_desc': "**重要性：** 这些汉字如桥梁，连接不同词族。掌握它们有助于把不同词汇集联系在一起。",
        'character_col': "汉字",
        'score_col': "得分",
        'in_degree_col': "作尾字次数",
        'out_degree_col': "作首字次数",
        'families_header': "词族浏览器",
        'families_desc': "通过社群检测算法，我们可以发现内部联系紧密的汉字集群。将这些“词族”一起学习可能是一种有效策略。",
        'family_select': "选择一个词族进行探索",
        'family_members': "词族成员",
        'family_verbs_header': "该词族内的动词",
        'family_graph_header': "词族网络图",
        'family_label': "词族",
    }
}

# ----------------------------
# Caching Functions
# ----------------------------
@st.cache_data
def build_graph(df):
    G = nx.DiGraph()
    for _, row in df.iterrows():
        if pd.notna(row['char1']) and pd.notna(row['char2']):
            G.add_edge(row['char1'], row['char2'], title=f"{row['Verb']} ({row['pinyin']})")
    return G

@st.cache_data
def get_communities(_G):
    G_undirected = _G.to_undirected()
    communities = nx.community.greedy_modularity_communities(G_undirected)
    return sorted([list(c) for c in communities], key=len, reverse=True)

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.header("⚙️ Settings / 设置")
lang_options = {'English': 'en', '中文 (Chinese)': 'zh'}
selected_lang_display = st.sidebar.radio("Select Language / 选择语言", options=lang_options.keys(), horizontal=True)
lang = lang_options[selected_lang_display]
T = translations[lang]

page_header(T['page_title'], "🕸️")

# --- Data Loading and Processing ---
@st.cache_data
def get_df():
    return load_data()
df = get_df()

if df.empty:
    st.error(T['load_error'])
    st.stop()

def parse_bilingual(text):
    if isinstance(text, str) and '(' in text and ')' in text:
        parts = text.split('(')
        zh, en = parts[0], parts[1].replace(')', '')
        return zh.strip(), en.strip()
    return text, text

# Bilingual classification
df[['Classification_zh', 'Classification_en']] = df['分类（Classification）'].apply(lambda x: pd.Series(parse_bilingual(x)))
df.rename(columns={'Chinese_Verbs': 'Verb'}, inplace=True)
classification_col_display = 'Classification_zh' if lang == 'zh' else 'Classification_en'

# --- Sidebar Filters (by class) ---
st.sidebar.header(T['controls_header'])
unique_classes = sorted(df[classification_col_display].dropna().unique())
selected_classes = st.sidebar.multiselect(T['filter_by_class'], options=unique_classes, default=unique_classes)

# Filter data by selected classes
filtered_df = df[df[classification_col_display].isin(selected_classes)].copy()
G = build_graph(filtered_df)

# ----------------------------
# Main Content Tabs
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs([T['tab_network'], T['tab_pathways'], T['tab_families'], T['tab_stats']])

# ----------------------------
# TAB 1 – Network Graph
# ----------------------------
with tab1:
    st.header(T['network_header'])
    st.markdown(T['network_desc'])

    if not filtered_df.empty:
        with st.spinner(T['generating_network']):
            # Compute node sizes from degree on filtered graph
            degrees = dict(G.degree())
            min_degree, max_degree = (1, 1)
            if degrees:
                min_degree = min(degrees.values())
                max_degree = max(degrees.values())

            if max_degree == min_degree:
                normalized_degrees = {node: 15 for node in degrees}
            else:
                normalized_degrees = {
                    node: 10 + 25 * (deg - min_degree) / (max_degree - min_degree)
                    for node, deg in degrees.items()
                }

            net = Network(
                height='750px', width='100%', notebook=False, directed=True,
                cdn_resources='in_line', select_menu=True, filter_menu=True
            )

            # Add nodes, colored/grouped by class (from filtered data, fallback to full df)
            for node, size in normalized_degrees.items():
                # try filtered_df first; if node not present (edge case), fallback to df
                pool = filtered_df if ((filtered_df['char1'] == node) | (filtered_df['char2'] == node)).any() else df
                classification = pool.loc[(pool['char1'] == node) | (pool['char2'] == node), classification_col_display].iloc[0]
                net.add_node(node, label=node, size=size, font={'size': size + 10}, group=classification)

            # Add edges for filtered set
            for _, row in filtered_df.iterrows():
                if row['char1'] and row['char2']:
                    net.add_edge(row['char1'], row['char2'], title=row['Verb'])

            try:
                file_path = 'verb_network.html'
                net.save_graph(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                st.components.v1.html(source_code, height=800)
                os.remove(file_path)
            except Exception as e:
                st.error(f"Error displaying network graph: {e}")
    else:
        st.warning(T['no_match_warning'])

# ----------------------------
# TAB 2 – Learning Pathways
# ----------------------------
with tab2:
    st.header(T['learning_pathways_header'])
    st.markdown(T['learning_pathways_desc'])

    if len(G.nodes) > 1:
        col1, col2 = st.columns(2)
        in_degree = dict(G.in_degree())
        out_degree = dict(G.out_degree())
        
        with col1:
            with st.expander(T['centrality_expander'], expanded=True):
                st.markdown(T['centrality_desc'])
                degree_cent = nx.degree_centrality(G)
                top_degree = sorted(degree_cent.items(), key=lambda x: -x[1])[:10]
                df_degree = pd.DataFrame(top_degree, columns=[T['character_col'], T['score_col']])
                df_degree[T['in_degree_col']] = df_degree[T['character_col']].map(in_degree)
                df_degree[T['out_degree_col']] = df_degree[T['character_col']].map(out_degree)
                df_degree[T['score_col']] = df_degree[T['score_col']].round(3)
                
                fig = px.bar(df_degree, x=T['score_col'], y=T['character_col'], orientation='h', text_auto=True)
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(df_degree, use_container_width=True)

        with col2:
            with st.expander(T['betweenness_expander'], expanded=True):
                st.markdown(T['betweenness_desc'])
                between_cent = nx.betweenness_centrality(G)
                top_between = sorted(between_cent.items(), key=lambda x: -x[1])[:10]
                df_between = pd.DataFrame(top_between, columns=[T['character_col'], T['score_col']])
                df_between[T['in_degree_col']] = df_between[T['character_col']].map(in_degree)
                df_between[T['out_degree_col']] = df_between[T['character_col']].map(out_degree)
                df_between[T['score_col']] = df_between[T['score_col']].round(3)
               
                fig = px.bar(df_between, x=T['score_col'], y=T['character_col'], orientation='h', text_auto=True)
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(df_between, use_container_width=True)
    else:
        st.warning(T['no_match_warning'])

# ----------------------------
# TAB 3 – Word Families
# ----------------------------
with tab3:
    st.header(T['families_header'])
    st.markdown(T['families_desc'])
    
    if len(G.nodes) > 1:
        communities = [c for c in get_communities(G) if len(c) > 2][:20]
        if communities:
            fam_options = {f"{T['family_label']} {i+1} ({len(c)} {T['character_col']}s)": c for i, c in enumerate(communities)}
            selected_fam_label = st.selectbox(T['family_select'], options=fam_options.keys())
            
            if selected_fam_label:
                selected_community = fam_options[selected_fam_label]
                st.info(f"**{T['family_members']}:** {', '.join(selected_community)}")
                
                community_verbs_df = filtered_df[filtered_df['char1'].isin(selected_community) & filtered_df['char2'].isin(selected_community)]
                
                st.subheader(T['family_graph_header'])
                if not community_verbs_df.empty:
                    C_graph = build_graph(community_verbs_df)
                    net_fam = Network(height='700px', width='100%', notebook=False, directed=True, cdn_resources='in_line')
                    for node in C_graph.nodes():
                        net_fam.add_node(node, label=node, size=10 + 3*C_graph.degree(node), font={'size': 18})
                    for edge in C_graph.edges(data=True):
                        net_fam.add_edge(edge[0], edge[1], title=edge[2]['title'])
                    
                    try:
                        file_path_fam = 'family_network.html'
                        net_fam.save_graph(file_path_fam)
                        with open(file_path_fam, 'r', encoding='utf-8') as f:
                            source_code_fam = f.read()
                        components.html(source_code_fam, height=550)
                        if os.path.exists(file_path_fam):
                            os.remove(file_path_fam)
                    except Exception as e:
                        st.error(f"Error displaying graph: {e}")
                
                st.subheader(T['family_verbs_header'])
                st.dataframe(community_verbs_df[['Verb', 'pinyin', 'English_Verb', classification_col_display]], use_container_width=True)
        else:
            st.warning(T['no_match_warning'])
    else:
        st.warning(T['no_match_warning'])

# ----------------------------
# TAB 4 – Character Statistics
# ----------------------------
with tab4:
    st.header(T['char_stats_header'])
    
    all_chars = sorted(list(G.nodes()))
    selected_char = st.selectbox(T['highlight_char'], options=[''] + all_chars)

    if selected_char and selected_char in G:
        st.subheader(f"'{selected_char}'")
        col1, col2, col3 = st.columns(3)
        col1.metric(T['starts_verbs_metric'], G.out_degree(selected_char))
        col2.metric(T['ends_verbs_metric'], G.in_degree(selected_char))
        col3.metric(T['total_verbs_metric'], G.degree(selected_char))
        
        with st.expander(T['verbs_list_expander']):
            st.dataframe(
                filtered_df[
                    (filtered_df['char1'] == selected_char) | (filtered_df['char2'] == selected_char)
                ][['Verb', 'pinyin', 'English_Verb', classification_col_display]].drop_duplicates(),
                use_container_width=True
            )
    else:
        st.info(T['select_char_prompt'])
