
# app.py (최신 Streamlit UI 포함)
import streamlit as st
import json
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar

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

# 간단한 해석 생성 함수
def generate_interpretation(name, gender, oheng, survey, bmi):
    saju_intro = (
        "사주(四柱)는 사람이 태어난 연도, 월, 일, 시를 기준으로 하는 네 개의 기둥을 의미하며, "
        "각 기둥은 천간과 지지로 구성되어 있습니다. 이를 통해 총 여덟 글자로 이루어진 팔자(八字)를 구성하게 됩니다.
"
        "이 사주팔자를 바탕으로 개인의 타고난 기질, 성격, 인생 흐름, 건강 상태 등을 분석할 수 있습니다.
"
        "특히 건강 측면에서는 사주의 오행 구성과 균형이 중요한 역할을 하며, 어떤 오행이 강하거나 약한지를 통해 질병의 경향성을 유추할 수 있습니다.
"
        "사주팔자는 단순한 운세를 넘어서, 동양의학과 접목되어 개인 맞춤형 건강 관리에도 응용되고 있습니다.

"
        f"{name}({gender})님의 사주는 '{oheng}' 오행이 주로 나타납니다.
"
        "오행은 동양 철학에서 만물을 구성하는 다섯 가지 기본 요소로, 사람의 체질과 성향에도 깊은 영향을 미친다고 여겨집니다.
"
        f"'{oheng}' 오행은 신체 장기 중 특정 부분과 기능을 상징하며, 사람의 성격, 에너지 흐름, 건강 상태에 밀접하게 연관됩니다.
"
        "예를 들어 '목(木)'은 간과 근육, '화(火)'는 심장과 혈액순환, '토(土)'는 위장과 소화기관, '금(金)'은 폐와 면역, '수(水)'는 신장과 뇌와 연관됩니다.
"
        "또한, 특정 오행이 강하거나 약한 경우, 성향이나 질병 발생 경향이 나타날 수 있습니다.
"
        f"'{oheng}'의 특성은 다음과 같습니다:
"
    )

    if oheng == "목":
        saju_intro += "- 창의적이고 진취적인 성향을 보이며 간 기능 및 스트레스에 민감할 수 있습니다.
"
    elif oheng == "화":
        saju_intro += "- 열정적이며 외향적인 기질이 강하고 심혈관계 질환에 주의가 필요합니다.
"
    elif oheng == "토":
        saju_intro += "- 균형감각이 뛰어나며 소화기 건강에 영향을 많이 받습니다.
"
    elif oheng == "금":
        saju_intro += "- 이성적이고 분석적이며 폐와 면역 시스템의 취약 여부를 고려해야 합니다.
"
    elif oheng == "수":
        saju_intro += "- 내향적이고 직관적이며 신장 기능과 정신 건강에 민감할 수 있습니다.
"

    saju_intro += (
        "오행의 균형은 사람마다 다르며, 특정 오행이 부족하거나 과할 경우 건강에 영향을 줄 수 있습니다.
"
        "이에 따라 영양제도 오행의 기운을 보완하는 방향으로 추천됩니다.
"
        "이제 건강 설문과 신체 정보(BMI 등)를 바탕으로 건강 분석을 진행하겠습니다.

"
    )

    result = saju_intro
    result += f"현재 BMI는 {bmi:.1f}로 "
    if bmi < 18.5:
        result += "저체중에 해당하며 영양소 흡수나 체력 유지에 주의가 필요합니다.
"
    elif bmi >= 25:
        result += "과체중 또는 비만 범주에 속해 생활습관 개선이 요구됩니다.
"
    else:
        result += "정상 범위로 보이며 건강 관리를 유지하는 것이 중요합니다.
"

    health_flags = [k for k, v in survey.items() if v]
    if health_flags:
        result += "건강 설문에서 다음과 같은 항목에 체크하셨습니다: " + ", ".join(health_flags) + "
"
        result += "이로 미루어 볼 때, 전반적인 피로 또는 만성질환 관리가 중요할 수 있습니다.
"
    else:
        result += "건강 설문 항목에서 특별한 이상은 보고되지 않았습니다.
"

    result += "2025년은 체내 에너지 균형과 관련된 문제가 나타날 수 있어 스트레스 관리가 중요하고,
"
    result += "2026년은 면역력 약화와 소화기 계통의 변화에 유의해야 할 시기입니다.
"
    result += "영양소 섭취는 해당 오행과 건강 상태를 고려해 선택하는 것이 바람직합니다."
    return result

# Streamlit UI 구성
st.set_page_config(page_title="사주 기반 건강 분석 및 영양제 추천", layout="centered")
st.title("🌿 사주 기반 건강 예측 및 영양제 추천")

st.subheader("👤 기본 정보 입력")
name = st.text_input("이름")
gender = st.radio("성별", ["남성", "여성"])
birth_date = st.date_input("생년월일", value=datetime(1990, 1, 1), min_value=datetime(1940, 1, 1), max_value=datetime(2025, 12, 31))
time_hour = st.number_input("태어난 시간 (0~23시)", min_value=0, max_value=23, value=12)
height = st.number_input("키 (cm)", min_value=100, max_value=250, value=170)
weight = st.number_input("몸무게 (kg)", min_value=30, max_value=200, value=65)
bmi = weight / ((height / 100) ** 2)

st.subheader("🩺 건강 관련 설문")
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

if st.button("🔍 분석 및 추천하기"):
    saju_oheng = analyze_oheng_by_year(birth_date.year)
    balance_type = "부족"
    nutrients = recommend_nutrients(saju_oheng, balance_type, bmi)
    result = generate_interpretation(name, gender, saju_oheng, survey, bmi)

    st.subheader("📖 사주 기반 건강 해석")
    st.text(result)

    if nutrients:
        st.subheader("💊 추천 영양소")
        for item in nutrients:
            st.markdown(f"- {item}")
    else:
        st.info("추천할 영양소가 충분하지 않습니다.")
