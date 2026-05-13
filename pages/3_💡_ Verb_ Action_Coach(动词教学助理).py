import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import page_header, load_data
from i18n.verb_action_coach import TRANSLATIONS as TX

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


# =========================
# Sidebar: language
# =========================
lang = language_selector()

PAGE_FALLBACKS = {
    "en": {
        "tab_overview": "🚀 Quick Start",
        "tab_heatmap": "🗺️ Tone Priorities",
        "tab_coverage": "🎯 Coverage Planner",
        "tab_deck": "🗂️ Practice Set Builder",
        "tab_pitfalls": "🚩 Confusion Alerts",
        "insight_total_verbs": "Two-char verbs",
        "insight_top_tone": "Top tone pair",
        "insight_top_category": "Main category",
        "quickstart_header": "Why This Page Helps",
        "learner_card_title": "For learners",
        "learner_card_body": "See which characters unlock the most verbs, spot the main tone patterns, and build small practice sets instead of memorizing random lists.",
        "teacher_card_title": "For teachers",
        "teacher_card_body": "Use the page to choose high-coverage characters, organize pronunciation targets, and export fast lesson material from the dataset.",
        "starter_pack_header": "Starter Pack",
        "starter_pack_desc": "Pick a small number of characters and see how many verbs they unlock.",
        "starter_pack_size": "How many starter characters?",
        "starter_pack_chars": "Suggested characters",
        "starter_pack_coverage": "Verb coverage",
        "starter_pack_preview": "Suggested starter verbs",
        "starter_pack_download": "Download starter pack (CSV)",
        "loading_data": "Loading coach data...",
    },
    "zh": {
        "tab_overview": "🚀 快速开始",
        "tab_heatmap": "🗺️ 声调重点",
        "tab_coverage": "🎯 覆盖规划",
        "tab_deck": "🗂️ 练习清单生成",
        "tab_pitfalls": "🚩 易混提醒",
        "insight_total_verbs": "双字动词数",
        "insight_top_tone": "最高频声调模式",
        "insight_top_category": "主要类别",
        "quickstart_header": "这页为什么有用",
        "learner_card_title": "对学习者",
        "learner_card_body": "帮助你看清哪些汉字最值得先学、哪些声调模式最常见，并快速生成一小组可练习的动词，而不是背随机词表。",
        "teacher_card_title": "对教师",
        "teacher_card_body": "帮助你选择高覆盖率汉字、确定发音重点，并快速导出可直接用于课堂的词表材料。",
        "starter_pack_header": "起步清单",
        "starter_pack_desc": "选择少量汉字，看看它们能解锁多少动词。",
        "starter_pack_size": "起步汉字数量",
        "starter_pack_chars": "推荐汉字",
        "starter_pack_coverage": "动词覆盖率",
        "starter_pack_preview": "推荐起步动词",
        "starter_pack_download": "下载起步清单（CSV）",
        "loading_data": "正在加载教学助理数据...",
    },
}

T = {
    **PAGE_FALLBACKS["en"],
    **TX.get("en", {}),
    **PAGE_FALLBACKS.get(lang, {}),
    **TX.get(lang, {}),
}

page_header(T["title"], "💡")

# =========================
# Load + prepare data
# =========================
@st.cache_data(show_spinner=False)
def get_df():
    return load_data()

with st.spinner(T["loading_data"]):
    df = get_df()
if df is None or df.empty:
    st.error(T["load_error"])
    st.stop()

# Parse bilingual classification "中文(English)"
def parse_bilingual(text):
    if isinstance(text, str) and "(" in text and ")" in text:
        zh, en = text.split("(", 1)
        en = en.replace(")", "")
        return zh.strip(), en.strip()
    return text, text

if "Chinese_Verbs" in df.columns and "Verb" not in df.columns:
    df = df.rename(columns={"Chinese_Verbs":"Verb"})

if "分类（Classification）" in df.columns:
    df[["Classification_zh","Classification_en"]] = df["分类（Classification）"].apply(
        lambda x: pd.Series(parse_bilingual(x))
    )
    classification_col_display = "Classification_zh" if lang == "zh" else "Classification_en"
else:
    classification_col_display = None

# Tone pair helpers
def split_tone_pair(tp: str):
    try:
        a,b = str(tp).split("-")
        return int(a), int(b)
    except Exception:
        return None, None

if "tone_pattern" in df.columns:
    df["tone_pattern"] = df["tone_pattern"].astype(str)
    df["src_tone"], df["dst_tone"] = zip(*df["tone_pattern"].map(split_tone_pair))
else:
    df["tone_pattern"] = None
    df["src_tone"] = None
    df["dst_tone"] = None

# Edge-level table (unique AB with one example row)
edge_cols = [
    "char1","char2","Verb","pinyin","English_Verb","tone_pattern","src_tone","dst_tone",
    "initial_1","final_1","initial_2","final_2","Classification_zh","Classification_en"
]
edge_cols = [c for c in edge_cols if c in df.columns]
edge_df = df[edge_cols].dropna(subset=["char1","char2"]).drop_duplicates()


@st.cache_data(show_spinner=False)
def build_starter_pack(edge_df: pd.DataFrame, k_max: int):
    edges = edge_df[["char1", "char2", "Verb", "pinyin", "English_Verb"]].drop_duplicates().reset_index(drop=True)
    edges["edge_id"] = edges["char1"] + "|" + edges["char2"]

    uncovered = set(edges["edge_id"])
    selected = []

    while len(selected) < k_max and uncovered:
        counts = {}
        for _, row in edges.iterrows():
            edge_id = row["edge_id"]
            if edge_id not in uncovered:
                continue
            for ch in (row["char1"], row["char2"]):
                counts[ch] = counts.get(ch, 0) + 1
        if not counts:
            break
        best = max(counts.items(), key=lambda kv: kv[1])[0]
        selected.append(best)
        newly_covered = edges[(edges["char1"] == best) | (edges["char2"] == best)]["edge_id"].tolist()
        uncovered -= set(newly_covered)

    covered = set(edges["edge_id"]) - uncovered
    covered_verbs = edges[edges["edge_id"].isin(covered)].drop(columns=["edge_id"]).reset_index(drop=True)
    coverage_pct = 100 * len(covered) / max(1, len(edges))
    return selected, coverage_pct, covered_verbs

# =========================
# Tabs
# =========================
TAB_OV, TAB_COV, TAB_DECK = st.tabs([
    T["tab_overview"],
    T["tab_coverage"],
    T["tab_deck"],
])

# =========================
# Tab 1 — Overview
# =========================
with TAB_OV:
    st.header(T["tab_overview"])
    with st.expander(T["ov_help_title"], expanded=False):
        st.markdown(T["ov_help_body"])

    total_verbs = int(len(edge_df))
    top_tone = "—"
    if "tone_pattern" in edge_df.columns and not edge_df["tone_pattern"].dropna().empty:
        top_tone = edge_df["tone_pattern"].value_counts().idxmax()
    top_category = "—"
    if classification_col_display and classification_col_display in df.columns and not df[classification_col_display].dropna().empty:
        top_category = df[classification_col_display].value_counts().idxmax()

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric(T["insight_total_verbs"], total_verbs)
    metric2.metric(T["insight_top_tone"], top_tone)
    metric3.metric(T["insight_top_category"], top_category)

    st.subheader(T["quickstart_header"])
    card_col1, card_col2 = st.columns(2)
    with card_col1:
        st.markdown(
            f"""
            <div style="background:#f8fafc;border:1px solid #dbeafe;border-radius:16px;padding:16px 18px;height:100%;">
              <div style="font-weight:700;font-size:1.02rem;margin-bottom:0.45rem;color:#1d4ed8;">{T["learner_card_title"]}</div>
              <div style="line-height:1.55;color:#0f172a;">{T["learner_card_body"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with card_col2:
        st.markdown(
            f"""
            <div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:16px;padding:16px 18px;height:100%;">
              <div style="font-weight:700;font-size:1.02rem;margin-bottom:0.45rem;color:#c2410c;">{T["teacher_card_title"]}</div>
              <div style="line-height:1.55;color:#431407;">{T["teacher_card_body"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader(T["starter_pack_header"])
    st.caption(T["starter_pack_desc"])
    starter_size = st.slider(T["starter_pack_size"], min_value=5, max_value=25, value=8, step=1)
    starter_chars, starter_coverage, starter_verbs = build_starter_pack(edge_df, starter_size)
    pack_col1, pack_col2 = st.columns([1, 1.2])
    with pack_col1:
        st.metric(T["starter_pack_coverage"], f"{starter_coverage:.1f}%")
        st.write("**" + T["starter_pack_chars"] + "**")
        st.write("、".join(starter_chars) if lang == "zh" else ", ".join(starter_chars))
    with pack_col2:
        st.write("**" + T["starter_pack_preview"] + "**")
        st.dataframe(starter_verbs.head(20), use_container_width=True, hide_index=True, height=280)
    st.download_button(
        T["starter_pack_download"],
        starter_verbs.to_csv(index=False).encode("utf-8"),
        file_name="starter_pack.csv",
        mime="text/csv",
    )

    # Category Distribution
    st.divider()
    st.subheader(T["cat_dist"])
    st.caption(T["cat_desc"])
    if classification_col_display and classification_col_display in df.columns:
        cat_counts = df[classification_col_display].value_counts(dropna=True).reset_index()
        cat_counts.columns = [classification_col_display, "count"]
        fig_cat = px.bar(
            cat_counts,
            x="count",
            y=classification_col_display,
            orientation="h",
            labels={"count": T["verb_count"], classification_col_display: T["category"]},
        )
        fig_cat.update_layout(yaxis={"categoryorder":"total ascending"})
        st.plotly_chart(fig_cat, use_container_width=True)
    else:
        st.info(T["no_data"] if "no_data" in T else "No data.")

    st.divider()

    # Phonetic Breakdown
    st.subheader(T["phon_header"])
    st.caption(T["phon_desc"])
    col1, col2 = st.columns(2)

    def freq_chart(series, title):
        if series is None or series.name not in df.columns:
            st.info(T["no_data"] if "no_data" in T else "No data.")
            return
        freq = df[series.name].value_counts().nlargest(15).reset_index()
        if freq.empty:
            st.info(T["no_data"] if "no_data" in T else "No data.")
            return
        freq.columns = ["component","count"]
        fig = px.bar(
            freq, x="count", y="component", orientation="h",
            labels={"count": T["frequency"], "component": T["component"]}, title=title
        )
        fig.update_layout(yaxis={"categoryorder":"total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    with col1:
        if "initial_1" in df.columns: freq_chart(df["initial_1"], T["initial_1"])
        if "initial_2" in df.columns: freq_chart(df["initial_2"], T["initial_2"])
    with col2:
        if "final_1" in df.columns: freq_chart(df["final_1"], T["final_1"])
        if "final_2" in df.columns: freq_chart(df["final_2"], T["final_2"])

# =========================
# Tab 2 — Coverage Optimizer
# =========================
with TAB_COV:
    st.header(T["cov_header"])
    with st.expander(T["cov_help_title"], expanded=False):
        st.markdown(T["cov_help_body"])
    st.caption(T["cov_caption"])

    if edge_df.empty:
        st.info(T["no_data"] if "no_data" in T else "No data.")
    else:
        k_max = st.slider(T["cov_how_many"], min_value=5, max_value=300, value=15, step=5)

        edges = edge_df[["char1","char2","Verb","pinyin","English_Verb"]].drop_duplicates().reset_index(drop=True)
        edges["edge_id"] = edges["char1"] + "|" + edges["char2"]

        uncovered = set(edges["edge_id"])
        selected = []
        # Greedy set cover by characters
        while len(selected) < k_max and uncovered:
            counts = {}
            # count coverage per character over currently uncovered edges
            for _, r in edges.iterrows():
                eid = r["edge_id"]
                if eid not in uncovered:
                    continue
                for ch in (r["char1"], r["char2"]):
                    counts[ch] = counts.get(ch, 0) + 1
            if not counts:
                break
            best = max(counts.items(), key=lambda kv: kv[1])[0]
            selected.append(best)
            newly = edges[(edges["char1"]==best) | (edges["char2"]==best)]["edge_id"].tolist()
            uncovered -= set(newly)

        covered = set(edges["edge_id"]) - uncovered
        coverage_pct = 100 * len(covered) / max(1, len(edges))

        colA, colB = st.columns(2)
        with colA:
            st.metric(T["cov_selected"], len(selected))
            st.write("**" + T["cov_list_prefix"] + "** " + ("、".join(selected) if selected else "—"))
        with colB:
            st.metric(T["cov_coverage"], f"{coverage_pct:.1f}%")
            st.caption(f"{T['cov_verbs_covered']}: {len(covered)} / {len(edges)}")

        covered_verbs = edges[edges["edge_id"].isin(covered)].drop(columns=["edge_id"])
        st.dataframe(covered_verbs, use_container_width=True, height=340)
        st.download_button(
            T["cov_download"],
            covered_verbs.to_csv(index=False).encode("utf-8"),
            file_name="covered_verbs.csv",
            mime="text/csv"
        )

# =========================
# Tab 3 — Deck Builder
# =========================
with TAB_DECK:
    st.header(T["deck_header"])
    with st.expander(T["deck_help_title"], expanded=False):
        st.markdown(T["deck_help_body"])

    if edge_df.empty:
        st.info(T["no_data"] if "no_data" in T else "No data.")
    else:
        # Tone pairs
        tone_opts = sorted(edge_df["tone_pattern"].dropna().unique().tolist()) if "tone_pattern" in edge_df.columns else []
        tone_pick = st.multiselect(T["deck_tone_pairs"], options=tone_opts, default=tone_opts[:6] if tone_opts else [])

        # Position & components
        pos_opts = [T["deck_any"], T["deck_first_init"], T["deck_first_final"], T["deck_second_init"], T["deck_second_final"]]
        pos_choice = st.selectbox(T["deck_position"], options=pos_opts)

        def comp_col_from_choice(choice: str):
            if choice in (T["deck_first_init"],):
                return "initial_1"
            if choice in (T["deck_first_final"],):
                return "final_1"
            if choice in (T["deck_second_init"],):
                return "initial_2"
            if choice in (T["deck_second_final"],):
                return "final_2"
            return None

        comp_col = comp_col_from_choice(pos_choice)
        comp_choices = sorted(edge_df[comp_col].dropna().unique().tolist()) if comp_col and comp_col in edge_df.columns else []
        components = st.multiselect(T["deck_components"], options=comp_choices, default=[])

        deck_size = st.slider(T["deck_size"], 10, 200, 40, 5)

        # Build deck
        deck = edge_df.copy()
        if tone_pick:
            deck = deck[deck["tone_pattern"].isin(tone_pick)]
        if comp_col and components:
            deck = deck[deck[comp_col].isin(components)]

        if deck.empty:
            st.info(T["deck_no_items"])
        else:
            # Weight by frequency in raw df (how often AB occurs)
            freq = df.groupby(["char1","char2"]).size().rename("f").reset_index()
            deck = deck.merge(freq, on=["char1","char2"], how="left")
            deck["f"] = deck["f"].fillna(1)

            k = min(deck_size, len(deck))
            # weighted sample without replacement
            deck = deck.sample(n=k, weights=deck["f"], replace=False, random_state=42)

            keep_cols = ["Verb","pinyin","English_Verb","tone_pattern","char1","char2"]
            if "Classification_zh" in deck.columns and "Classification_en" in deck.columns:
                deck["Classification"] = deck["Classification_zh"] if lang=="zh" else deck["Classification_en"]
                keep_cols.append("Classification")

            deck = deck[keep_cols].reset_index(drop=True)

            st.dataframe(deck, use_container_width=True, height=340)
            st.download_button(
                T["deck_download"],
                deck.to_csv(index=False).encode("utf-8"),
                file_name="study_deck.csv",
                mime="text/csv"
            )
