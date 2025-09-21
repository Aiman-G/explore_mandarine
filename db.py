# db.py
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

# Only create engine if secret exists
if "db_connection" in st.secrets:
    CONN_STR = st.secrets["db_connection"]
    engine = create_engine(CONN_STR, pool_pre_ping=True)
else:
    engine = None  # fallback, local CSV will be used

def run_query(query: str) -> pd.DataFrame:
    if engine is None:
        st.error("No database connection found. Using local CSV instead.")
        return pd.DataFrame()  # empty DataFrame fallback
    with engine.connect() as conn:
        return pd.read_sql(query, conn)
