
import streamlit as st
import json
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_oheng_data():
    with open("oheng_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

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
    lines.append(f"🔮 {name}({gender})님의 사주는 '{oheng}'의 기운을 중심으로 형성되어 있으며, 출생 계절은 '{season}'입니다.\n")

    lines.append("🧭 [1] 사주로 본 성격, 운세, 직업, 애정운")
    if oheng == "목":
        lines.append("- 🌳 목(木): 창의력과 성장의 기운을 타고났습니다. 독립적이고 도전정신이 강한 성향입니다.")
        lines.append("- 🔮 운세상 끊임없이 배움과 성장을 추구하며, 환경 변화에 민감합니다.")
        lines.append("- 💼 적합 직업: 기획자, 연구자, 교육자, 예술가 등 자유롭고 창의적인 분야")
        lines.append("- ❤️ 애정운: 깊은 관계를 추구하나 고집이 있어 충돌이 있을 수 있음")
    elif oheng == "화":
        lines.append("- 🔥 화(火): 열정과 추진력의 기운을 타고났습니다. 활발하고 리더십이 뛰어난 타입입니다.")
        lines.append("- 🔮 운세상 빠른 결정과 실행력으로 기회를 얻지만, 조급함은 주의해야 합니다.")
        lines.append("- 💼 적합 직업: 마케팅, 영업, 정치, 연예계 등 외향적이고 경쟁적인 분야")
        lines.append("- ❤️ 애정운: 열정적이지만 감정 기복이 있어 상대를 지치게 할 수도 있음")
    elif oheng == "토":
        lines.append("- 🪵 토(土): 균형감각과 책임감이 뛰어납니다. 실용적이고 신뢰받는 성향입니다.")
        lines.append("- 🔮 운세상 안정적 삶을 추구하며, 한 분야에서 오래 머무는 힘이 있습니다.")
        lines.append("- 💼 적합 직업: 공무원, 금융, 행정, 보건 등 안정성과 실용성이 중요한 분야")
        lines.append("- ❤️ 애정운: 신중하고 배려심 많으며, 따뜻한 파트너십을 선호함")
    elif oheng == "금":
        lines.append("- ⚔️ 금(金): 이성적이며 논리적인 성향입니다. 규율을 중시하고 목표지향적입니다.")
        lines.append("- 🔮 운세상 승부욕이 강하고, 냉철하게 기회를 분석하는 능력이 뛰어납니다.")
        lines.append("- 💼 적합 직업: 법률, 분석, 기술, 데이터 기반 업종")
        lines.append("- ❤️ 애정운: 표현이 적고 직설적이지만, 진심은 깊습니다.")
    else:  # 수
        lines.append("- 💧 수(水): 감성적이고 통찰력이 뛰어납니다. 상상력이 풍부하고 신중합니다.")
        lines.append("- 🔮 운세상 흐름을 잘 읽는 유연한 운명이나, 우유부단함이 단점일 수 있습니다.")
        lines.append("- 💼 적합 직업: 상담, 심리, 예술, 글쓰기, 교육 등 내면 탐구형 분야")
        lines.append("- ❤️ 애정운: 감성적이고 섬세하나 상처를 쉽게 받을 수 있어 조심스러움")

    lines.append("\n🩺 [2] 사주에 따른 건강 분석")
    if oheng == "목":
        lines.append("- 간과 근육 건강이 핵심이며, 스트레스가 쌓이면 간 기능 저하에 취약합니다.")
    elif oheng == "화":
        lines.append("- 심장, 혈압, 순환계 질환 가능성이 높고, 과로에 취약합니다.")
    elif oheng == "토":
        lines.append("- 위장, 비장과 관련된 소화기계 건강을 꾸준히 관리해야 합니다.")
    elif oheng == "금":
        lines.append("- 폐, 기관지 건강이 약할 수 있으며, 알레르기나 호흡기 문제에 민감합니다.")
    else:  # 수
        lines.append("- 신장, 방광, 뇌 관련 건강에 주의하며, 수분 섭취와 감정기복 관리가 중요합니다.")

    lines.append("\n📋 [3] 설문 및 체질 반영 건강 결론")
    lines.append(f"- 현재 BMI: {bmi:.1f}")
    if bmi < 18.5:
        lines.append("  → 저체중: 체력과 면역력 강화가 필요합니다.")
    elif bmi >= 25:
        lines.append("  → 과체중: 대사 증후군 예방을 위한 체중 감량 권장")
    else:
        lines.append("  → 정상체중: 유지와 체력 관리 중요")

    flags = [k for k, v in survey.items() if v]
    if flags:
        lines.append(f"- 설문에서 주의가 필요한 건강 이슈: {', '.join(flags)}")
    else:
        lines.append("- 설문에서는 건강상 특별한 이상은 나타나지 않았습니다.")

    lines.append("\n🛡️ [4] 건강관리 요령")
    if oheng == "목":
        lines.append("- 규칙적인 수면, 스트레스 완화, 간 건강 영양소가 중요합니다.")
    elif oheng == "화":
        lines.append("- 심장 강화 운동, 항산화 식단, 혈압 관리가 핵심입니다.")
    elif oheng == "토":
        lines.append("- 식사 습관 개선, 위장에 부담 없는 음식, 장건강 프로바이오틱스 활용")
    elif oheng == "금":
        lines.append("- 유산소 운동, 폐 기능 강화, 비염/알레르기 예방에 주력")
    else:
        lines.append("- 수분 섭취 늘리기, 신장 보호, 감정관리 및 명상 추천")

    lines.append("\n💊 [5] 추천 영양소 및 이유")
    oheng_data = load_oheng_data()
    element_data = oheng_data.get(oheng, {}).get("부족")
    if element_data:
        for nutrient in element_data["영양소"]:
            lines.append(f"- {nutrient}: 체질 보완 및 {oheng} 오행의 균형 회복을 돕습니다.")
    else:
        lines.append("- 분석된 영양소 정보가 없습니다.")

    return "\n".join(lines)

def send_email(recipient_email, subject, message):
    try:
        sender_email = "audiso.seo@gmail.com"
        sender_password = "tjdudwns00!!"
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

# Streamlit UI
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

if st.button("🔍 분석 및 추천하기"):
    oheng = analyze_oheng_by_year(birth_date.year)
    season = get_birth_season(birth_date)
    explanation = generate_interpretation(name, gender, oheng, survey, bmi, season)
    st.subheader("📘 사주 건강 분석 결과")
    st.text(explanation)

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
