import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import page_header, load_data
from i18n.verb_action_coach import TRANSLATIONS as TX




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
st.sidebar.header(f"{TX['en']['settings']} / {TX['zh']['settings']}")
lang_options = {"English":"en", "中文 (Chinese)":"zh"}
lang = st.sidebar.radio("Select Language / 选择语言", options=list(lang_options.keys()), horizontal=True)
lang = lang_options[lang]
T = TX[lang]

page_header(T["title"], "💡")

# =========================
# Load + prepare data
# =========================
@st.cache_data
def get_df():
    return load_data()

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

# =========================
# Tabs
# =========================
TAB_OV, TAB_HM, TAB_COV, TAB_DECK, TAB_PIT = st.tabs([
    T["tab_overview"],
    T["tab_heatmap"],
    T["tab_coverage"],
    T["tab_deck"],
    T["tab_pitfalls"],
])

# =========================
# Tab 1 — Overview
# =========================
with TAB_OV:
    st.header(T["tab_overview"])
    with st.expander(T["ov_help_title"], expanded=False):
        st.markdown(T["ov_help_body"])

    # Category Distribution
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
# Tab 2 — Tone Heatmap
# =========================
with TAB_HM:
    st.header(T["hm_header"])
    with st.expander(T["hm_help_title"], expanded=False):
        st.markdown(T["hm_help_body"])

    if edge_df.empty or "src_tone" not in edge_df.columns or "dst_tone" not in edge_df.columns:
        st.info(T["no_data"] if "no_data" in T else "No data.")
    else:
        cats = [T["hm_all"]]
        if classification_col_display and classification_col_display in edge_df.columns:
            cats += sorted(edge_df[classification_col_display].dropna().unique().tolist())
        cat_choice = st.selectbox(T["hm_cat"], options=cats)
        sub = edge_df.copy()
        if cat_choice != T["hm_all"] and classification_col_display:
            sub = sub[sub[classification_col_display] == cat_choice]

        # 5×5 matrix src→dst
        idx = pd.MultiIndex.from_product([range(1,6), range(1,6)], names=["src_tone","dst_tone"])
        mat = (
            sub.dropna(subset=["src_tone","dst_tone"])
               .groupby(["src_tone","dst_tone"]).size()
               .reindex(idx, fill_value=0).unstack(fill_value=0)
        )
        fig_hm = px.imshow(
            mat.values,
            x=[1,2,3,4,5], y=[1,2,3,4,5], text_auto=True, aspect="equal",
            labels=dict(x="dst tone", y="src tone", color="count"),
        )
        st.plotly_chart(fig_hm, use_container_width=True)

# =========================
# Tab 3 — Coverage Optimizer
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
# Tab 4 — Deck Builder
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

# =========================
# Tab 5 — Polyphony & Pitfalls
# =========================
with TAB_PIT:
    st.header(T["pit_header"])
    with st.expander(T["pit_help_title"], expanded=False):
        st.markdown(T["pit_help_body"])

    if df.empty:
        st.info(T["no_data"] if "no_data" in T else "No data.")
    else:
        col1, col2 = st.columns(2)

        # Polyphony: distinct tone roles per character
        if "src_tone" in df.columns and "dst_tone" in df.columns:
            poly_src = df.groupby("char1")["src_tone"].nunique(dropna=True).rename("src_var")
            poly_dst = df.groupby("char2")["dst_tone"].nunique(dropna=True).rename("dst_var")
            poly = pd.concat([poly_src, poly_dst], axis=1).fillna(0).astype(int)
            poly["polyphony"] = poly["src_var"] + poly["dst_var"]
            poly_chars = poly[poly["polyphony"] >= 3].sort_values("polyphony", ascending=False).head(40)
            with col1:
                st.caption(T["pit_poly_caption"])
                st.dataframe(poly_chars, use_container_width=True, height=360)
        else:
            with col1:
                st.info(T["no_data"] if "no_data" in T else "No data.")

        # 3→3 sandhi list
        with col2:
            if "tone_pattern" in df.columns:
                sandhi = df[df["tone_pattern"] == "3-3"][["Verb","pinyin","English_Verb"]].drop_duplicates().head(80)
                st.caption(T["pit_sandhi_caption"])
                if sandhi.empty:
                    st.info(T["no_data"] if "no_data" in T else "No data.")
                else:
                    st.dataframe(sandhi, use_container_width=True, height=360)
            else:
                st.info(T["no_data"] if "no_data" in T else "No data.")