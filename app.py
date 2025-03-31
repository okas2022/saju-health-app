# app.py
import streamlit as st
import json
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar
import openai
import os

# GPT API Key 설정 (환경 변수 또는 직접 입력)
openai.api_key = os.getenv("OPENAI_API_KEY")

# 오행-영양소 매핑 데이터 로드
def load_oheng_data():
    with open("oheng_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 사주 오행 분석 (년간 기준)
def analyze_oheng_by_year(year):
    stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    stem = stems[(year - 4) % 10]
    if stem in ['갑', '을']:
        return "목"
    elif stem in ['병', '정']:
        return "화"
    elif stem in ['무', '기']:
        return "토"
    elif stem in ['경', '신']:
        return "금"
    else:
        return "수"

# 영양소 추천 함수
def recommend_nutrients(oheng_element, balance, bmi):
    oheng_data = load_oheng_data()
    element_data = oheng_data.get(oheng_element, {}).get(balance)
    if not element_data:
        return []
    base = element_data["영양소"]
    if bmi >= 25:
        base.append("체중관리 보조 성분: CLA, 녹차추출물")
    elif bmi < 18.5:
        base.append("체중 증가 지원: 단백질, 아연")
    return list(set(base))

# GPT 해석 생성 함수
def generate_gpt_interpretation(name, gender, oheng, survey, nutrients, bmi):
    survey_summary = ", ".join([k for k, v in survey.items() if v])
    prompt = f"""
당신은 전통 사주와 건강 분석을 결합한 AI 건강 상담사입니다.
사용자의 이름은 {name}, 성별은 {gender}, 주요 오행은 {oheng}입니다.
BMI는 {bmi:.1f}로 건강 상태 판단에 참고해야 합니다.
사용자의 건강 설문 응답 중 체크된 항목은 다음과 같습니다: {survey_summary}.
AI가 추천한 영양소는 {', '.join(nutrients)}입니다.

1. 위 정보를 기반으로 2025년 올해의 건강 상태를 예측하고 조언해 주세요.
2. 2026년 내년의 건강 흐름과 주의해야 할 점을 포함해 설명해 주세요.
3. 종합적으로 5줄 이상의 건강 분석 및 영양제 추천 이유를 자연스럽게 작성해주세요.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 사주와 건강을 융합하여 맞춤형 건강 예측과 영양제를 설명하는 AI 상담사입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT 응답 중 오류 발생: {str(e)}"

# Streamlit 앱 시작
st.set_page_config(page_title="사주 건강 영양제 추천", layout="centered")
st.title("🌿 사주 기반 건강 예측 및 영양제 추천 앱")

# 사용자 기본 정보
st.subheader("👤 기본 정보 입력")
name = st.text_input("이름을 입력하세요")
gender = st.radio("성별을 선택하세요", options=["남성", "여성"])
birth_date = st.date_input("생년월일 선택", value=datetime(1993, 3,
