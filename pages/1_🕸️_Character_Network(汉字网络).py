import streamlit as st
import pandas as pd
import plotly.express as px
from utils import page_header, load_data
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

try:
    from utils import language_selector
except ImportError:
    def language_selector(
        header: str = "⚙️ Settings / 设置",
        label: str = "Select Language / 选择语言",
    ):
        lang_options = {"English": "en", "中文 (Chinese)": "zh"}
        display_by_code = {code: text for text, code in lang_options.items()}
        state_key = "app_language"
        widget_key = "_app_language_widget"

        if state_key not in st.session_state:
            st.session_state[state_key] = "en"
        st.session_state[widget_key] = display_by_code.get(st.session_state[state_key], "English")

        def sync_language():
            selected = st.session_state.get(widget_key, "English")
            st.session_state[state_key] = lang_options.get(selected, "en")

        st.sidebar.header(header)
        st.sidebar.radio(label, options=list(lang_options.keys()), key=widget_key, horizontal=True, on_change=sync_language)
        sync_language()
        return st.session_state[state_key]

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
        This graph shows how single characters combine into two-character verbs. Use the sidebar to **filter by verb class**.
        - **Nodes:** Single Chinese characters. Larger nodes connect to more verbs.
        - **Edges:** Each arrow is one verb (for example, A → B means the verb is “AB”), and edge color shows the verb class.
        """,
        'generating_network': "Generating network graph...",
        'network_view_mode': "View Mode",
        'focused_view': "Focused Explorer",
        'full_view': "Full Network",
        'focus_char_label': "Start From Character",
        'focus_depth_label': "Neighborhood Depth",
        'network_summary': "Showing {nodes} characters and {edges} verbs.",
        'full_view_note': "Full network view is denser. Use Focused Explorer for easier browsing.",
        'edge_legend': "Verb class colors",
        'unknown_class': "Unclassified",
        'char_stats_header': "Character Statistics Explorer",
        'select_char_prompt': "Please select a character to see its statistics.",
        'starts_verbs_metric': "Starts Verbs",
        'ends_verbs_metric': "Ends Verbs",
        'total_verbs_metric': "Total Connections",
        'node_hover_starts': "Starts verbs",
        'node_hover_ends': "Ends verbs",
        'node_hover_total': "Total connections",
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
        此图展示单个汉字如何组合成双字动词。请使用侧栏按**动词类别**进行筛选。
        - **节点：** 单个汉字。节点越大，表示连接的动词越多。
        - **边：** 每条箭头代表一个动词（例如 A → B 表示“AB”），边的颜色表示动词类别。
        """,
        'generating_network': "正在生成网络图...",
        'network_view_mode': "视图模式",
        'focused_view': "聚焦探索",
        'full_view': "完整网络",
        'focus_char_label': "从这个汉字开始",
        'focus_depth_label': "邻域层级",
        'network_summary': "当前显示 {nodes} 个汉字，{edges} 个动词。",
        'full_view_note': "完整网络会更密集。更适合学习者浏览的是“聚焦探索”。",
        'edge_legend': "动词类别颜色",
        'unknown_class': "未分类",
        'char_stats_header': "汉字统计浏览器",
        'select_char_prompt': "请选择一个汉字以查看其统计数据。",
        'starts_verbs_metric': "作为首字",
        'ends_verbs_metric': "作为尾字",
        'total_verbs_metric': "总连接数",
        'node_hover_starts': "作为首字",
        'node_hover_ends': "作为尾字",
        'node_hover_total': "总连接数",
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
@st.cache_data(show_spinner=False)
def build_graph(df, classification_col_display):
    G = nx.DiGraph()
    for _, row in df.iterrows():
        if pd.notna(row['char1']) and pd.notna(row['char2']):
            classification = row.get(classification_col_display, None) if classification_col_display in row else None
            hover_lines = [row['Verb']]
            if pd.notna(row.get('pinyin')):
                hover_lines.append(str(row['pinyin']))
            if pd.notna(row.get('English_Verb')):
                hover_lines.append(str(row['English_Verb']))
            if pd.notna(classification):
                hover_lines.append(str(classification))

            G.add_edge(
                row['char1'],
                row['char2'],
                title=" | ".join(hover_lines),
                classification=classification,
                verb=row.get('Verb'),
                pinyin=row.get('pinyin'),
                english=row.get('English_Verb'),
            )
    return G

@st.cache_data(show_spinner=False)
def get_communities(_G):
    G_undirected = _G.to_undirected()
    communities = nx.community.greedy_modularity_communities(G_undirected)
    return sorted([list(c) for c in communities], key=len, reverse=True)


def make_class_color_map(classes):
    fallback_palette = ['#2563eb', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6', '#14b8a6']
    color_map = {}
    fallback_index = 0

    for class_name in classes:
        if not isinstance(class_name, str):
            continue

        class_name_lower = class_name.lower()
        if '动作' in class_name or 'action' in class_name_lower:
            color_map[class_name] = '#2563eb'
        elif '心理' in class_name or 'mental' in class_name_lower:
            color_map[class_name] = '#f59e0b'
        elif '其他' in class_name or 'other' in class_name_lower:
            color_map[class_name] = '#10b981'
        else:
            color_map[class_name] = fallback_palette[fallback_index % len(fallback_palette)]
            fallback_index += 1

    return color_map


def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return f"rgba(148, 163, 184, {alpha})"
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def render_class_legend(title, color_map):
    if not color_map:
        return

    chips = "".join(
        f"""
        <span style="display:inline-flex;align-items:center;gap:0.4rem;padding:0.35rem 0.7rem;border:1px solid #dbe2ea;
        border-radius:999px;background:#ffffff;font-size:0.92rem;margin:0.2rem 0.35rem 0.2rem 0;">
            <span style="width:0.78rem;height:0.78rem;border-radius:999px;background:{color};display:inline-block;"></span>
            {label}
        </span>
        """
        for label, color in color_map.items()
    )
    st.markdown(
        f"""
        <div style="margin:0.4rem 0 1rem 0;">
            <div style="font-weight:600;margin-bottom:0.45rem;">{title}</div>
            <div style="display:flex;flex-wrap:wrap;">{chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def add_neutral_nodes(net, G, T):
    degrees = dict(G.degree())
    min_degree, max_degree = (1, 1)
    if degrees:
        min_degree = min(degrees.values())
        max_degree = max(degrees.values())

    if max_degree == min_degree:
        normalized_degrees = {node: 18 for node in degrees}
    else:
        normalized_degrees = {
            node: 14 + 16 * (deg - min_degree) / (max_degree - min_degree)
            for node, deg in degrees.items()
        }

    for node, size in normalized_degrees.items():
        starts = G.out_degree(node)
        ends = G.in_degree(node)
        total = G.degree(node)
        title = "\n".join(
            [
                node,
                f"{T['node_hover_starts']}: {starts}",
                f"{T['node_hover_ends']}: {ends}",
                f"{T['node_hover_total']}: {total}",
            ]
        )

        net.add_node(
            node,
            label=node,
            title=title,
            size=size + 2,
            shape='circle',
            font={
                'size': max(int(size) + 5, 21),
                'color': '#0f172a',
                'face': 'Noto Sans SC, Microsoft YaHei, SimHei, sans-serif',
                'strokeWidth': 3,
                'strokeColor': '#ffffff',
                'vadjust': 0,
            },
            color={
                'background': '#fefce8',
                'border': '#c2410c',
                'highlight': {'background': '#fff7cc', 'border': '#9a3412'},
                'hover': {'background': '#fff7cc', 'border': '#9a3412'},
            },
            borderWidth=2,
            borderWidthSelected=3,
            shadow={'enabled': True, 'size': 10, 'x': 0, 'y': 2, 'color': 'rgba(15, 23, 42, 0.12)'},
        )


def add_class_edges(net, edge_df, graph, classification_col_display, class_color_map, unknown_class_label):
    for _, row in edge_df.iterrows():
        if pd.notna(row['char1']) and pd.notna(row['char2']):
            edge_data = graph.get_edge_data(row['char1'], row['char2']) or {}
            classification = row.get(classification_col_display, unknown_class_label)
            if pd.isna(classification):
                classification = unknown_class_label
            edge_color = class_color_map.get(classification, '#94a3b8')

            net.add_edge(
                row['char1'],
                row['char2'],
                title=edge_data.get('title', row.get('Verb', '')),
                color={
                    'color': hex_to_rgba(edge_color, 0.33),
                    'highlight': edge_color,
                    'hover': edge_color,
                    'inherit': False,
                },
                width=2.0,
                selectionWidth=3.5,
                hoverWidth=0.9,
                arrows='to',
                length=185,
            )


def configure_network(net):
    net.set_options(
        """
        var options = {
          "layout": {
            "improvedLayout": true
          },
          "nodes": {
            "shape": "circle",
            "scaling": {
              "min": 18,
              "max": 42
            }
          },
          "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true,
            "tooltipDelay": 120
          },
          "physics": {
            "solver": "barnesHut",
            "barnesHut": {
              "gravitationalConstant": -5200,
              "centralGravity": 0.08,
              "springLength": 205,
              "springConstant": 0.028,
              "damping": 0.22,
              "avoidOverlap": 1
            },
            "stabilization": {
              "enabled": true,
              "iterations": 180,
              "updateInterval": 25,
              "fit": true
            },
            "minVelocity": 0.75
          },
          "edges": {
            "smooth": {
              "enabled": true,
              "type": "continuous",
              "roundness": 0.08
            }
          }
        }
        """
    )


@st.cache_data(show_spinner=False)
def get_focus_network_df(df, focus_char, depth):
    if not focus_char:
        return df.copy()

    undirected = nx.Graph()
    valid_edges = df[['char1', 'char2']].dropna()
    undirected.add_edges_from(valid_edges.itertuples(index=False, name=None))

    if focus_char not in undirected:
        return df.copy()

    visible_nodes = set(nx.single_source_shortest_path_length(undirected, focus_char, cutoff=depth).keys())
    return df[df['char1'].isin(visible_nodes) & df['char2'].isin(visible_nodes)].copy()


@st.cache_data(show_spinner=False)
def build_network_html(
    df,
    classification_col_display,
    class_color_items,
    unknown_class_label,
    starts_label,
    ends_label,
    total_label,
    canvas_height,
):
    graph = build_graph(df, classification_col_display)
    class_color_map = dict(class_color_items)
    hover_labels = {
        'node_hover_starts': starts_label,
        'node_hover_ends': ends_label,
        'node_hover_total': total_label,
    }

    net = Network(
        height=canvas_height,
        width='100%',
        notebook=False,
        directed=True,
        cdn_resources='remote',
        select_menu=False,
        filter_menu=False,
        neighborhood_highlight=True,
        bgcolor='#ffffff',
        font_color='#0f172a',
    )
    configure_network(net)
    add_neutral_nodes(net, graph, hover_labels)
    add_class_edges(net, df, graph, classification_col_display, class_color_map, unknown_class_label)
    return net.generate_html(notebook=False)

# ----------------------------
# Sidebar
# ----------------------------
lang = language_selector()
T = translations[lang]

page_header(T['page_title'], "🕸️")

# --- Data Loading and Processing ---
@st.cache_data(show_spinner=False)
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
G = build_graph(filtered_df, classification_col_display)
class_color_map = make_class_color_map(unique_classes)


def render_network_html(net, height):
    components.html(net, height=height)

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
        ranked_chars = sorted(G.nodes(), key=lambda node: (-G.degree(node), node))
        default_focus_char = ranked_chars[0] if ranked_chars else None
        control_col1, control_col2, control_col3 = st.columns([1.1, 1.8, 1.1])

        with control_col1:
            view_mode = st.radio(
                T['network_view_mode'],
                options=[T['focused_view'], T['full_view']],
                horizontal=True,
            )

        focus_char = None
        focus_depth = 1
        if view_mode == T['focused_view'] and ranked_chars:
            with control_col2:
                focus_char = st.selectbox(
                    T['focus_char_label'],
                    options=ranked_chars,
                    index=0 if default_focus_char else None,
                )
            with control_col3:
                focus_depth = st.radio(
                    T['focus_depth_label'],
                    options=[1, 2],
                    index=0,
                    horizontal=True,
                )
        else:
            st.caption(T['full_view_note'])

        network_df = get_focus_network_df(filtered_df, focus_char, focus_depth) if view_mode == T['focused_view'] else filtered_df
        network_graph = build_graph(network_df, classification_col_display)
        visible_class_colors = {
            cls: class_color_map[cls]
            for cls in sorted(network_df[classification_col_display].dropna().unique())
            if cls in class_color_map
        }

        with st.spinner(T['generating_network']):
            render_class_legend(T['edge_legend'], visible_class_colors)
            st.caption(T['network_summary'].format(nodes=len(network_graph.nodes()), edges=len(network_df)))
            network_html = build_network_html(
                network_df,
                classification_col_display,
                tuple(class_color_map.items()),
                T['unknown_class'],
                T['node_hover_starts'],
                T['node_hover_ends'],
                T['node_hover_total'],
                '750px',
            )

            try:
                render_network_html(network_html, height=800)
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
                    family_classes = sorted(community_verbs_df[classification_col_display].dropna().unique())
                    family_class_colors = {cls: class_color_map[cls] for cls in family_classes if cls in class_color_map}
                    render_class_legend(T['edge_legend'], family_class_colors)
                    family_network_html = build_network_html(
                        community_verbs_df,
                        classification_col_display,
                        tuple(class_color_map.items()),
                        T['unknown_class'],
                        T['node_hover_starts'],
                        T['node_hover_ends'],
                        T['node_hover_total'],
                        '700px',
                    )
                    
                    try:
                        render_network_html(family_network_html, height=550)
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
