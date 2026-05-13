#utils.py
import streamlit as st
import pandas as pd
from db import run_query


LANG_OPTIONS = {"English": "en", "中文 (Chinese)": "zh"}
LANG_DISPLAY_BY_CODE = {code: label for label, code in LANG_OPTIONS.items()}
LANG_STATE_KEY = "app_language"
LANG_WIDGET_KEY = "_app_language_widget"


# @st.cache_data(ttl=86400)  # cache for 1 day
# def cached_query(query_func, query: str):
#     """Run a query with caching wrapper."""
#     return query_func(query)

def page_header(title: str, emoji: str = "📄"):
    """Reusable page header with emoji."""
    st.markdown(f"# {emoji} {title}")


def language_selector(
    header: str = "⚙️ Settings / 设置",
    label: str = "Select Language / 选择语言",
):
    """Persist language choice across Streamlit multipage navigation."""
    if LANG_STATE_KEY not in st.session_state:
        st.session_state[LANG_STATE_KEY] = "en"

    current_lang = st.session_state.get(LANG_STATE_KEY, "en")
    current_display = LANG_DISPLAY_BY_CODE.get(current_lang, "English")
    st.session_state[LANG_WIDGET_KEY] = current_display

    def sync_language():
        selected_display = st.session_state.get(LANG_WIDGET_KEY, "English")
        st.session_state[LANG_STATE_KEY] = LANG_OPTIONS.get(selected_display, "en")

    st.sidebar.header(header)
    st.sidebar.radio(
        label,
        options=list(LANG_OPTIONS.keys()),
        key=LANG_WIDGET_KEY,
        horizontal=True,
        on_change=sync_language,
    )
    sync_language()
    return st.session_state[LANG_STATE_KEY]


@st.cache_data(ttl=86400, show_spinner=False) # cache for one day
def load_data(local_csv="data/two_char_verbs_with_Tr_Pro_with_UMAP.csv",
              table_name="verbs",
              use_local=False,
              show_status=False):
    """
    Load verbs data:
    - If use_local=True -> always load local CSV
    - If use_local=False and Neon secret exists -> query Neon
    """
    if not use_local and "db_connection" in st.secrets and run_query is not None:
        try:
            df = run_query(f"SELECT * FROM {table_name};")
            if show_status:
                st.info("Loaded data from Neon database ✅")
            return df
        except Exception as e:
            st.warning(f"Failed to query Neon DB: {e}\nFalling back to local CSV.")

    # Local CSV fallback
    try:
        df = pd.read_csv(local_csv)
        if show_status:
            st.info("Loaded data from local CSV ✅")
        return df
    except FileNotFoundError:
        st.error("Local CSV not found. Please add it to your project folder.")
        return pd.DataFrame()  # empty DataFrame
