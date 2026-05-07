import streamlit as st
import random
from kiwipiepy import Kiwi

# Kiwi 초기화
@st.cache_resource
def load_kiwi():
    return Kiwi()

kiwi = load_kiwi()

def generate_therapy_sentences(user_input):
    ending = user_input.strip().replace('-', '')
    
    logic_db = {
        "원인/결과": {
            "endings": ["아서", "어서", "니까", "니"],
            "scenarios": [
                ("배가 고프", "VA", " 밥을 많이 먹었어요."),
                ("비가 많이 오", "VV", " 장화를 신고 나가요."),
                ("날씨가 너무 춥", "VA", " 두꺼운 외투를 입으세요."),
                ("몸이 좋지 않", "VA", " 집에서 푹 쉬고 있어요."),
                ("목이 너무 마르", "VA", " 시원한 물을 마십니다."),
                ("밤이 아주 깊", "VA", " 이제 잠을 자야겠어요."),
                ("밖이 너무 시끄럽", "VA", " 창문을 꼭 닫았습니다.")
            ]
        },
        "관찰/반응": {
            "endings": ["길래", "더니"],
            "scenarios": [
                ("친구가 사탕을 먹", "VV", " 저도 하나 달라고 했어요."),
                ("아이가 환하게 웃", "VV", " 저도 기분이 좋아졌습니다."),
                ("맛있는 냄새가 나", "VV", " 주방으로 가보았어요."),
                ("동생이 잠을 자", "VV", " 조용히 문을 닫아주었습니다."),
                ("길에 예쁜 꽃이 피", "VV", " 멈춰서 사진을 찍었어요.")
            ]
        },
        "목적/의도": {
            "endings": ["려고", "으려고", "러", "으러", "고자"],
            "scenarios": [
                ("사과를 맛있게 씻", "VV", " 주방으로 갔어요."),
                ("잠을 시원하게 자", "VV", " 선풍기를 켰습니다."),
                ("친구를 즐겁게 만나", "VV", " 놀이터에서 기다려요."),
                ("좋은 책을 읽", "VV", " 도서관에 방문했습니다."),
                ("손을 깨끗이 씻", "VV", " 화장실로 들어갑니다.")
            ]
        },
        "단순나열": {
            "endings": ["고", "다가", "며", "면서"],
            "scenarios": [
                ("밥을 다 먹", "VV", " 깨끗하게 양치를 해요."),
                ("숙제를 다 하", "VV", " 장난감을 가지고 놀아요."),
                ("노래를 부르", "VV", " 신나게 춤을 춥니다."),
                ("외출복을 입", "VV", " 운동화를 신어요."),
                ("텔레비전을 보", "VV", " 맛있는 과일을 먹었습니다.")
            ]
        }
    }

    selected_scenarios = []
    category_label = "미분류"
    for label, content in logic_db.items():
        if ending in content["endings"]:
            selected_scenarios = content["scenarios"]
            category_label = label
            break
    if not selected_scenarios:
        selected_scenarios = logic_db["단순나열"]["scenarios"]
        category_label = "기본(나열)"

    samples = random.sample(selected_scenarios, min(3, len(selected_scenarios)))
    results = []
    for stem, tag, suffix in samples:
        try:
            tokens = [(stem, tag), (ending, "EC")]
            combined = kiwi.join(tokens)
            if "ㅂ어" in combined or "ㅂ아" in combined:
                if "춥" in stem: combined = combined.replace("춥어", "추워")
                if "시끄럽" in stem: combined = combined.replace("시끄럽어", "시끄러워")
            if "고프어" in combined: combined = combined.replace("고프어", "고파")
            results.append(f"{combined}{suffix}")
        except: continue
    return results, category_label

# 화면 구성
st.set_page_config(page_title="언어치료 도우미", page_icon="🏥")
st.title("🏥 언어치료용 문장 생성기")
st.info("연습하고 싶은 '어미'를 입력하면 올바른 활용형 문장을 생성합니다.")

target = st.text_input("연습할 어미를 입력하세요 (예: 아서, 니까, 려고)", key="input")

if target:
    generated_sentences, cat = generate_therapy_sentences(target)
    st.markdown(f"### 📌 분석 결과: **{cat}** 유형")
    for i, sent in enumerate(generated_sentences, 1):
        st.success(f"{i}. {sent}")
