import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import page_header, load_data
from pyvis.network import Network
import networkx as nx
import os
import streamlit.components.v1 as components
import re
from collections import Counter, defaultdict
from i18n.tone_patterns import TRANSLATIONS as TX

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
# Translation Strings (EN/ZH)
# ----------------------------
st.markdown("""
<style>
/* ===== Expander: Blue header + persistent left stripe on body ===== */
div[data-testid="stExpander"] > details{
  --accent: #2563eb;          /* blue header & stripe */
  --accent-open: #1d4ed8;     /* header when open */
  --border: #dbeafe;          /* soft outer border */
  --focus: #93c5fd;
  border: 1px solid var(--border);
  border-radius: 12px;
  margin: .25rem 0 1rem 0;
  overflow: hidden;
  background: #fff;
  position: relative;
}

/* Header bar */
div[data-testid="stExpander"] > details > summary{
  list-style: none;
  background: var(--accent);
  color: #fff;
  padding: .75rem 1rem;
  font-weight: 700;
  cursor: pointer;
  user-select: none;
}
div[data-testid="stExpander"] > details > summary::-webkit-details-marker{ display:none; }
div[data-testid="stExpander"] > details > summary::after{
  content: "▾";
  float: right;
  color: #fff;
  transition: transform .2s ease;
}
div[data-testid="stExpander"] > details[open] > summary{
  background: var(--accent-open);
}
div[data-testid="stExpander"] > details[open] > summary::after{
  transform: rotate(180deg);
}

/* Body container (cover multiple Streamlit versions) */
div[data-testid="stExpander"] > details > div[role='group'],
div[data-testid="stExpander"] > details > div[role='region'],
div[data-testid="stExpander"] > details > div[data-testid="stExpanderContent"]{
  position: relative;               /* needed for the pseudo stripe */
  background: #fff;
  padding: 1rem 1.1rem 1rem 1.1rem; /* base padding; we'll add left offset when open */
  border-top: 1px solid var(--border);
}

/* Left stripe ON the body when open (pseudo-element so it never disappears) */
div[data-testid="stExpander"] > details[open] > div[role='group']::before,
div[data-testid="stExpander"] > details[open] > div[role='region']::before,
div[data-testid="stExpander"] > details[open] > div[data-testid="stExpanderContent"]::before{
  content: "";
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 6px;
  background: var(--accent);
  border-radius: 0;                 /* keep it crisp */
  pointer-events: none;
}
/* Add space so text doesn't sit under the stripe */
div[data-testid="stExpander"] > details[open] > div[role='group'],
div[data-testid="stExpander"] > details[open] > div[role='region'],
div[data-testid="stExpander"] > details[open] > div[data-testid="stExpanderContent"]{
  padding-left: calc(1.1rem + 6px);
}

/* Focus ring & hover (accessibility niceties) */
div[data-testid="stExpander"] > details > summary:hover{ filter: brightness(0.97); }
div[data-testid="stExpander"] > details > summary:focus{
  outline: 2px solid var(--focus);
  outline-offset: 2px;
}
</style>
""", unsafe_allow_html=True)



# ----------------------------
# Sidebar: language and header
# ----------------------------
lang = language_selector()

PAGE_FALLBACKS = {
    'en': {
        'pair_priority_header': "Most Useful Tone Pairs",
        'pair_priority_desc': "Start with the most frequent tone transitions in the current filter.",
        'pair_focus': "Focus Tone Pair",
        'pair_count_metric': "Verbs",
        'pair_char_count_metric': "Characters",
        'pair_top_class_metric': "Main Class",
        'pair_examples_header': "High-Value Examples",
        'pair_examples_desc': "These verbs are good starting examples for the selected tone pair.",
        'pair_characters_header': "Best Starter Characters",
        'pair_characters_desc': "These characters connect to the most verbs inside the selected tone pair.",
        'pair_network_header': "Focused Tone-Pair Network",
        'pair_network_desc': "Explore a small neighborhood instead of the full graph.",
        'pair_focus_char': "Center Character",
        'pair_focus_depth': "Neighborhood Depth",
        'network_summary': "Showing {nodes} characters and {edges} verbs for tone pair {pair}.",
        'character_col': "Character",
        'connections_col': "Connections",
        'tab_network': "🎯 Tone-Pair Explorer",
        'loading_data': "Loading tone explorer data...",
        'loading_network': "Rendering focused tone network...",
    },
    'zh': {
        'pair_priority_header': "最值得先学的声调模式",
        'pair_priority_desc': "先从当前筛选中最常见的声调转移开始。",
        'pair_focus': "聚焦声调模式",
        'pair_count_metric': "动词数",
        'pair_char_count_metric': "汉字数",
        'pair_top_class_metric': "主要类别",
        'pair_examples_header': "高价值例词",
        'pair_examples_desc': "这些动词适合作为该声调模式的起步例词。",
        'pair_characters_header': "最佳起步汉字",
        'pair_characters_desc': "这些汉字在所选声调模式中连接的动词最多。",
        'pair_network_header': "聚焦式声调网络",
        'pair_network_desc': "不要看整张大网，只看一个小范围邻域更适合学习。",
        'pair_focus_char': "中心汉字",
        'pair_focus_depth': "邻域层级",
        'network_summary': "当前展示声调模式 {pair} 下的 {nodes} 个汉字、{edges} 个动词。",
        'character_col': "汉字",
        'connections_col': "连接数",
        'tab_network': "🎯 声调模式探索",
        'loading_data': "正在加载声调探索数据...",
        'loading_network': "正在渲染聚焦声调网络...",
    },
}

T = {
    **PAGE_FALLBACKS['en'],
    **TX.get('en', {}),
    **PAGE_FALLBACKS.get(lang, {}),
    **TX.get(lang, {}),
}

page_header(T['page_title'], "🎵")

# ----------------------------
# Data Loading & Preprocessing
# ----------------------------
@st.cache_data(show_spinner=False)
def get_df():
    return load_data()

with st.spinner(T['loading_data']):
    df = get_df()
if df.empty:
    st.error(T['load_error'])
    st.stop()

# Handle bilingual classification

def parse_bilingual(text):
    if isinstance(text, str) and '(' in text and ')' in text:
        parts = text.split('(')
        zh, en = parts[0], parts[1].replace(')', '')
        return zh.strip(), en.strip()
    return text, text

if 'Chinese_Verbs' in df.columns and 'Verb' not in df.columns:
    df.rename(columns={'Chinese_Verbs': 'Verb'}, inplace=True)

if '分类（Classification）' in df.columns:
    df[['Classification_zh', 'Classification_en']] = df['分类（Classification）'].apply(lambda x: pd.Series(parse_bilingual(x)))
    classification_col_display = 'Classification_zh' if lang == 'zh' else 'Classification_en'
else:
    classification_col_display = 'English_Verb'  # fallback

# Clean tone pair

def split_tone_pair(tp: str):
    try:
        a,b = str(tp).split('-')
        return int(a), int(b)
    except Exception:
        return None, None

# Compute helper columns
for col in ['char1','char2','tone_pattern','pinyin']:
    if col not in df.columns:
        df[col] = None

# Remove rows missing chars or tones
src_tone, dst_tone = zip(*df['tone_pattern'].astype(str).map(split_tone_pair))
df['src_tone'] = src_tone
df['dst_tone'] = dst_tone
mask_valid = df['char1'].notna() & df['char2'].notna() & df['src_tone'].between(1,5) & df['dst_tone'].between(1,5)
df = df.loc[mask_valid].copy()

# Pinyin base (remove 1–5 digits)
df['pinyin_base'] = df['pinyin'].astype(str).str.replace(r"[1-5]", "", regex=True)

# Build aggregated edge table to get weights
agg_cols = ['char1','char2','tone_pattern','src_tone','dst_tone','Verb','pinyin','English_Verb']
if 'Classification_zh' in df.columns and 'Classification_en' in df.columns:
    agg_cols += ['Classification_zh','Classification_en']
edge_df = df[agg_cols].copy()
edge_df['weight'] = 1
edge_df = edge_df.groupby(['char1','char2','tone_pattern','src_tone','dst_tone'], as_index=False).agg({
    'weight':'sum',
    'Verb':'first','pinyin':'first','English_Verb':'first',
    **({'Classification_zh':'first','Classification_en':'first'} if 'Classification_zh' in df.columns else {})
})

# Build graph
@st.cache_data(show_spinner=False)
def build_graph(edge_df: pd.DataFrame):
    G = nx.DiGraph()
    for _, r in edge_df.iterrows():
        G.add_edge(r['char1'], r['char2'],
                   tone_pair=r['tone_pattern'], src_tone=int(r['src_tone']), dst_tone=int(r['dst_tone']),
                   weight=int(r['weight']),
                   verb=r.get('Verb'), pinyin=r.get('pinyin'), english=r.get('English_Verb'),
                   cls_zh=r.get('Classification_zh'), cls_en=r.get('Classification_en'))
    # dominant node tone
    node_tone = {}
    for n in G.nodes():
        tones = []
        for _, _, d in G.in_edges(n, data=True):
            tones.append(d['dst_tone'])
        for _, _, d in G.out_edges(n, data=True):
            tones.append(d['src_tone'])
        if tones:
            counts = Counter(tones)
            node_tone[n] = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    nx.set_node_attributes(G, node_tone, 'tone')
    return G

G_full = build_graph(edge_df)

# ----------------------------
# Shared Filters (apply to multiple tabs)
# ----------------------------
all_pairs = sorted(edge_df['tone_pattern'].dropna().unique())
all_src = sorted(edge_df['src_tone'].dropna().unique())
all_dst = sorted(edge_df['dst_tone'].dropna().unique())
all_classes = sorted(df[classification_col_display].dropna().unique()) if classification_col_display in df.columns else []

st.sidebar.header(T['controls_header'])
selected_pairs = st.sidebar.multiselect(T['filter_by_tonepair'], options=all_pairs, default=all_pairs)
selected_src = st.sidebar.multiselect(T['filter_src_tone'], options=all_src, default=all_src)
selected_dst = st.sidebar.multiselect(T['filter_dst_tone'], options=all_dst, default=all_dst)
selected_cls = st.sidebar.multiselect(T['filter_class'], options=all_classes, default=all_classes) if all_classes else []

# Filter edge table
mask = edge_df['tone_pattern'].isin(selected_pairs) & edge_df['src_tone'].isin(selected_src) & edge_df['dst_tone'].isin(selected_dst)
if selected_cls and 'Classification_zh' in edge_df.columns:
    disp_col = 'Classification_zh' if lang == 'zh' else 'Classification_en'
    mask = mask & edge_df[disp_col].isin(selected_cls)
edge_df_f = edge_df.loc[mask].copy()

# Color map for tone pairs
palette = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf",
           "#393b79","#637939","#8c6d31","#843c39","#7b4173","#3182bd","#e6550d","#31a354","#756bb1","#636363"]
unique_pairs = sorted(edge_df['tone_pattern'].dropna().unique())
pair_color = {tp: palette[i % len(palette)] for i, tp in enumerate(unique_pairs)}


def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return f"rgba(148, 163, 184, {alpha})"
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


@st.cache_data(show_spinner=False)
def get_focus_network_df(edge_subset: pd.DataFrame, focus_char: str, depth: int):
    if edge_subset.empty or not focus_char:
        return edge_subset.copy()

    undirected = nx.Graph()
    undirected.add_edges_from(edge_subset[['char1', 'char2']].dropna().itertuples(index=False, name=None))

    if focus_char not in undirected:
        return edge_subset.copy()

    visible_nodes = set(nx.single_source_shortest_path_length(undirected, focus_char, cutoff=depth).keys())
    return edge_subset[
        edge_subset['char1'].isin(visible_nodes) & edge_subset['char2'].isin(visible_nodes)
    ].copy()


@st.cache_data(show_spinner=False)
def build_pair_network_html(edge_subset: pd.DataFrame, edge_color: str):
    G = nx.DiGraph()
    for _, row in edge_subset.iterrows():
        G.add_edge(
            row['char1'],
            row['char2'],
            title=" | ".join(
                [
                    str(row.get('Verb', '')),
                    str(row.get('pinyin', '')),
                    str(row.get('English_Verb', '')),
                    str(row.get('tone_pattern', '')),
                ]
            ),
            weight=int(row.get('weight', 1)),
        )

    degrees = dict(G.degree())
    if degrees:
        min_degree = min(degrees.values())
        max_degree = max(degrees.values())
    else:
        min_degree, max_degree = 0, 1

    if max_degree == min_degree:
        normalized = {node: 18 for node in degrees}
    else:
        normalized = {
            node: 14 + 12 * (deg - min_degree) / (max_degree - min_degree)
            for node, deg in degrees.items()
        }

    net = Network(
        height='620px',
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
    net.set_options(
        """
        var options = {
          "layout": {
            "improvedLayout": true
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
              "gravitationalConstant": -4200,
              "centralGravity": 0.08,
              "springLength": 175,
              "springConstant": 0.03,
              "damping": 0.2,
              "avoidOverlap": 0.9
            },
            "stabilization": {
              "enabled": true,
              "iterations": 160,
              "fit": true
            }
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

    for node, size in normalized.items():
        net.add_node(
            node,
            label=node,
            title=node,
            shape='circle',
            size=size,
            font={
                'size': max(int(size) + 7, 22),
                'color': '#0f172a',
                'face': 'Noto Sans SC, Microsoft YaHei, SimHei, sans-serif',
                'strokeWidth': 3,
                'strokeColor': '#ffffff',
            },
            color={
                'background': '#fff7cc',
                'border': '#b45309',
                'highlight': {'background': '#fef3c7', 'border': '#92400e'},
                'hover': {'background': '#fef3c7', 'border': '#92400e'},
            },
            borderWidth=2,
        )

    for u, v, data in G.edges(data=True):
        net.add_edge(
            u,
            v,
            title=data.get('title', ''),
            color={
                'color': hex_to_rgba(edge_color, 0.38),
                'highlight': edge_color,
                'hover': edge_color,
                'inherit': False,
            },
            width=1.8 + min(data.get('weight', 1), 3) * 0.4,
            arrows='to',
            length=170,
        )

    return net.generate_html(notebook=False)

# ----------------------------
# Tabs
# ----------------------------
TAB2, TAB5, TAB6 = st.tabs([
    T['tab_network'], T['tab_minpairs'], T['tab_charprof']
])

# ----------------------------
# TAB 2 – Tone Network
# ----------------------------
with TAB2:
    st.header(T['tab_network'])
    with st.expander(T['help_network_title'], expanded=False):
        st.markdown(T['help_network_body'])

    st.markdown(T['network_desc'])

    if edge_df_f.empty:
        st.warning(T['no_match_warning'])
    else:
        pair_rank = (
            edge_df_f.groupby('tone_pattern', as_index=False)['weight']
            .sum()
            .sort_values('weight', ascending=False)
        )

        st.subheader(T['pair_priority_header'])
        st.caption(T['pair_priority_desc'])
        fig_pairs = px.bar(
            pair_rank.head(12),
            x='weight',
            y='tone_pattern',
            orientation='h',
            text='weight',
            color='tone_pattern',
            color_discrete_map=pair_color,
        )
        fig_pairs.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
        st.plotly_chart(fig_pairs, use_container_width=True)

        focus_pair = st.selectbox(
            T['pair_focus'],
            options=pair_rank['tone_pattern'].tolist(),
            index=0,
        )
        pair_df = edge_df_f[edge_df_f['tone_pattern'] == focus_pair].copy()
        pair_graph = build_graph(pair_df)
        disp_col = 'Classification_zh' if lang == 'zh' else 'Classification_en'
        top_class = '—'
        if disp_col in pair_df.columns and not pair_df[disp_col].dropna().empty:
            top_class = pair_df[disp_col].value_counts().idxmax()

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric(T['pair_count_metric'], int(pair_df['weight'].sum()))
        metric2.metric(T['pair_char_count_metric'], int(pair_graph.number_of_nodes()))
        metric3.metric(T['pair_top_class_metric'], top_class)

        st.subheader(T['pair_examples_header'])
        st.caption(T['pair_examples_desc'])
        pair_examples = pair_df[['Verb', 'pinyin', 'English_Verb', 'weight']].sort_values(
            ['weight', 'Verb'], ascending=[False, True]
        ).rename(columns={'weight': T['connections_col']})
        st.dataframe(pair_examples.head(20), use_container_width=True, hide_index=True)

        st.subheader(T['pair_characters_header'])
        st.caption(T['pair_characters_desc'])
        char_counts = Counter(pair_df['char1'].dropna().tolist() + pair_df['char2'].dropna().tolist())
        char_df = pd.DataFrame(
            char_counts.most_common(12),
            columns=[T['character_col'], T['connections_col']]
        )
        left_col, right_col = st.columns([1.1, 1.6])
        with left_col:
            st.dataframe(char_df, use_container_width=True, hide_index=True)

        ranked_chars = sorted(pair_graph.nodes(), key=lambda node: (-pair_graph.degree(node), node))
        focus_char = ranked_chars[0] if ranked_chars else None
        focus_depth = 1
        if ranked_chars:
            with right_col:
                st.subheader(T['pair_network_header'])
                st.caption(T['pair_network_desc'])
                control_a, control_b = st.columns([1.5, 1])
                with control_a:
                    focus_char = st.selectbox(T['pair_focus_char'], options=ranked_chars, index=0)
                with control_b:
                    focus_depth = st.radio(T['pair_focus_depth'], options=[1, 2], index=0, horizontal=True)

            visible_pair_df = get_focus_network_df(pair_df, focus_char, focus_depth)
            visible_pair_graph = build_graph(visible_pair_df)
            st.caption(
                T['network_summary'].format(
                    nodes=visible_pair_graph.number_of_nodes(),
                    edges=len(visible_pair_df),
                    pair=focus_pair,
                )
            )
            try:
                with st.spinner(T['loading_network']):
                    pair_html = build_pair_network_html(visible_pair_df, pair_color.get(focus_pair, '#6366f1'))
                    components.html(pair_html, height=680)
            except Exception as e:
                st.error(f"Error displaying graph: {e}")

# ----------------------------
# TAB 5 – Minimal Tone-Contrast Sets
# ----------------------------
with TAB5:
    st.header(T['tab_minpairs'])
    with st.expander(T['help_minpairs_title'], expanded=False):
        st.markdown(T['help_minpairs_body'])

    st.caption(T['minpairs_desc'])

    if edge_df_f.empty:
        st.warning(T['no_match_warning'])
    else:
        focus = st.selectbox(T['minpairs_contrast'], options=[T['contrast_any'], T['contrast_src'], T['contrast_dst']])
        # Build groups where letters are the same (pinyin digits removed)
        sub = df.copy()
        sub = sub[sub['tone_pattern'].isin(selected_pairs) & sub['src_tone'].isin(selected_src) & sub['dst_tone'].isin(selected_dst)]
        groups = sub.groupby('pinyin_base')
        records = []
        for base, block in groups:
            if len(block) < 2: continue
            # unique by tone pair
            block_u = block.drop_duplicates(subset=['tone_pattern'])
            # pairwise combinations
            rows = block_u[['Verb','pinyin','English_Verb','tone_pattern']]
            arr = rows.to_dict('records')
            for i in range(len(arr)):
                for j in range(i+1, len(arr)):
                    a, b = arr[i], arr[j]
                    s1, d1 = map(int, a['tone_pattern'].split('-'))
                    s2, d2 = map(int, b['tone_pattern'].split('-'))
                    cond = False
                    if focus == T['contrast_any']:
                        cond = (a['tone_pattern'] != b['tone_pattern'])
                    elif focus == T['contrast_src']:
                        cond = (s1 != s2)
                    elif focus == T['contrast_dst']:
                        cond = (d1 != d2)
                    if cond:
                        records.append({
                            'pinyin_base': base,
                            'A_Verb': a['Verb'], 'A_pinyin': a['pinyin'], 'A_tone': a['tone_pattern'], 'A_Eng': a['English_Verb'],
                            'B_Verb': b['Verb'], 'B_pinyin': b['pinyin'], 'B_tone': b['tone_pattern'], 'B_Eng': b['English_Verb'],
                        })
        mpairs = pd.DataFrame(records)
        if mpairs.empty:
            st.warning(T['no_match_warning'])
        else:
            st.dataframe(mpairs.head(300), use_container_width=True)
            st.download_button(T['download_csv'], mpairs.to_csv(index=False).encode('utf-8'), file_name='minimal_pairs.csv', mime='text/csv')

# ----------------------------
# TAB 6 – Character Tone Profiles
# ----------------------------
with TAB6:
    st.header(T['tab_charprof'])
    with st.expander(T['help_charprof_title'], expanded=False):
        st.markdown(T['help_charprof_body'])

    st.caption(T['charprof_desc'])
    all_chars = sorted(list(set(edge_df[['char1','char2']].values.flatten())))
    sel_char = st.selectbox(T['charprof_select'], options=['']+all_chars)

    if sel_char:
        df_char_src = df[df['char1']==sel_char]
        df_char_dst = df[df['char2']==sel_char]
        # Profile
        tone_counts = pd.Series(dtype=int)
        tone_counts = df_char_src['src_tone'].value_counts().add(df_char_dst['dst_tone'].value_counts(), fill_value=0).astype(int)
        tone_counts = tone_counts.sort_index()
        prof_df = pd.DataFrame({'tone': tone_counts.index.astype(int), 'count': tone_counts.values})
        st.subheader(T['tone_profile'])
        fig = px.bar(prof_df, x='tone', y='count', text='count')
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric(T['src_count'], int(len(df_char_src)))
            st.dataframe(df_char_src[['Verb','pinyin','English_Verb','tone_pattern']].drop_duplicates(), use_container_width=True)
        with col2:
            st.metric(T['dst_count'], int(len(df_char_dst)))
            st.dataframe(df_char_dst[['Verb','pinyin','English_Verb','tone_pattern']].drop_duplicates(), use_container_width=True)

        # Quick buttons
        st.subheader(T['quick_show'])
        tlist = [1,2,3,4,5]
        c1, c2 = st.columns(2)
        with c1:
            toneX = st.selectbox('X (src)', options=tlist, index=2)
            sub = df[(df['char1']==sel_char) & (df['src_tone']==toneX)]
            st.caption(T['show_src_to_any'].replace('X', str(toneX)))
            st.dataframe(sub[['Verb','pinyin','English_Verb','tone_pattern']], use_container_width=True)
        with c2:
            toneY = st.selectbox('X (dst)', options=tlist, index=3)
            sub2 = df[(df['char2']==sel_char) & (df['dst_tone']==toneY)]
            st.caption(T['show_any_to_dst'].replace('X', str(toneY)))
            st.dataframe(sub2[['Verb','pinyin','English_Verb','tone_pattern']], use_container_width=True)
