import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import page_header, load_data
import os

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
# Page Configuration & Header
# ----------------------------
st.set_page_config(layout="wide")

# ----------------------------
# Translation Strings
# ----------------------------
translations = {
    'en': {
        'page_title': "Explore Two-Character Verbs",
        'load_error': "Data could not be loaded. Please ensure the data file is available.",
        'settings_header': "⚙️ Settings",
        'language_select': "Select Language",
        'controls_header': "🔍 Controls",
        'filter_by_category': "Filter by Verb Category",
        'filter_by_tone': "Filter by Tone Pattern",
        'highlight_verb': "Highlight a Specific Verb",
        'no_match_warning': "No verbs match the current filter selection.",
        'tab_semantic': "🗺️ Semantic Map",
        'tab_tonal': "🌊 Tonal Flow",
        'semantic_header': "Semantic Verb Map",
        'semantic_desc': """
        This interactive scatter plot visualizes the semantic relationships between verbs. The positions are determined by UMAP, a dimensionality reduction technique applied to word embeddings.
        **Verbs that are closer together are more similar in meaning.**
        - **Color:** Represents the verb's functional category.
        - **Interact:** Hover over points to see details, and use the mouse to zoom and pan.
        """,
        'category_legend_title': "Verb Category",
        'details_for': "Details for",
        'metric_english': "English",
        'metric_category': "Category",
        'metric_tone': "Tone Pattern",
        'metric_prob': "Transition Probability",
        'tonal_header': "Tonal Flow in Two-Character Verbs",
        'tonal_desc': """
        This Sankey diagram shows the most common tone patterns. The width of the flow from a
        first character tone (left) to a second character tone (right) represents the number of verbs
        with that specific pattern in the selected data. This helps identify common phonetic structures.
        """,
        'sankey_title': "First Character Tone to Second Character Tone Flow",
        'sankey_tone_1st': "Tone {t} (1st)",
        'sankey_tone_2nd': "Tone {t} (2nd)",
        'no_sankey_data': "No data to display Tonal Flow diagram for the current selection.",
    },
    'zh': {
        'page_title': "探索双字动词",
        'load_error': "无法加载数据。请确保数据文件可用。",
        'settings_header': "⚙️ 设置",
        'language_select': "选择语言",
        'controls_header': "🔍 控制面板",
        'filter_by_category': "按动词类别筛选",
        'filter_by_tone': "按声调模式筛选",
        'highlight_verb': "高亮特定动词",
        'no_match_warning': "没有符合当前筛选条件的动词。",
        'tab_semantic': "🗺️ 语义地图",
        'tab_tonal': "🌊 声调流向",
        'semantic_header': "动词语义地图",
        'semantic_desc': """
        这个交互式散点图展示了动词之间的语义关系。位置由 UMAP（一种应用于词嵌入的降维技术）确定。
        **位置越近的动词，意义也越相似。**
        - **颜色:** 代表动词的功能类别。
        - **交互:** 将鼠标悬停在点上可查看详细信息，使用鼠标进行缩放和平移。
        """,
        'category_legend_title': "动词类别",
        'details_for': "详细信息",
        'metric_english': "英文",
        'metric_category': "类别",
        'metric_tone': "声调模式",
        'metric_prob': "转换概率",
        'tonal_header': "双字动词的声调流向",
        'tonal_desc': """
        此桑基图显示了最常见的声调模式。从第一个字声调（左）到第二个字声调（右）的流量宽度，
        代表了在所选数据中具有该特定模式的动词数量。这有助于识别常见的语音结构。
        """,
        'sankey_title': "第一字声调到第二字声调流向图",
        'sankey_tone_1st': "{t}声 (第一字)",
        'sankey_tone_2nd': "{t}声 (第二字)",
        'no_sankey_data': "没有可用于当前选择的声调流向图数据。",
    }
}

# ----------------------------
# Sidebar Language Selector
# ----------------------------
lang = language_selector()
T = translations[lang]

page_header(T['page_title'], "📖")

# ----------------------------
# Load and Process Data
# ----------------------------
df = load_data()

if df.empty:
    st.error(T['load_error'])
    st.stop()

def parse_bilingual(text):
    if isinstance(text, str) and '(' in text and ')' in text:
        parts = text.split('(')
        zh = parts[0]
        en = parts[1].replace(')', '')
        return zh.strip(), en.strip()
    return text, text

df[['Classification_zh', 'Classification_en']] = df['分类（Classification）'].apply(lambda x: pd.Series(parse_bilingual(x)))
df.rename(columns={'Chinese_Verbs': 'Verb'}, inplace=True)
classification_col_display = 'Classification_zh' if lang == 'zh' else 'Classification_en'

# ----------------------------
# Sidebar for Filters & Controls
# ----------------------------
st.sidebar.header(T['controls_header'])

type_mapping = df.set_index(classification_col_display)['verb_type'].to_dict()
unique_display_types = sorted(df[classification_col_display].unique())

selected_display_types = st.sidebar.multiselect(
    T['filter_by_category'],
    options=unique_display_types,
    default=unique_display_types
)
selected_types_internal = [type_mapping.get(t) for t in selected_display_types if t in type_mapping]

unique_tone_patterns = sorted(df['tone_pattern'].unique())
selected_tones = st.sidebar.multiselect(
    T['filter_by_tone'],
    options=unique_tone_patterns,
    default=unique_tone_patterns
)

filtered_df = df[df['verb_type'].isin(selected_types_internal) & df['tone_pattern'].isin(selected_tones)].copy()

# ----------------------------
# Main Content in Tabs
# ----------------------------
tab1, tab2 = st.tabs([T['tab_semantic'], T['tab_tonal']])

# --- Tab 1: Semantic Map ---
with tab1:
    st.header(T['semantic_header'])
    st.markdown(T['semantic_desc'])
    
    # --- Highlight verb selectbox is now INSIDE the tab ---
    search_verb = st.selectbox(
        T['highlight_verb'],
        options=[''] + sorted(list(filtered_df['Verb'].unique())),
        format_func=lambda x: f"{x} ({df[df['Verb'] == x]['pinyin'].iloc[0]})" if x else "None"
    )

    if filtered_df.empty:
        st.warning(T['no_match_warning'])
    else:
        fig_umap = px.scatter(
            filtered_df,
            x='umap_x',
            y='umap_y',
            color='verb_type',
            hover_data={
                'Verb': True, 'pinyin': True, 'English_Verb': True,
                classification_col_display: True, 'verb_type': False,
                'umap_x': False, 'umap_y': False
            },
            labels={'verb_type': T['category_legend_title']},
            template='plotly_white'
        )
        fig_umap.update_layout(height=600, legend_title_text=T['category_legend_title'])
        fig_umap.update_traces(marker=dict(size=8, opacity=0.7))

        legend_name_mapping = df.set_index('verb_type')[classification_col_display].to_dict()
        fig_umap.for_each_trace(lambda t: t.update(name=legend_name_mapping.get(t.name, t.name)))

        if search_verb:
            highlight_df = filtered_df[filtered_df['Verb'] == search_verb]
            if not highlight_df.empty:
                fig_umap.add_trace(go.Scatter(
                    x=highlight_df['umap_x'], y=highlight_df['umap_y'],
                    mode='markers', marker=dict(color='black', size=16, symbol='star'),
                    name='Selected', hoverinfo='skip'
                ))
        st.plotly_chart(fig_umap, use_container_width=True)

        if search_verb:
            verb_details = df[df['Verb'] == search_verb].iloc[0]
            st.subheader(f"{T['details_for']}: {verb_details['Verb']} ({verb_details['pinyin']})")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(T['metric_english'], verb_details['English_Verb'])
            col2.metric(T['metric_category'], verb_details[classification_col_display])
            col3.metric(T['metric_tone'], verb_details['tone_pattern'])
            col4.metric(T['metric_prob'], f"{verb_details['transition_probability_PerVerbType']:.2%}")

# --- Tab 2: Tonal Flow ---
with tab2:
    st.header(T['tonal_header'])
    st.markdown(T['tonal_desc'])

    if not filtered_df.empty:
        sankey_data = filtered_df.groupby(['first_char_tone', 'second_char_tone']).size().reset_index(name='count')
        labels = [T['sankey_tone_1st'].format(t=t) for t in range(1, 6)] + \
                 [T['sankey_tone_2nd'].format(t=t) for t in range(1, 6)]
        
        # Adjust for tones including neutral tone (often marked as 5 or 0)
        sankey_data = sankey_data[(sankey_data['first_char_tone'] > 0) & (sankey_data['second_char_tone'] > 0)]
        
        source = sankey_data['first_char_tone'].apply(lambda t: t - 1)
        target = sankey_data['second_char_tone'].apply(lambda t: t + 4) # Adjust target index
        value = sankey_data['count']

        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels, color="royalblue"),
            link=dict(source=source, target=target, value=value)
        )])
        fig_sankey.update_layout(title_text=T['sankey_title'], font_size=12, height=400)
        st.plotly_chart(fig_sankey, use_container_width=True)
    else:
        st.warning(T['no_sankey_data'])
