#utils.py
import streamlit as st
import pandas as pd
from db import run_query


# @st.cache_data(ttl=86400)  # cache for 1 day
# def cached_query(query_func, query: str):
#     """Run a query with caching wrapper."""
#     return query_func(query)

def page_header(title: str, emoji: str = "📄"):
    """Reusable page header with emoji."""
    st.markdown(f"# {emoji} {title}")


@st.cache_data(ttl=86400) # cash for one day
def load_data(local_csv="data/two_char_verbs_with_Tr_Pro_with_UMAP.csv",
              table_name="verbs",
              use_local=False):
    """
    Load verbs data:
    - If use_local=True -> always load local CSV
    - If use_local=False and Neon secret exists -> query Neon
    """
    if not use_local and "db_connection" in st.secrets and run_query is not None:
        try:
            df = run_query(f"SELECT * FROM {table_name};")
            st.info("Loaded data from Neon database ✅")
            return df
        except Exception as e:
            st.warning(f"Failed to query Neon DB: {e}\nFalling back to local CSV.")

    # Local CSV fallback
    try:
        df = pd.read_csv(local_csv)
        st.info("Loaded data from local CSV ✅")
        return df
    except FileNotFoundError:
        st.error("Local CSV not found. Please add it to your project folder.")
        return pd.DataFrame()  # empty DataFrame

