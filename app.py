# app.py
import streamlit as st
import json
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar

# 오행-영양소 매핑 데이터 로드 (JSON 파일 불러오기)
def load_oheng_data():
    with open("oheng_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 사주 오행 간단 분석 (년간지만 기준으로 간단화)
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
def recommend_nutrients(oheng_element, balance, survey_data):
    oheng_data = load_oheng_data()
    element_data = oheng_data.get(oheng_element, {}).get(balance)
    if not element_data:
        return []

    base = element_data["영양소"]
    return list(set(base))

# Streamlit UI 시작
st.set_page_config(page_title="사주 건강 영양제 추천", layout="centered")
st.title("🌿 사주 기반 건강 영양제 추천 앱")

# 사용자 입력
col1, col2 = st.columns(2)
with col1:
    birth_date = st.date_input("생년월일을 선택하세요", value=datetime(1993, 3, 29))
with col2:
    time_hour = st.number_input("태어난 시간 (0~23시)", min_value=0, max_value=23, value=12)

st.subheader("📝 건강 설문")
fatigue = st.checkbox("자주 피로함")
sleep = st.checkbox("수면 부족 또는 불면증")
digest = st.checkbox("소화불량 또는 장트러블")

if st.button("분석 및 추천하기"):
    saju_oheng = analyze_oheng_by_year(birth_date.year)

    st.success(f"당신의 주 오행은 '{saju_oheng}' 입니다.")

    # 예시: 부족하다고 가정 (실제 앱은 오행 균형 분석 로직 추가 필요)
    balance_type = "부족"

    # 설문 정보
    survey = {
        "피로": fatigue,
        "수면": sleep,
        "소화": digest
    }

    nutrients = recommend_nutrients(saju_oheng, balance_type, survey)

    if nutrients:
        st.subheader("🔍 추천 영양 성분")
        for n in nutrients:
            st.markdown(f"- {n}")
    else:
        st.warning("추천할 영양소가 충분하지 않습니다. 입력 정보를 확인하세요.")