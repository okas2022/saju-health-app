
# streamlit_saju_app_complete.py (통합 기능 최종 버전)
import streamlit as st
import json
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar
from fpdf import FPDF
import tempfile
import os
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

def generate_interpretation(name, gender, oheng, survey, bmi, season):
    intro = (
        f"사주(四柱)는 사람이 태어난 연도, 월, 일, 시간을 기준으로 하는 네 개의 기둥을 의미합니다.\n"
        "이 네 기둥은 각각 천간(天干)과 지지(地支)로 구성되어 있어, 총 8글자로 이루어진 팔자(八字)를 형성합니다.\n"
        "사주는 단순한 운세를 넘어서, 사람이 타고난 기질, 성격, 에너지 흐름과 건강 경향까지 포괄적으로 해석할 수 있는 전통적인 분석 도구입니다.\n"
        "오행(五行)은 목(木), 화(火), 토(土), 금(金), 수(水)로 나뉘며, 인간의 장기와 감정, 성향, 질병과도 밀접한 연관이 있습니다.\n"
        f"{name}({gender})님은 {season}에 태어나, '{oheng}'의 기운을 타고난 분입니다.\n"
    )
    if oheng == "목":
        oheng_desc = (
            "🌳 목(木)의 기운은 생명력과 성장의 상징입니다.\n"
            "간, 담과 관련이 깊고, 창의성과 자율성이 강하지만 스트레스에 취약할 수 있습니다.\n"
        )
    elif oheng == "화":
        oheng_desc = (
            "🔥 화(火)의 기운은 열정과 에너지를 상징합니다.\n"
            "심장, 소장과 관련이 깊고, 활발하고 사교적이지만 과로 시 혈압 문제에 주의가 필요합니다.\n"
        )
    elif oheng == "토":
        oheng_desc = (
            "⛰️ 토(土)의 기운은 안정감과 균형을 상징합니다.\n"
            "비장과 위장 기능이 중심이며, 내면이 깊고 현실적이지만 과식 또는 소화기 문제에 유의해야 합니다.\n"
        )
    elif oheng == "금":
        oheng_desc = (
            "⚔️ 금(金)의 기운은 결단력과 냉철함을 나타냅니다.\n"
            "폐, 대장과 관련이 있으며, 민감한 피부나 면역계 문제에 주의가 필요합니다.\n"
        )
    else:  # 수
        oheng_desc = (
            "💧 수(水)의 기운은 지혜와 깊이를 상징합니다.\n"
            "신장과 방광, 뇌와 관련이 있으며, 감정 기복이나 무기력감이 나타날 수 있습니다.\n"
        )

    body_info = f"💡 현재 BMI 지수는 {bmi:.1f}입니다. "
    if bmi < 18.5:
        body_info += "저체중 범위로, 체력과 면역 관리가 필요합니다.\n"
    elif bmi >= 25:
        body_info += "과체중 또는 비만으로 분류되며, 생활습관 개선이 권장됩니다.\n"
    else:
        body_info += "정상 체중으로 판단되며 건강 유지를 위한 관리가 중요합니다.\n"

    health_flags = [k for k, v in survey.items() if v]
    if health_flags:
        health_summary = "🩺 건강 설문 응답에 따르면 다음 항목에 체크하셨습니다: " + ", ".join(health_flags) + "\n"
    else:
        health_summary = "🩺 건강 설문에서는 특이사항이 발견되지 않았습니다.\n"

    forecast = (
        "🔮 2025년은 정신적 스트레스 관리가 가장 중요한 시기입니다.\n"
        "🔮 2026년은 소화기 및 면역력 강화에 집중하는 것이 좋습니다.\n"
    )

    return intro + oheng_desc + body_info + health_summary + forecast
    saju_intro = (
        f"{name}({gender})님의 사주는 '{oheng}' 오행이 주로 나타납니다.\n"
        f"출생 계절은 '{season}'입니다. 이는 체질이나 환경적 민감도에 영향을 줄 수 있습니다.\n"
    )
    result = saju_intro
    result += f"현재 BMI는 {bmi:.1f}로 "
    if bmi < 18.5:
        result += "저체중에 해당하며 영양소 흡수나 체력 유지에 주의가 필요합니다.\n"
    elif bmi >= 25:
        result += "과체중 또는 비만 범주에 속해 생활습관 개선이 요구됩니다.\n"
    else:
        result += "정상 범위로 보이며 건강 관리를 유지하는 것이 중요합니다.\n"
    health_flags = [k for k, v in survey.items() if v]
    if health_flags:
        result += "건강 설문에서 다음 항목에 체크하셨습니다: " + ", ".join(health_flags) + "\n"
    else:
        result += "건강 설문에서는 특별한 이상은 보고되지 않았습니다.\n"
    result += "2025년은 스트레스 관리, 2026년은 면역력과 소화기 건강에 주의가 필요합니다."
    return result


    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Nanum', '', 'NanumGothic.ttf', uni=True)
    pdf.set_font("Nanum", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    path = os.path.join(tempfile.gettempdir(), "report.pdf")
    pdf.output(path)
    return path

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
    nutrients = recommend_nutrients(oheng, "부족", bmi)

    st.subheader("📘 사주 건강 해석")
    st.text(explanation)
    st.subheader("💊 추천 영양소")
    for n in nutrients:
        st.markdown(f"- {n}")

        st.download_button("📄 분석 결과 PDF 다운로드", f, file_name="health_report.pdf")

    st.markdown("---")
    st.markdown("[🛍️ 건강 보청기 솔루션 제안 — xr.audiso.co.kr](https://xr.audiso.co.kr)")
    st.markdown("---")

    email_address = st.text_input("📧 결과를 이메일로 받아보시겠어요? 이메일 주소를 입력해주세요.")
    if st.button("📨 이메일 전송하기"):
        if email_address:
            if send_email(email_address, "사주 건강 분석 결과", explanation + "\n\n추천 영양소:\n" + "\n".join(nutrients)):
                st.success("✅ 이메일이 성공적으로 전송되었습니다!")
            else:
                st.error("❌ 이메일 전송에 실패했습니다. 설정을 확인해주세요.")
        else:
            st.warning("⚠️ 이메일 주소를 입력해주세요.")

with st.expander("❓ 자주 묻는 질문 (FAQ)"):
    st.markdown("""
**Q. 사주로 정말 건강 상태를 알 수 있나요?**  
A. 사주는 동양 철학의 체질 해석 기반이며, 이 앱은 전통 해석 + 건강 설문을 함께 고려합니다.

**Q. 오행은 어떻게 분석되나요?**  
A. 태어난 해의 천간을 기준으로 목·화·토·금·수 중 어떤 기운이 중심인지 분석합니다.

**Q. PDF 결과는 어디에 활용할 수 있나요?**  
A. 병원 건강 상담 시 참고하거나, 영양제 구매 시 본인의 특성에 맞는 제품 선택에 도움이 됩니다.
""")
