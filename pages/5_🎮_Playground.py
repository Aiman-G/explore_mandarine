import streamlit as st
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from utils import page_header, load_data
import random

# ============================
# Page Config
# ============================
st.set_page_config(layout="wide", page_title="🎮 Verb Playground")

# ============================
# Translations (EN/ZH)
# ============================
I18N = {
    'en': {
        'title': "Verb Playground",
        'settings': "⚙️ Settings",
        'lang_select': "Select Language",
        'study': "🧠 Study",
        'study_tip': "Pick strong pivots (high degree). Click characters to add/remove them from your Practice List.",
        'top_starters': "Top Starters (as first char)",
        'top_enders': "Top Enders (as second char)",
        'char_explorer': "Character Explorer",
        'pick_char': "Pick a character",
        'as_start': "As Starter (A→•)",
        'as_end': "As Ender (•→B)",
        'add_pivot': "Add to Practice List",
        'remove_pivot': "Remove from Practice List",
        'practice_list': "Practice List",
        'play': "🎮 Play",
        'play_desc': "Connect the pivot with one option to form a valid verb.",
        'mode': "Game Mode",
        'mode_start': "Start Mode (pick second char)",
        'mode_end': "End Mode (pick first char)",
        'mode_mix': "Mixed",
        'opts_count': "Options per round",
        'lives': "Lives",
        'start_game': "Start New Game",
        'next_round': "Next Round",
        'skip_round': "Skip",
        'score': "Score",
        'streak': "Streak",
        'accuracy': "Accuracy",
        'attempts': "Attempts",
        'pivot': "Pivot",
        'choose_char': "Choose a character:",
        'correct': "Correct! +1",
        'wrong': "Oops! −1",
        'near_miss_reverse': "Near miss: BA exists, not AB",
        'no_valid_answers': "No valid answers for this pivot. Picking a new pivot…",
        'formed_table': "Formed Verbs (learning artifact)",
        'download_csv': "Download CSV",
        'game_over': "Game Over",
        'empty_data': "No data available.",
        'classification': "Semantic Class",
    },
    'zh': {
        'title': "动词游乐场",
        'settings': "⚙️ 设置",
        'lang_select': "选择语言",
        'study': "🧠 学习",
        'study_tip': "先选择高连接度的枢纽字。点击汉字加入/移出练习单。",
        'top_starters': "高起始字（作首字）",
        'top_enders': "高收尾字（作尾字）",
        'char_explorer': "汉字浏览",
        'pick_char': "选择一个汉字",
        'as_start': "作为首字 (A→•)",
        'as_end': "作为尾字 (•→B)",
        'add_pivot': "加入练习单",
        'remove_pivot': "移出练习单",
        'practice_list': "练习单",
        'play': "🎮 练习",
        'play_desc': "将枢纽字与选项连接，若构成动词则得分。",
        'mode': "模式",
        'mode_start': "首字模式（选第二个字）",
        'mode_end': "尾字模式（选第一个字）",
        'mode_mix': "混合",
        'opts_count': "每轮选项数",
        'lives': "生命",
        'start_game': "开始新游戏",
        'next_round': "下一轮",
        'skip_round': "跳过",
        'score': "分数",
        'streak': "连击",
        'accuracy': "准确率",
        'attempts': "尝试次数",
        'pivot': "枢纽字",
        'choose_char': "请选择：",
        'correct': "正确！+1",
        'wrong': "可惜！−1",
        'near_miss_reverse': "差一点：存在 BA，不是 AB",
        'no_valid_answers': "该枢纽没有可连词，自动更换…",
        'formed_table': "已生成的动词（学习成果）",
        'download_csv': "下载 CSV",
        'game_over': "游戏结束",
        'empty_data': "没有可用数据。",
        'classification': "语义类别",
    }
}

# ============================
# Helpers
# ============================

def ensure_cols(df: pd.DataFrame) -> pd.DataFrame:
    if 'Chinese_Verbs' in df.columns and 'Verb' not in df.columns:
        df = df.rename(columns={'Chinese_Verbs':'Verb'})
    for col in ['char1','char2','Verb','pinyin','English_Verb']:
        if col not in df.columns:
            df[col] = None
    return df


def parse_bilingual(text):
    if isinstance(text, str) and '(' in text and ')' in text:
        parts = text.split('(')
        zh, en = parts[0], parts[1].replace(')', '')
        return zh.strip(), en.strip()
    return text, text


def build_tables(df: pd.DataFrame):
    # aggregate by edge (char1,char2) to one example verb (+ class)
    cols = ['char1','char2','Verb','pinyin','English_Verb']
    if 'Classification_zh' in df.columns and 'Classification_en' in df.columns:
        cols += ['Classification_zh','Classification_en']
    tmp = df[cols].dropna(subset=['char1','char2']).copy()
    tmp['count'] = 1
    agg = { 'count':'sum','Verb':'first','pinyin':'first','English_Verb':'first' }
    if 'Classification_zh' in tmp.columns:
        agg['Classification_zh'] = 'first'; agg['Classification_en'] = 'first'
    edges = (tmp.groupby(['char1','char2'], as_index=False).agg(agg))

    # adjacency
    forward = defaultdict(list)
    reverse = defaultdict(list)
    for _, r in edges.iterrows():
        rec = {
            'other': r['char2'], 'verb': r['Verb'], 'pinyin': r['pinyin'], 'english': r['English_Verb'], 'count': int(r['count']),
            'cls_zh': r.get('Classification_zh'), 'cls_en': r.get('Classification_en')
        }
        forward[r['char1']].append(rec)
        rec2 = {
            'other': r['char1'], 'verb': r['Verb'], 'pinyin': r['pinyin'], 'english': r['English_Verb'], 'count': int(r['count']),
            'cls_zh': r.get('Classification_zh'), 'cls_en': r.get('Classification_en')
        }
        reverse[r['char2']].append(rec2)

    # degrees
    out_deg = edges.groupby('char1')['char2'].nunique().to_dict()
    in_deg  = edges.groupby('char2')['char1'].nunique().to_dict()
    all_chars = set(list(out_deg.keys()) + list(in_deg.keys()))
    degree = {c: out_deg.get(c,0) + in_deg.get(c,0) for c in all_chars}
    return edges, forward, reverse, out_deg, in_deg, degree


def pick_top_series(d: dict, n=20):
    if not d:
        return pd.DataFrame({'char':[], 'deg':[]})
    s = pd.Series(d).sort_values(ascending=False).head(n)
    return s.reset_index().rename(columns={'index':'char',0:'deg'})


def build_round(state, lang):
    """Create one round based on current mode, practice pivots and data."""
    L = I18N[lang]
    rng = random.Random(state.get('seed', 42))
    mode = state.get('mode','start')

    # candidate pivot pool
    pivot_pool = list(state['pivots']) if state['pivots'] else list(state['degree_sorted'])[:50]
    if not pivot_pool:
        state['round_msg'] = L['empty_data']
        state['current'] = None
        return

    # choose mode if mixed
    mode_used = rng.choice(['start','end']) if mode == 'mix' else mode

    # try a few pivots to ensure valid answers
    for _ in range(50):
        pivot = rng.choice(pivot_pool)
        if mode_used == 'start':
            valid = state['forward'].get(pivot, [])
            valid_set = {v['other'] for v in valid}
        else:
            valid = state['reverse'].get(pivot, [])
            valid_set = {v['other'] for v in valid}
        if len(valid_set) > 0:
            break
    else:
        state['round_msg'] = L['no_valid_answers']
        state['current'] = None
        return

    # Build options list
    opts_target = state.get('opts_count', 8)
    n_valid = min(max(2, opts_target//3), len(valid_set))
    valid_choices = rng.sample(list(valid_set), n_valid)

    # decoys: reversed-only + random none-edges
    decoys = set()
    all_chars = state['all_chars']
    if mode_used == 'start':
        reversed_only = {x['other'] for x in state['reverse'].get(pivot, [])} - valid_set
    else:
        reversed_only = {x['other'] for x in state['forward'].get(pivot, [])} - valid_set
    rev_pick = rng.sample(list(reversed_only), min(len(reversed_only), max(1, opts_target//4))) if reversed_only else []
    decoys.update(rev_pick)

    # random decoys without edge in current direction
    while len(valid_choices) + len(decoys) < opts_target:
        c = rng.choice(list(all_chars))
        if c == pivot or c in valid_set or c in decoys:
            continue
        decoys.add(c)

    options = list(valid_choices) + list(decoys)
    rng.shuffle(options)

    # stash round
    state['current'] = {
        'pivot': pivot,
        'mode_used': mode_used,
        'options': options,
        'valid_set': valid_set
    }
    state['round_msg'] = None


def handle_choice(state, choice, lang):
    L = I18N[lang]
    cur = state.get('current')
    if not cur:
        return
    pivot = cur['pivot']
    mode_used = cur['mode_used']
    valid_set = cur['valid_set']

    state['attempts'] += 1

    correct = choice in valid_set
    if correct:
        state['score'] += 1
        state['streak'] += 1
        # append formed verb row with semantic class
        if mode_used == 'start':
            recs = state['forward'].get(pivot, [])
            example = next((r for r in recs if r['other']==choice), None)
            verb = example['verb'] if example else f"{pivot}{choice}"
            pinyin = example['pinyin'] if example else ''
            eng = example['english'] if example else ''
            cls = example.get('cls_zh') if lang=='zh' else example.get('cls_en') if example else ''
            row = {'char1': pivot, 'char2': choice, 'Verb': verb, 'pinyin': pinyin, 'English_Verb': eng, 'Mode': 'Start', 'Classification': cls}
        else:
            recs = state['reverse'].get(pivot, [])
            example = next((r for r in recs if r['other']==choice), None)
            verb = example['verb'] if example else f"{choice}{pivot}"
            pinyin = example['pinyin'] if example else ''
            eng = example['english'] if example else ''
            cls = example.get('cls_zh') if lang=='zh' else example.get('cls_en') if example else ''
            row = {'char1': choice, 'char2': pivot, 'Verb': verb, 'pinyin': pinyin, 'English_Verb': eng, 'Mode': 'End', 'Classification': cls}
        state['formed'].append(row)
        state['feedback'] = (True, L['correct'], row)
    else:
        state['score'] -= 1
        state['streak'] = 0
        state['lives'] -= 1
        # near miss if reversed exists
        reversed_ok = False
        if mode_used == 'start':
            reversed_ok = any(choice == r['other'] for r in state['reverse'].get(pivot, []))
        else:
            reversed_ok = any(choice == r['other'] for r in state['forward'].get(pivot, []))
        msg = L['wrong'] + (f" — {L['near_miss_reverse']}" if reversed_ok else "")
        state['feedback'] = (False, msg, None)


# ============================
# Load & Prepare Data
# ============================
@st.cache_data
def get_df():
    return load_data()

df_raw = get_df()
if df_raw is None or df_raw.empty:
    st.error("No data.")
    st.stop()

df = ensure_cols(df_raw.copy())

# Bilingual classification
if '分类（Classification）' in df.columns:
    df[['Classification_zh', 'Classification_en']] = df['分类（Classification）'].apply(lambda x: pd.Series(parse_bilingual(x)))

# Build everything once (no teacher filters)
edges, forward, reverse, out_deg, in_deg, degree = build_tables(df)
all_chars = set(list(degree.keys()))

# ============================
# Init session state
# ============================
if 'game' not in st.session_state:
    st.session_state['game'] = {}
state = st.session_state['game']

# Static maps into state
state['forward'] = forward
state['reverse'] = reverse
state['all_chars'] = all_chars
state['degree_sorted'] = [c for c,_ in sorted(degree.items(), key=lambda kv:-kv[1])]

# Practice list
if 'pivots' not in state:
    state['pivots'] = set()

# Game vars
state.setdefault('mode','start')
state.setdefault('opts_count', 8)
state.setdefault('lives', 3)
state.setdefault('score', 0)
state.setdefault('streak', 0)
state.setdefault('attempts', 0)
state.setdefault('formed', [])  # list of dicts
state.setdefault('seed', 42)
state.setdefault('current', None)
state.setdefault('round_msg', None)
state.setdefault('feedback', None)

# Sidebar: language only (no teacher controls)
st.sidebar.header(I18N['en']['settings'] + " / " + I18N['zh']['settings'])
lang_options = {'English': 'en', '中文 (Chinese)': 'zh'}
selected_lang_display = st.sidebar.radio("Select Language / 选择语言", options=lang_options.keys(), horizontal=True)
lang = lang_options[selected_lang_display]
L = I18N[lang]

page_header(L['title'], "🎮")

# ============================
# STUDY EXPANDER
# ============================
with st.expander(L['study'], expanded=True):
    st.caption(L['study_tip'])
    colA, colB = st.columns(2)
    with colA:
        st.subheader(L['top_starters'])
        top_out = pick_top_series(out_deg, n=20)
        for _, r in top_out.iterrows():
            c = r['char']; deg = int(r['deg'])
            cols = st.columns([2,1])
            with cols[0]:
                st.write(f"**{c}**  · out={deg}  · in={in_deg.get(c,0)}")
            with cols[1]:
                if c in state['pivots']:
                    if st.button(f"− {L['remove_pivot']}", key=f"rm_start_{c}"):
                        state['pivots'].discard(c)
                else:
                    if st.button(f"+ {L['add_pivot']}", key=f"add_start_{c}"):
                        state['pivots'].add(c)
    with colB:
        st.subheader(L['top_enders'])
        top_in = pick_top_series(in_deg, n=20)
        for _, r in top_in.iterrows():
            c = r['char']; deg = int(r['deg'])
            cols = st.columns([2,1])
            with cols[0]:
                st.write(f"**{c}**  · in={deg}  · out={out_deg.get(c,0)}")
            with cols[1]:
                if c in state['pivots']:
                    if st.button(f"− {L['remove_pivot']}", key=f"rm_end_{c}"):
                        state['pivots'].discard(c)
                else:
                    if st.button(f"+ {L['add_pivot']}", key=f"add_end_{c}"):
                        state['pivots'].add(c)

    st.markdown(f"**{L['practice_list']}:** " + ("、".join(sorted(state['pivots'])) if state['pivots'] else "—"))

    st.subheader(L['char_explorer'])
    char_options = sorted(list(all_chars))
    sel_char = st.selectbox(L['pick_char'], options=['']+char_options)
    if sel_char:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{L['as_start']}**")
            starts = pd.DataFrame(state['forward'].get(sel_char, []))
            if not starts.empty:
                starts = starts.rename(columns={'other':'char2','verb':'Verb','pinyin':'pinyin','english':'English_Verb','count':'freq','cls_zh':'Classification_zh','cls_en':'Classification_en'})
                disp_cls = 'Classification_zh' if lang=='zh' else 'Classification_en'
                cols = ['char2','Verb','pinyin','English_Verb','freq', disp_cls] if disp_cls in starts.columns else ['char2','Verb','pinyin','English_Verb','freq']
                st.dataframe(starts[cols].head(50), use_container_width=True)
            else:
                st.info('—')
        with c2:
            st.markdown(f"**{L['as_end']}**")
            ends = pd.DataFrame(state['reverse'].get(sel_char, []))
            if not ends.empty:
                ends = ends.rename(columns={'other':'char1','verb':'Verb','pinyin':'pinyin','english':'English_Verb','count':'freq','cls_zh':'Classification_zh','cls_en':'Classification_en'})
                disp_cls = 'Classification_zh' if lang=='zh' else 'Classification_en'
                cols = ['char1','Verb','pinyin','English_Verb','freq', disp_cls] if disp_cls in ends.columns else ['char1','Verb','pinyin','English_Verb','freq']
                st.dataframe(ends[cols].head(50), use_container_width=True)
            else:
                st.info('—')
        col_add = st.columns([1,3])[0]
        with col_add:
            if sel_char in state['pivots']:
                if st.button(f"− {L['remove_pivot']}", key=f"rm_sel_{sel_char}"):
                    state['pivots'].discard(sel_char)
            else:
                if st.button(f"+ {L['add_pivot']}", key=f"add_sel_{sel_char}"):
                    state['pivots'].add(sel_char)

# ============================
# PLAY EXPANDER
# ============================
with st.expander(L['play'], expanded=False):
    st.caption(L['play_desc'])
    c1,c2,c3,c4,c5,c6 = st.columns([1.3,1,1,1,1,1])
    with c1:
        state['mode'] = st.selectbox(L['mode'], options=['start','end','mix'], format_func=lambda x: { 'start':L['mode_start'], 'end':L['mode_end'], 'mix':L['mode_mix']}[x], index=0)
    with c2:
        state['opts_count'] = st.slider(L['opts_count'], min_value=4, max_value=12, value=8, step=2)
    with c3:
        state['lives'] = st.number_input(L['lives'], min_value=1, max_value=10, value=int(state.get('lives',3)))
    with c4:
        if st.button(L['start_game']):
            # reset game
            state['score'] = 0
            state['streak'] = 0
            state['attempts'] = 0
            state['formed'] = []
            state['feedback'] = None
            # build first round
            build_round(state, lang)
    with c5:
        if st.button(L['next_round']):
            state['feedback'] = None
            build_round(state, lang)
    with c6:
        if st.button(L['skip_round']):
            state['feedback'] = None
            build_round(state, lang)

    # Scoreboard
    colS, colT, colA, colL = st.columns(4)
    correct_n = len(state['formed'])
    acc = (state['attempts'] and f"{(correct_n/state['attempts']*100):.0f}%") or "—"
    colS.metric(L['score'], state['score'])
    colT.metric(L['streak'], state['streak'])
    colA.metric(L['accuracy'], acc)
    colL.metric(L['lives'], state['lives'])

    st.divider()

    # Round area
    cur = state.get('current')
    if state.get('lives',0) <= 0:
        st.subheader(f"🛑 {L['game_over']}")
    elif cur is None:
        st.info(state.get('round_msg') or L['empty_data'])
    else:
        st.subheader(f"{L['pivot']}: {cur['pivot']}")
        st.caption({ 'start': L['mode_start'], 'end': L['mode_end'] }[cur['mode_used']])

        # Options as buttons (grid)
        opts = cur['options']
        ncols = 4
        rows = (len(opts) + ncols - 1)//ncols
        idx = 0
        for _ in range(rows):
            cols = st.columns(ncols)
            for c in cols:
                if idx < len(opts):
                    val = opts[idx]
                    if c.button(val, key=f"opt_{idx}"):
                        handle_choice(state, val, lang)
                    idx += 1
        # Feedback
        if state.get('feedback'):
            ok, msg, row = state['feedback']
            if ok:
                st.success(msg)
                if row:
                    dfrow = pd.DataFrame([row])
                    st.table(dfrow[['Verb','pinyin','English_Verb','Classification','char1','char2','Mode']])
            else:
                st.error(msg)

    # Formed verbs table (learning artifact)
    st.subheader(L['formed_table'])
    formed_df = pd.DataFrame(state['formed'])
    if formed_df.empty:
        st.info('—')
    else:
        cols = ['Verb','pinyin','English_Verb','Classification','char1','char2','Mode']
        keep = [c for c in cols if c in formed_df.columns]
        st.dataframe(formed_df[keep], use_container_width=True)
        st.download_button(L['download_csv'], formed_df[keep].to_csv(index=False).encode('utf-8'), file_name='formed_verbs.csv', mime='text/csv')
