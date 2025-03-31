# app.py (OpenAI legacy version compatible)
import streamlit as st
import json
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar
import openai

# OpenAI API 키 직접 입력 (주의: 테스트용)
openai.api_key="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"

# 오행-영양소 매핑 데이터 로드
def load_oheng_data():
    with open("oheng_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 사주 오행 분석
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

# 영양소 추천
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

# GPT 해석 생성 함수 (legacy)
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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 사주와 건강을 융합하여 맞춤형 건강 예측과 영양제를 설명하는 AI 상담사입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"GPT 응답 중 오류 발생: {str(e)}"

# Streamlit 앱
st.set_page_config(page_title="사주 건강 영양제 추천", layout="centered")
st.title("🌿 사주 기반 건강 예측 및 영양제 추천 앱")

# 사용자 입력
st.subheader("👤 기본 정보 입력")
name = st.text_input("이름을 입력하세요")
gender = st.radio("성별을 선택하세요", options=["남성", "여성"])
birth_date = st.date_input("생년월일 선택", value=datetime(1993, 3, 29), min_value=datetime(1940, 1, 1), max_value=datetime(2025, 12, 31))
time_hour = st.number_input("태어난 시간 (0~23시)", min_value=0, max_value=23, value=12)
height = st.number_input("키(cm)", min_value=100, max_value=250, value=170)
weight = st.number_input("체중(kg)", min_value=30, max_value=200, value=70)
bmi = weight / ((height / 100) ** 2)

# 건강 설문
st.subheader("📝 건강 설문")
survey = {
    "피로": st.checkbox("자주 피로함"),
    "수면": st.checkbox("수면 부족 또는 불면증"),
    "소화": st.checkbox("소화불량 또는 장트러블"),
    "고혈압": st.checkbox("고혈압 병력 있음"),
    "당뇨": st.checkbox("당뇨 병력 있음"),
    "신장": st.checkbox("신장 질환 있음"),
    "심장": st.checkbox("심장 질환 있음"),
    "뇌": st.checkbox("뇌 질환 있음"),
    "운동부족": st.checkbox("운동을 거의 하지 않음"),
    "수분부족": st.checkbox("물을 거의 마시지 않음")
}

# 실행
if st.button("분석 및 추천하기"):
    saju_oheng = analyze_oheng_by_year(birth_date.year)
    balance_type = "부족"
    nutrients = recommend_nutrients(saju_oheng, balance_type, bmi)

    st.subheader("🔍 GPT 건강 예측 및 해석")
    explanation = generate_gpt_interpretation(name, gender, saju_oheng, survey, nutrients, bmi)
    st.markdown(explanation)

    if nutrients:
        st.subheader("💊 추천 영양 성분")
        for n in nutrients:
            st.markdown(f"- {n}")
    else:
        st.warning("추천할 영양소가 충분하지 않습니다.")
