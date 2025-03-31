# 🧠 사주 기반 건강 분석 Streamlit 앱

이 앱은 사주(四柱)와 건강 설문 데이터를 기반으로 건강 상태를 분석하고, 개인 맞춤형 영양소를 추천하는 Streamlit 애플리케이션입니다.

---

## 🚀 주요 기능

- 사주 오행 기반 체질 분석
- 출생 계절(봄/여름/가을/겨울) 해석
- 건강 설문 20문항 분석
- BMI 기반 영양소 보완 제안
- 결과 PDF 다운로드 (한글 폰트 적용)
- 이메일 전송 기능 (SMTP 연동)
- 외부 광고 링크 배너
- 자주 묻는 질문(FAQ) 표시

---

## 📦 설치 방법

```bash
git clone https://github.com/your-username/saju-health-app.git
cd saju-health-app
pip install -r requirements.txt
```

> PDF 저장 시 한글 폰트 오류를 방지하려면 `NanumGothic.ttf` 파일을 같은 디렉토리에 위치시키세요.

---

## ▶️ 실행 방법

```bash
streamlit run app.py
```

---

## ✉️ 이메일 전송 기능

앱에서는 `audiso.seo@gmail.com` 계정을 기본 SMTP 전송으로 사용합니다.  
보안을 위해 배포 전에는 `.env` 설정 또는 환경변수로 이동하세요.

---

## 🧩 폴더 구성

```
app.py                  # Streamlit 애플리케이션 코드
requirements.txt       # 설치 패키지 목록
NanumGothic.ttf        # PDF 한글 폰트
README.md              # 이 문서
```
