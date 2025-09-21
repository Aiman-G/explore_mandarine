import streamlit as st
import pandas as pd
import plotly.express as px
from utils import page_header, load_data

# ----------------------------
# Page Configuration & Header
# ----------------------------
st.set_page_config(layout="wide")

# ----------------------------
# Translation Strings
# ----------------------------
translations = {
    'en': {
        'page_title': "Verb Analytics",
        'load_error': "Data could not be loaded. Please ensure the data file is available.",
        'settings_header': "⚙️ Settings",
        'language_select': "Select Language",
        'category_dist_header': "Verb Category Distribution",
        'category_dist_desc': "This chart shows the number of verbs in each functional category, providing an overview of the dataset's composition.",
        'category': "Category",
        'verb_count': "Number of Verbs",
        'phonetic_header': "Phonetic Component Analysis (Initials & Finals)",
        'phonetic_desc': "These charts display the most frequent initials (声母 shēngmǔ) and finals (韵母 yùnmǔ) for the first and second characters in the verbs. This helps identify common phonetic building blocks in verb formation.",
        'initial_1': "First Character - Initial",
        'final_1': "First Character - Final",
        'initial_2': "Second Character - Initial",
        'final_2': "Second Character - Final",
        'frequency': "Frequency",
        'component': "Phonetic Component"
    },
    'zh': {
        'page_title': "动词分析",
        'load_error': "无法加载数据。请确保数据文件可用。",
        'settings_header': "⚙️ 设置",
        'language_select': "选择语言",
        'category_dist_header': "动词类别分布",
        'category_dist_desc': "此图表显示了每个功能类别中的动词数量，提供了数据集构成的概览。",
        'category': "类别",
        'verb_count': "动词数量",
        'phonetic_header': "语音成分分析 (声母和韵母)",
        'phonetic_desc': "这些图表显示了动词中第一和第二汉字最常见的声母 (shēngmǔ) 和韵母 (yùnmǔ)。这有助于识别动词构成中常见的语音构件。",
        'initial_1': "第一字 - 声母",
        'final_1': "第一字 - 韵母",
        'initial_2': "第二字 - 声母",
        'final_2': "第二字 - 韵母",
        'frequency': "频率",
        'component': "语音成分"
    }
}

# ----------------------------
# Sidebar Language Selector
# ----------------------------
st.sidebar.header("⚙️ Settings / 设置")
lang_options = {'English': 'en', '中文 (Chinese)': 'zh'}
selected_lang_display = st.sidebar.radio(
    "Select Language / 选择语言",
    options=lang_options.keys(),
    horizontal=True
)
lang = lang_options[selected_lang_display]
T = translations[lang]

page_header(T['page_title'], "💡")

# ----------------------------
# Load and Process Data
# ----------------------------
df = load_data()

if df.empty:
    st.error(T['load_error'])
    st.stop()

# Function to parse bilingual column like "中文(English)"
def parse_bilingual(text):
    if isinstance(text, str) and '(' in text and ')' in text:
        parts = text.split('(')
        zh = parts[0]
        en = parts[1].replace(')', '')
        return zh.strip(), en.strip()
    return text, text

# Apply parsing to the classification column
df[['Classification_zh', 'Classification_en']] = df['分类（Classification）'].apply(lambda x: pd.Series(parse_bilingual(x)))
classification_col_display = 'Classification_zh' if lang == 'zh' else 'Classification_en'

# ----------------------------
# Main Content
# ----------------------------

# --- 1. Category Distribution ---
st.header(T['category_dist_header'])
st.markdown(T['category_dist_desc'])

category_counts = df[classification_col_display].value_counts().reset_index()
category_counts.columns = [classification_col_display, 'count']

fig_cat = px.bar(
    category_counts,
    x='count',
    y=classification_col_display,
    orientation='h',
    title=T['category_dist_header'],
    labels={
        'count': T['verb_count'],
        classification_col_display: T['category']
    }
)
fig_cat.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_cat, use_container_width=True)

st.divider()

# --- 2. Phonetic Breakdown ---
st.header(T['phonetic_header'])
st.markdown(T['phonetic_desc'])

col1, col2 = st.columns(2)

# Function to create a frequency chart
def create_freq_chart(data_series, title):
    freq = data_series.value_counts().nlargest(15).reset_index()
    freq.columns = ['component', 'count']
    fig = px.bar(
        freq,
        x='count',
        y='component',
        orientation='h',
        title=title,
        labels={
            'count': T['frequency'],
            'component': T['component']
        }
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

with col1:
    st.plotly_chart(create_freq_chart(df['initial_1'], T['initial_1']), use_container_width=True)
    st.plotly_chart(create_freq_chart(df['initial_2'], T['initial_2']), use_container_width=True)

with col2:
    st.plotly_chart(create_freq_chart(df['final_1'], T['final_1']), use_container_width=True)
    st.plotly_chart(create_freq_chart(df['final_2'], T['final_2']), use_container_width=True)
