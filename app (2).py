import streamlit as st
import json
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 오행 영양소 추천 데이터 불러오기
def load_oheng_data():
    with open("oheng_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 질병 기반 추천 사전 정의
def get_disease_recommendations(disease_list, medications):
    disease_reco_map = {
        "고혈압": ["칼륨", "마그네슘", "코엔자임 Q10"],
        "당뇨": ["크롬", "마그네슘", "오메가3"],
        "신장질환": ["비타민 D", "오메가3"],
        "심장질환": ["코엔자임 Q10", "타우린"],
        "난청": ["비타민 B12", "아연", "오메가3"],
        "아토피피부염": ["비타민 E", "프로바이오틱스", "감마리놀렌산"],
        "천식": ["비타민 C", "오메가3", "마그네슘"],
        "정신질환": ["비타민 B군", "오메가3", "마그네슘"]
    }
    recommendations = set()
    for disease in disease_list:
        recommendations.update(disease_reco_map.get(disease, []))
    return sorted(list(recommendations))

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

def get_birth_season(birth_date):
    month = birth_date.month
    if month in [3, 4, 5]:
        return "봄"
    elif month in [6, 7, 8]:
        return "여름"
    elif month in [9, 10, 11]:
        return "가을"
    else:
        return "겨울"

def generate_interpretation(name, gender, oheng, survey, bmi, season):
    lines = []
    lines.append(f"🔮 {name}({gender})님의 사주는 '{oheng}'의 기운을 중심으로 하며, 출생 계절은 '{season}'입니다.\n")

    # [생략: 오행 기반 분석 내용 — 이전과 동일]

    lines.append("\n💊 [8] 체질 보완을 위한 추천 영양소")
    oheng_data = load_oheng_data()
    nutrients = oheng_data.get(oheng, {}).get("부족", {}).get("영양소", [])
    explanation = {
        "비타민 B군": "피로 회복, 에너지 대사, 신경 안정",
        "아연": "면역 기능 강화, 상처 회복, 간 기능 보조",
        "L-카르니틴": "지방 연소, 피로감 감소",
        "코엔자임 Q10": "심혈관 건강, 세포 에너지 생성",
        "마그네슘": "근육 이완, 스트레스 완화, 혈압 조절",
        "타우린": "간 해독, 심장 기능 안정",
        "프로바이오틱스": "장 건강, 면역력 향상",
        "효소": "소화 촉진, 영양소 흡수 보조",
        "비타민 B1": "당 대사, 신경 기능 유지",
        "비타민 C": "항산화 작용, 면역력 강화",
        "비타민 D": "뼈 건강, 면역 기능",
        "오메가3": "혈중 콜레스테롤 개선, 염증 억제",
        "비타민 E": "세포 보호, 노화 방지",
        "셀레늄": "항산화, 갑상선 기능 보조"
    }
    for n in nutrients:
        desc = explanation.get(n, "신체 균형을 위한 필수 영양소")
        lines.append(f"- {n}: {desc}")

    return "\n".join(lines)

def send_email(recipient_email, subject, message):
    try:
        sender_email = "audiso.seo@gmail.com"
        sender_password = "tjdudwns00!!"  # 보안 이슈로 서버에서는 별도 환경변수 처리 권장
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception:
        return False

# 🖥️ Streamlit UI
st.set_page_config(page_title="사주 건강 예측", layout="centered")
st.title("🌿 내 몸에 맞는 건강관리, 내 사주에 물어보세요")

st.subheader("👤 기본 정보 입력")
name = st.text_input("이름")
gender = st.radio("성별", ["남성", "여성"])
birth_date = st.date_input("생년월일", datetime(1993, 3, 29), min_value=datetime(1940, 1, 1))
height = st.number_input("키 (cm)", 100, 250, 170)
weight = st.number_input("몸무게 (kg)", 30, 200, 70)
bmi = weight / ((height / 100) ** 2)

st.subheader("🩺 건강 설문 (20문항)")
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
    "수분부족": st.checkbox("물을 거의 마시지 않음"),
    "스트레스": st.checkbox("스트레스를 자주 느낌"),
    "피부트러블": st.checkbox("피부 트러블이 자주 생김"),
    "감기잦음": st.checkbox("감기에 자주 걸림"),
    "눈피로": st.checkbox("눈의 피로가 잦음"),
    "손발차가움": st.checkbox("손발이 잘 차가움"),
    "두통": st.checkbox("두통을 자주 느낌"),
    "변비": st.checkbox("변비 증상이 있음"),
    "설사": st.checkbox("설사를 자주 함"),
    "체중변화": st.checkbox("체중 변화가 큼"),
    "무기력": st.checkbox("무기력함을 자주 느낌")
}

# 질병 및 약물 입력 추가
st.subheader("🧬 질환 정보 및 복용 약")
disease_options = ["고혈압", "당뇨", "신장질환", "심장질환", "난청", "아토피피부염", "천식", "정신질환"]
selected_diseases = st.multiselect("진단받은 질환을 선택하세요", disease_options)
medications = st.text_area("복용 중인 약을 입력해주세요 (선택)")

if st.button("🔍 분석 및 추천하기"):
    oheng = analyze_oheng_by_year(birth_date.year)
    season = get_birth_season(birth_date)
    explanation = generate_interpretation(name, gender, oheng, survey, bmi, season)
    st.subheader("📘 사주 건강 분석 결과")
    st.text(explanation)

    # 추가: 질병 기반 영양소 추천
    if selected_diseases:
        st.subheader("💊 질병 기반 추천 영양소")
        disease_recos = get_disease_recommendations(selected_diseases, medications)
        if disease_recos:
            st.markdown("해당 질환을 고려한 맞춤 영양소 추천 목록:")
            for nutrient in disease_recos:
                st.markdown(f"- {nutrient}")
        else:
            st.markdown("해당 질환에 대한 영양소 추천 데이터가 없습니다.")

    st.markdown("---")
    st.markdown("[🛍️ 건강 보청기 솔루션 제안 — xr.audiso.co.kr](https://xr.audiso.co.kr)")
    st.markdown("---")

    email_address = st.text_input("📧 결과를 이메일로 받아보시겠어요? 이메일 주소를 입력해주세요.")
    if st.button("📨 이메일 전송하기"):
        if email_address:
            if send_email(email_address, "사주 건강 분석 결과", explanation):
                st.success("✅ 이메일이 성공적으로 전송되었습니다!")
            else:
                st.error("❌ 이메일 전송에 실패했습니다. 설정을 확인해주세요.")
        else:
            st.warning("⚠️ 이메일 주소를 입력해주세요.")
