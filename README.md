# 데이터공작소 TFT 홈페이지

켈리 데이터공작소 TFT의 공식 홈페이지입니다. 다양한 프로젝트와 솔루션을 소개합니다.

## 🚀 기능

- 📱 **반응형 디자인**: 모든 디바이스에서 최적화된 경험
- ✨ **인터랙티브 애니메이션**: 스크롤 애니메이션, 호버 효과, 3D 카드 효과
- 🎨 **모던한 UI**: 그래디언트 애니메이션, 펄스 효과
- 🔗 **프로젝트 쇼케이스**: TFT의 다양한 프로젝트 소개

## 📦 로컬에서 실행하기

### 1. 의존성 설치

```bash
npm install
```

### 2. 개발 서버 실행

```bash
npm start
```

브라우저에서 `http://localhost:3000` 로 접속하세요.

## 🚂 Railway로 배포하기

### 방법 1: Railway CLI 사용

1. **Railway CLI 설치**
```bash
npm install -g @railway/cli
```

2. **Railway 로그인**
```bash
railway login
```

3. **프로젝트 초기화**
```bash
railway init
```

4. **배포**
```bash
railway up
```

5. **도메인 확인**
```bash
railway domain
```

### 방법 2: GitHub 연동 (추천)

1. **GitHub에 코드 푸시**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Railway 웹사이트에서 배포**
   - [Railway.app](https://railway.app) 접속
   - "Start a New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 저장소 선택
   - 자동으로 빌드 및 배포 시작

3. **환경 설정 확인**
   - Railway는 자동으로 `package.json`의 `start` 스크립트 실행
   - PORT 환경변수 자동 설정

4. **도메인 설정**
   - Settings > Networking에서 도메인 생성
   - 또는 커스텀 도메인 연결

## 📁 프로젝트 구조

```
gongjakso-tft/
├── data-workshop-site.html  # 메인 HTML 파일
├── server.js                 # Express 서버
├── package.json              # 프로젝트 설정
├── railway.json              # Railway 배포 설정
└── README.md                 # 문서
```

## 🛠️ 기술 스택

- **프론트엔드**: HTML5, CSS3, JavaScript (ES6+)
- **백엔드**: Node.js, Express
- **배포**: Railway
- **스타일링**: Custom CSS (Gradient Animations, Scroll Animations)

## 🎨 개선된 기능

- **그래디언트 배경 애니메이션**: Hero 섹션의 생동감 있는 배경
- **스크롤 애니메이션**: 섹션별 페이드인 효과
- **3D 카드 효과**: 마우스 움직임에 따른 카드 회전
- **카드 반짝임 효과**: 호버 시 빛나는 효과
- **펄스 애니메이션**: CTA 버튼의 주목도 향상
- **네비게이션 스크롤 효과**: 스크롤 시 네비게이션 배경 변화

## 📝 라이센스

MIT License

## 👥 제작

데이터공작소 개발 TFT

---

**배포 완료 후 접속 가능!** 🎉
