import random

import pandas as pd
import streamlit as st

from utils import load_data, page_header

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


st.set_page_config(layout="wide")


translations = {
    "en": {
        "page_title": "Mission Mode",
        "load_error": "Data could not be loaded. Please ensure the data file is available.",
        "loading_data": "Loading mission data...",
        "controls_header": "🎯 Mission Settings",
        "filter_by_class": "Focus Verb Class",
        "mode_label": "Mission Type",
        "mode_build": "Build the Verb",
        "mode_order": "Order the Verb",
        "mode_tone": "Tone Pair Hunt",
        "mode_bridge": "Bridge the Network",
        "mission_length": "Questions per mission",
        "mission_intro": "Practice one small skill at a time. Finish a short mission, check mistakes, and replay.",
        "mission_tip": "Best use: choose one class, play 6 to 10 questions, then replay your weak items.",
        "mode_build_hint": "Complete a two-character verb by choosing the missing partner character.",
        "mode_order_hint": "See two characters and decide which order makes the real verb.",
        "mode_tone_hint": "Match verbs to tone pairs without seeing pinyin in the answer choices.",
        "mode_bridge_hint": "Find the middle character that creates two real verbs and connects the network.",
        "start_mission": "Start New Mission",
        "score_label": "Score",
        "progress_label": "Question {current} of {total}",
        "answer_label": "Choose your answer",
        "check_answer": "Check Answer",
        "next_question": "Next Question",
        "select_answer_warning": "Choose an answer first.",
        "no_questions_match": "No mission questions matched the current filters. Broaden the class filter or change the mission type.",
        "correct_label": "Correct",
        "incorrect_label": "Not quite",
        "mission_complete": "Mission complete: {score}/{total}",
        "mistakes_header": "Review Mistakes",
        "mistakes_desc": "Replay this mission and focus on these items.",
        "no_mistakes": "Perfect round. Start another mission or change the focus.",
        "build_prompt_first": "Which character completes a real verb with {char} as the first character?",
        "build_prompt_second": "Which character completes a real verb with {char} as the second character?",
        "build_explanation": "{char1} + {char2} = {verb} · {pinyin} · {english}",
        "order_prompt": "Which order makes a real verb from these two characters: {char1} and {char2}?",
        "order_explanation": "The real verb is {verb} = {char1} + {char2} · {pinyin} · {english}",
        "tone_prompt": "Which verb matches the tone pair {pair}?",
        "tone_explanation": "{verb} has tone pair {pair} · {pinyin} · {english}",
        "bridge_prompt": "Which character connects {char1} and {char3} to form two real verbs?",
        "bridge_explanation": "{char1} + {middle} = {verb1} · {pinyin1}; {middle} + {char3} = {verb2} · {pinyin2}",
        "mission_summary_header": "Why This Helps",
        "mission_summary_body": "These missions turn the network into short drills: character combination, order, tone recognition, and bridge-building between word families.",
        "review_question": "Question",
        "review_correct": "Correct Answer",
        "review_yours": "Your Answer",
        "review_note": "Explanation",
    },
    "zh": {
        "page_title": "任务模式",
        "load_error": "无法加载数据。请确保数据文件可用。",
        "loading_data": "正在加载任务数据...",
        "controls_header": "🎯 任务设置",
        "filter_by_class": "聚焦动词类别",
        "mode_label": "任务类型",
        "mode_build": "组词挑战",
        "mode_order": "顺序挑战",
        "mode_tone": "声调模式挑战",
        "mode_bridge": "网络桥接挑战",
        "mission_length": "每轮题数",
        "mission_intro": "一次只练一个小技能。完成短任务，查看错题，再重玩。",
        "mission_tip": "推荐用法：选择一个类别，练 6 到 10 题，再重做你的薄弱项。",
        "mode_build_hint": "选择缺失的搭配字，完成一个双字动词。",
        "mode_order_hint": "看到两个汉字后，判断哪一个顺序才是真实动词。",
        "mode_tone_hint": "不看拼音，只根据声调模式判断正确动词。",
        "mode_bridge_hint": "找出中间汉字，让它形成两个真实动词，并把网络连接起来。",
        "start_mission": "开始新任务",
        "score_label": "得分",
        "progress_label": "第 {current} / {total} 题",
        "answer_label": "选择答案",
        "check_answer": "检查答案",
        "next_question": "下一题",
        "select_answer_warning": "请先选择一个答案。",
        "no_questions_match": "当前筛选下没有可用题目。请放宽类别筛选或更换任务类型。",
        "correct_label": "答对了",
        "incorrect_label": "还不对",
        "mission_complete": "任务完成：{score}/{total}",
        "mistakes_header": "错题回顾",
        "mistakes_desc": "重玩这一轮时，重点注意这些题。",
        "no_mistakes": "这一轮全对了。可以换一个任务继续练习。",
        "build_prompt_first": "哪一个汉字能和 {char} 组成一个真实动词，并且 {char} 是首字？",
        "build_prompt_second": "哪一个汉字能和 {char} 组成一个真实动词，并且 {char} 是尾字？",
        "build_explanation": "{char1} + {char2} = {verb} · {pinyin} · {english}",
        "order_prompt": "下面两个汉字中，哪一种顺序能组成真实动词：{char1} 和 {char2}？",
        "order_explanation": "真实动词是 {verb} = {char1} + {char2} · {pinyin} · {english}",
        "tone_prompt": "哪一个动词符合声调模式 {pair}？",
        "tone_explanation": "{verb} 的声调模式是 {pair} · {pinyin} · {english}",
        "bridge_prompt": "哪个汉字能连接 {char1} 和 {char3}，组成两个真实动词？",
        "bridge_explanation": "{char1} + {middle} = {verb1} · {pinyin1}；{middle} + {char3} = {verb2} · {pinyin2}",
        "mission_summary_header": "为什么这个模式有用",
        "mission_summary_body": "这些任务把网络数据变成短练习：组词、顺序判断、声调识别，以及词族之间的桥接。",
        "review_question": "题目",
        "review_correct": "正确答案",
        "review_yours": "你的答案",
        "review_note": "说明",
    },
}


MISSION_STATE_PREFIX = "mission_mode_"


def state_key(name: str) -> str:
    return f"{MISSION_STATE_PREFIX}{name}"


@st.cache_data(show_spinner=False)
def get_df():
    return load_data()


def parse_bilingual(text):
    if isinstance(text, str) and "(" in text and ")" in text:
        zh, en = text.split("(", 1)
        return zh.strip(), en.replace(")", "").strip()
    return text, text


def sample_records(records, count, rng):
    if not records:
        return []
    if len(records) >= count:
        return rng.sample(records, count)
    return [rng.choice(records) for _ in range(count)]


def unique_distractors(values, correct, k, rng):
    pool = sorted({value for value in values if pd.notna(value) and value != correct})
    if len(pool) <= k:
        return pool
    return rng.sample(pool, k)


def format_verb_option(row):
    return str(row["Verb"])


def build_build_questions(records, rounds, rng, T):
    questions = []
    char1_pool = [row["char1"] for row in records if row.get("char1")]
    char2_pool = [row["char2"] for row in records if row.get("char2")]

    for row in sample_records(records, rounds, rng):
        ask_second = rng.choice([True, False])
        if ask_second:
            prompt = T["build_prompt_first"].format(char=row["char1"])
            correct = row["char2"]
            distractors = unique_distractors(char2_pool, correct, 3, rng)
        else:
            prompt = T["build_prompt_second"].format(char=row["char2"])
            correct = row["char1"]
            distractors = unique_distractors(char1_pool, correct, 3, rng)

        options = distractors + [correct]
        options = list(dict.fromkeys(options))
        rng.shuffle(options)
        if len(options) < 2:
            continue

        questions.append(
            {
                "prompt": prompt,
                "correct": correct,
                "options": options,
                "explanation": T["build_explanation"].format(
                    char1=row["char1"],
                    char2=row["char2"],
                    verb=row["Verb"],
                    pinyin=row.get("pinyin", ""),
                    english=row.get("English_Verb", ""),
                ),
            }
        )
    return questions


def build_tone_questions(records, rounds, rng, T):
    questions = []
    for row in sample_records(records, rounds, rng):
        correct_label = format_verb_option(row)
        distractor_rows = [
            candidate for candidate in records
            if candidate.get("tone_pattern") != row.get("tone_pattern") and candidate.get("Verb") != row.get("Verb")
        ]
        distractors = [format_verb_option(candidate) for candidate in sample_records(distractor_rows, 3, rng)]
        options = distractors + [correct_label]
        options = list(dict.fromkeys(options))
        rng.shuffle(options)
        if len(options) < 2:
            continue

        questions.append(
            {
                "prompt": T["tone_prompt"].format(pair=row.get("tone_pattern", "")),
                "correct": correct_label,
                "options": options,
                "explanation": T["tone_explanation"].format(
                    verb=row["Verb"],
                    pair=row.get("tone_pattern", ""),
                    pinyin=row.get("pinyin", ""),
                    english=row.get("English_Verb", ""),
                ),
            }
        )
    return questions


def build_order_questions(records, rounds, rng, T):
    pair_map = {
        (row["char1"], row["char2"]): row
        for row in records
        if row.get("char1") and row.get("char2")
    }
    eligible = [
        row
        for (char1, char2), row in pair_map.items()
        if (char2, char1) not in pair_map
    ]
    questions = []

    for row in sample_records(eligible, rounds, rng):
        correct = f"{row['char1']}{row['char2']}"
        reverse = f"{row['char2']}{row['char1']}"
        options = [correct, reverse]
        rng.shuffle(options)

        questions.append(
            {
                "prompt": T["order_prompt"].format(char1=row["char1"], char2=row["char2"]),
                "correct": correct,
                "options": options,
                "explanation": T["order_explanation"].format(
                    verb=row["Verb"],
                    char1=row["char1"],
                    char2=row["char2"],
                    pinyin=row.get("pinyin", ""),
                    english=row.get("English_Verb", ""),
                ),
            }
        )
    return questions


def build_bridge_questions(records, rounds, rng, T):
    pair_map = {
        (row["char1"], row["char2"]): row
        for row in records
        if row.get("char1") and row.get("char2")
    }
    outgoing = {}
    middle_pool = sorted({char2 for _, char2 in pair_map.keys()})
    for char1, char2 in pair_map.keys():
        outgoing.setdefault(char1, set()).add(char2)

    bridge_candidates = {}
    for (char1, middle), first_row in pair_map.items():
        for char3 in outgoing.get(middle, set()):
            if char3 in {char1, middle} or (char1, char3) in pair_map:
                continue
            second_row = pair_map.get((middle, char3))
            if not second_row:
                continue
            endpoint_key = (char1, char3)
            bridge_candidates.setdefault(endpoint_key, []).append(
                {
                    "char1": char1,
                    "middle": middle,
                    "char3": char3,
                    "verb1": first_row.get("Verb", ""),
                    "verb2": second_row.get("Verb", ""),
                    "pinyin1": first_row.get("pinyin", ""),
                    "pinyin2": second_row.get("pinyin", ""),
                }
            )

    bridge_paths = [
        rows[0]
        for rows in bridge_candidates.values()
        if len({row["middle"] for row in rows}) == 1
    ]

    questions = []
    for row in sample_records(bridge_paths, rounds, rng):
        distractors = unique_distractors(middle_pool, row["middle"], 3, rng)
        options = distractors + [row["middle"]]
        options = list(dict.fromkeys(options))
        rng.shuffle(options)
        if len(options) < 2:
            continue

        questions.append(
            {
                "prompt": T["bridge_prompt"].format(char1=row["char1"], char3=row["char3"]),
                "correct": row["middle"],
                "options": options,
                "explanation": T["bridge_explanation"].format(
                    char1=row["char1"],
                    middle=row["middle"],
                    char3=row["char3"],
                    verb1=row["verb1"],
                    verb2=row["verb2"],
                    pinyin1=row["pinyin1"],
                    pinyin2=row["pinyin2"],
                ),
            }
        )
    return questions


def start_mission(records, mode, rounds, T):
    rng = random.Random()
    if mode == T["mode_build"]:
        questions = build_build_questions(records, rounds, rng, T)
    elif mode == T["mode_order"]:
        questions = build_order_questions(records, rounds, rng, T)
    elif mode == T["mode_bridge"]:
        questions = build_bridge_questions(records, rounds, rng, T)
    else:
        questions = build_tone_questions(records, rounds, rng, T)

    st.session_state[state_key("questions")] = questions
    st.session_state[state_key("index")] = 0
    st.session_state[state_key("score")] = 0
    st.session_state[state_key("checked")] = False
    st.session_state[state_key("results")] = []
    st.session_state[state_key("signature")] = (mode, rounds)
    st.session_state.pop(state_key("last_correct"), None)
    st.session_state.pop(state_key("last_selected"), None)


lang = language_selector()
T = translations[lang]
page_header(T["page_title"], "🎮")

with st.spinner(T["loading_data"]):
    df = get_df()
if df.empty:
    st.error(T["load_error"])
    st.stop()

if "Chinese_Verbs" in df.columns and "Verb" not in df.columns:
    df = df.rename(columns={"Chinese_Verbs": "Verb"})

if "分类（Classification）" in df.columns:
    df[["Classification_zh", "Classification_en"]] = df["分类（Classification）"].apply(
        lambda x: pd.Series(parse_bilingual(x))
    )
else:
    df["Classification_zh"] = None
    df["Classification_en"] = None

mission_df = df.dropna(subset=["char1", "char2", "Verb"]).copy()
class_col = "Classification_zh" if lang == "zh" else "Classification_en"

st.markdown(T["mission_intro"])
st.caption(T["mission_tip"])
st.info(T["mission_summary_body"])

st.sidebar.header(T["controls_header"])
available_classes = sorted(mission_df[class_col].dropna().unique()) if class_col in mission_df.columns else []
selected_classes = st.sidebar.multiselect(
    T["filter_by_class"],
    options=available_classes,
    default=available_classes,
)
if selected_classes:
    mission_df = mission_df[mission_df[class_col].isin(selected_classes)].copy()

mode = st.radio(
    T["mode_label"],
    options=[T["mode_build"], T["mode_order"], T["mode_tone"], T["mode_bridge"]],
    horizontal=True,
)
mode_hints = {
    T["mode_build"]: T["mode_build_hint"],
    T["mode_order"]: T["mode_order_hint"],
    T["mode_tone"]: T["mode_tone_hint"],
    T["mode_bridge"]: T["mode_bridge_hint"],
}
st.caption(mode_hints.get(mode, ""))
rounds = st.slider(T["mission_length"], min_value=5, max_value=12, value=8, step=1)

records = mission_df[["Verb", "pinyin", "English_Verb", "char1", "char2", "tone_pattern"]].drop_duplicates().to_dict("records")

signature = (mode, rounds, tuple(selected_classes), lang)
if (
    state_key("questions") not in st.session_state
    or st.session_state.get(state_key("signature")) != signature
):
    start_mission(records, mode, rounds, T)
    st.session_state[state_key("signature")] = signature

top_col1, top_col2 = st.columns([1, 1])
with top_col1:
    st.metric(T["score_label"], st.session_state.get(state_key("score"), 0))
with top_col2:
    if st.button(T["start_mission"], use_container_width=True):
        start_mission(records, mode, rounds, T)
        st.session_state[state_key("signature")] = signature
        st.rerun()

questions = st.session_state.get(state_key("questions"), [])
if not questions:
    st.warning(T["no_questions_match"])
    st.stop()

index = st.session_state.get(state_key("index"), 0)
score = st.session_state.get(state_key("score"), 0)
checked = st.session_state.get(state_key("checked"), False)
question = questions[index]
answer_key = state_key(f"answer_{index}")

st.progress(index / max(1, len(questions)), text=T["progress_label"].format(current=index + 1, total=len(questions)))
st.subheader(question["prompt"])
st.radio(T["answer_label"], options=question["options"], index=None, key=answer_key)

if not checked:
    if st.button(T["check_answer"], use_container_width=False):
        selected = st.session_state.get(answer_key)
        if not selected:
            st.warning(T["select_answer_warning"])
        else:
            is_correct = selected == question["correct"]
            st.session_state[state_key("checked")] = True
            st.session_state[state_key("last_correct")] = is_correct
            st.session_state[state_key("last_selected")] = selected
            st.session_state[state_key("score")] = score + int(is_correct)
            st.session_state[state_key("results")].append(
                {
                    T["review_question"]: question["prompt"],
                    T["review_correct"]: question["correct"],
                    T["review_yours"]: selected,
                    T["review_note"]: question["explanation"],
                    "is_correct": is_correct,
                }
            )
            st.rerun()
else:
    if st.session_state.get(state_key("last_correct")):
        st.success(T["correct_label"])
    else:
        st.error(T["incorrect_label"])
    st.info(question["explanation"])

    if index < len(questions) - 1:
        if st.button(T["next_question"], use_container_width=False):
            st.session_state[state_key("index")] = index + 1
            st.session_state[state_key("checked")] = False
            st.rerun()
    else:
        final_score = st.session_state.get(state_key("score"), 0)
        st.success(T["mission_complete"].format(score=final_score, total=len(questions)))
        mistake_rows = [row for row in st.session_state.get(state_key("results"), []) if not row["is_correct"]]
        if mistake_rows:
            st.subheader(T["mistakes_header"])
            st.caption(T["mistakes_desc"])
            review_df = pd.DataFrame(mistake_rows).drop(columns=["is_correct"])
            st.dataframe(review_df, use_container_width=True, hide_index=True)
        else:
            st.info(T["no_mistakes"])
