
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
    lines.append(f"🔮 {name}({gender})님의 사주는 '{oheng}'의 기운을 중심으로 하며, 출생 계절은 '{season}'입니다.\n")

    # 1. 성격과 성향
    lines.append("🧠 [1] 타고난 성격과 성향")
    if oheng == "목":
        lines.append("- 🌳 목(木): 창조적이고 진취적인 성향을 지닌 분입니다. 독립심이 강하며 새로운 시도를 두려워하지 않습니다.")
    elif oheng == "화":
        lines.append("- 🔥 화(火): 활발하고 열정적인 성격으로 주변을 이끄는 리더 기질이 있으며 감정 표현이 풍부합니다.")
    elif oheng == "토":
        lines.append("- 🪵 토(土): 차분하고 신중하며 책임감이 강한 성격으로, 안정과 조화를 추구하는 유형입니다.")
    elif oheng == "금":
        lines.append("- ⚔️ 금(金): 냉철하고 분석적인 성향으로, 체계적이며 논리적인 사고를 지향합니다.")
    else:
        lines.append("- 💧 수(水): 감성적이고 직관적인 성향으로, 예술적 감각과 사람에 대한 통찰력이 뛰어납니다.")

    # 2. 운세 흐름
    lines.append("\n🔮 [2] 운세 흐름과 인생 경향")
    lines.append("- 연도별 오행의 흐름에 따라 건강과 운의 강약이 달라질 수 있습니다.")
    if season == "봄":
        lines.append("- 봄에 태어난 분은 성장과 변화에 유리하며, 청년기 기회가 많습니다.")
    elif season == "여름":
        lines.append("- 여름 출생자는 에너지 넘치며 성공욕이 강하나 소모가 심할 수 있습니다.")
    elif season == "가을":
        lines.append("- 가을 출생자는 실속 있고 인내심이 강하여 중년 이후에 더욱 빛납니다.")
    else:
        lines.append("- 겨울 출생자는 내면이 깊고 준비성이 뛰어나며, 늦게 개화하는 스타일입니다.")

    # 3. 직업 성향
    lines.append("\n💼 [3] 적합한 직업과 생활 방식")
    if oheng == "목":
        lines.append("- 기획, 연구, 창작, 교육, 자연과학 등 자유롭고 성장성 높은 분야가 어울립니다.")
    elif oheng == "화":
        lines.append("- 마케팅, 스포츠, 정치, 방송, 리더십이 요구되는 분야에서 강점을 가집니다.")
    elif oheng == "토":
        lines.append("- 금융, 행정, 상담, 식품 등 실무 중심의 안정적인 직업군이 적합합니다.")
    elif oheng == "금":
        lines.append("- 법률, 기술, 데이터 분석, 컨설팅 등 논리력과 전략이 필요한 직종에 유리합니다.")
    else:
        lines.append("- 예술, 상담, 교육, 치료 분야처럼 감성을 기반으로 한 직업에 적합합니다.")

    # 4. 애정운
    lines.append("\n💞 [4] 애정운과 인간관계")
    if oheng == "목":
        lines.append("- 자상하고 배려심 깊지만, 고집이 있어 갈등이 생길 수 있습니다.")
    elif oheng == "화":
        lines.append("- 열정적인 연애를 즐기며 빠르게 친해지지만, 감정기복으로 오해 소지가 있습니다.")
    elif oheng == "토":
        lines.append("- 안정감 있는 관계를 선호하며 헌신적이지만 표현에는 다소 서툴 수 있습니다.")
    elif oheng == "금":
        lines.append("- 신중하고 절제된 사랑을 추구하며, 친밀해지기까지 시간이 필요합니다.")
    else:
        lines.append("- 감성적이며 의존적인 성향으로, 깊은 애정과 교감에 민감합니다.")

    # 5. 건강 분석
    lines.append("\n🩺 [5] 사주 기반 건강 경향")
    if oheng == "목":
        lines.append("- 간과 근육, 인대 계통이 약할 수 있으며 스트레스성 피로에 민감합니다.")
    elif oheng == "화":
        lines.append("- 심장, 혈압, 순환계 문제가 발생할 가능성이 있으며, 열이 많은 체질일 수 있습니다.")
    elif oheng == "토":
        lines.append("- 소화기 계통에 약점을 가질 수 있으며, 복부 트러블에 주의해야 합니다.")
    elif oheng == "금":
        lines.append("- 폐와 피부, 면역 계통이 민감하여 호흡기 질환이나 알레르기에 유의해야 합니다.")
    else:
        lines.append("- 신장, 방광, 뇌 건강과 연관이 크며, 체내 수분 부족이나 정신적 피로가 동반될 수 있습니다.")

    # 6. 건강 결론
    lines.append("\n📊 [6] 설문 및 BMI 기반 종합 건강 판단")
    lines.append(f"- 현재 BMI: {bmi:.1f}")
    if bmi < 18.5:
        lines.append("  → 저체중: 체력 저하와 영양 불균형 가능성이 있습니다.")
    elif bmi >= 25:
        lines.append("  → 과체중: 고혈압, 당뇨 등 대사질환 발생 가능성이 높습니다.")
    else:
        lines.append("  → 정상체중: 균형 잡힌 체형입니다. 유지가 중요합니다.")

    active_flags = [k for k, v in survey.items() if v]
    if active_flags:
        lines.append(f"- 설문을 통해 나타난 건강 이슈: {', '.join(active_flags)}")
    else:
        lines.append("- 건강 설문상 큰 특이사항은 확인되지 않았습니다.")

    # 7. 예방을 위한 건강 가이드
    lines.append("\n🛡️ [7] 생활 습관 및 건강관리 팁")
    if oheng == "목":
        lines.append("- 스트레스 해소, 주기적인 간 해독, 규칙적인 걷기 운동이 좋습니다.")
    elif oheng == "화":
        lines.append("- 유산소 운동, 혈액순환 촉진 식단, 심장에 무리 주지 않는 생활을 권장합니다.")
    elif oheng == "토":
        lines.append("- 식습관 개선, 가벼운 복부 마사지, 장 건강 프로바이오틱스 섭취가 도움됩니다.")
    elif oheng == "금":
        lines.append("- 미세먼지 피하기, 수분 섭취 늘리기, 유산소 운동 중심의 생활 습관을 추천드립니다.")
    else:
        lines.append("- 따뜻한 물 자주 마시기, 정신안정 요법(명상 등), 수면의 질 개선에 집중하세요.")

    # 8. 추천 영양소 및 기능
    lines.append("\n💊 [8] 체질 보완을 위한 추천 영양소")
    oheng_data = load_oheng_data()
    nutrients = oheng_data.get(oheng, {}).get("부족", {}).get("영양소", [])
    for n in nutrients:
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
        desc = explanation.get(n, "신체 균형을 위한 필수 영양소")
        lines.append(f"- {n}: {desc}")

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

