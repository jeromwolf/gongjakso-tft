# 데이터공작소 TFT 플랫폼

켈리 데이터공작소 TFT의 공식 커뮤니티 플랫폼입니다.

**배포 URL**: https://gongjakso-tft.up.railway.app

---

## 🏗️ 프로젝트 구조

```
gongjakso-tft/
├── backend/              # FastAPI 백엔드
│   ├── api/             # API 엔드포인트
│   ├── models/          # 데이터베이스 모델
│   ├── schemas/         # Pydantic 스키마
│   ├── core/            # 핵심 설정 (DB, 보안)
│   ├── services/        # 비즈니스 로직
│   └── main.py          # 엔트리포인트
│
├── frontend/            # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/        # App Router 페이지
│   │   ├── components/ # React 컴포넌트
│   │   ├── contexts/   # React Context (Auth 등)
│   │   └── lib/        # 유틸리티, API 클라이언트
│   └── public/         # 정적 파일
│
├── docs/                # 문서
│   └── IMPLEMENTATION_PLAN.md  # Phase 1-8 구현 계획
│
├── archive/             # 아카이브
│   └── v1-static-site/ # 기존 정적 사이트
│
├── DEPLOYMENT_CHECKLIST.md  # Railway 배포 가이드
├── TEST_REPORT.md           # 테스트 결과
└── docker-compose.yml       # 로컬 개발 환경
```

---

## 🚀 기능

### 현재 구현 완료 ✅
- **회원 인증**: 회원가입, 로그인 (JWT)
- **블로그**: 기술 블로그 게시판
- **프로젝트**: 프로젝트 쇼케이스
- **Newsletter**: 이메일 구독 관리
- **AI 컨텐츠**: OpenAI 기반 컨텐츠 생성

### 향후 구현 예정 📋
- **Phase 1-4** (9개월): 회원 프로필, Q&A, 배지 시스템
- **Phase 5** (2개월): 커뮤니티 게시판 (공지/자유/건의)
- **Phase 6** (3개월): 스터디 관리 시스템
- **Phase 7** (2개월): 프로젝트 협업 강화
- **Phase 8** (2개월): 행사/세미나 관리

자세한 내용은 [IMPLEMENTATION_PLAN.md](./docs/IMPLEMENTATION_PLAN.md)를 참고하세요.

---

## 🛠️ 기술 스택

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15 + SQLAlchemy (async)
- **Auth**: JWT (python-jose)
- **AI**: OpenAI GPT-4 API
- **Email**: Resend API

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: React Query (TanStack Query)
- **Forms**: React Hook Form

### Infrastructure
- **Hosting**: Railway
- **Database**: Railway PostgreSQL
- **CI/CD**: GitHub Actions (예정)

---

## 🏃 로컬 개발 환경 설정

### 1. Docker Compose 사용 (권장)

```bash
# 환경 변수 설정
cp .env.example .env
# .env 파일 편집 (DATABASE_URL, API 키 등)

# Docker Compose 실행
docker-compose up -d

# 서비스 확인
docker ps

# 접속
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/api/docs
```

### 2. 개별 실행

#### Backend

```bash
cd backend

# Python 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집

# 데이터베이스 마이그레이션
# (앱 시작 시 자동 실행됨)

# 서버 실행
uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 개발 서버 실행
npm run dev
```

---

## 🚂 Railway 배포

자세한 배포 가이드는 [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)를 참고하세요.

### 빠른 배포 요약

1. **GitHub 연동**
   - Railway 대시보드에서 GitHub 저장소 연결
   - Branch: `main` (또는 `feature/backend-integration`)

2. **Backend 서비스 생성**
   - Root Directory: `/backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - 환경 변수 설정 (DATABASE_URL, SECRET_KEY, API 키 등)

3. **Frontend 서비스 생성**
   - Root Directory: `/frontend`
   - Start Command: `npm start`
   - 환경 변수: `NEXT_PUBLIC_API_URL=<backend-url>`

4. **PostgreSQL 추가**
   - Railway 플러그인에서 PostgreSQL 추가
   - Backend 서비스에 연결

5. **도메인 설정**
   - Frontend: `gongjakso-tft.up.railway.app` (메인)
   - Backend: `gongjakso-tft-backend.up.railway.app`

---

## 📊 테스트

### 전체 테스트 리포트
[TEST_REPORT.md](./TEST_REPORT.md) 참고

### 로컬 테스트

```bash
# Backend API 테스트
curl http://localhost:8000/api/health

# 블로그 API 테스트
curl http://localhost:8000/api/blog

# Frontend 접속
open http://localhost:3000
```

---

## 📝 환경 변수

### Backend (.env)
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname
SECRET_KEY=<32자 이상의 강력한 랜덤 키>
OPENAI_API_KEY=<your-openai-api-key>
RESEND_API_KEY=<your-resend-api-key>
FROM_EMAIL=<your-email>@resend.dev
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📚 문서

- [구현 계획](./docs/IMPLEMENTATION_PLAN.md) - Phase 1-8 상세 계획 (20개월)
- [배포 체크리스트](./DEPLOYMENT_CHECKLIST.md) - Railway 배포 가이드
- [테스트 리포트](./TEST_REPORT.md) - 배포 전 테스트 결과
- [운영 정책](./docs/공작소%20TFT%20사이트%20운영%20정책(가상).pdf) - 회원 등급, 행동 규칙
- [SWOT 분석](./docs/공작소%20TFT%20SWOT%20분석.pdf) - 전략적 방향성

---

## 🔄 최근 변경사항

### 2025-10-04
- ✅ 로그인/회원가입 에러 메시지 UX 개선
- ✅ 전체 시스템 테스트 완료 (Docker)
- ✅ Railway 배포 가이드 작성
- ✅ Phase 5-8 구현 계획 추가 (게시판, 스터디, 협업, 행사)
- ✅ 기존 정적 사이트 아카이브 (`archive/v1-static-site`)

### 2025-10-02 ~ 2025-10-03
- ✅ Backend/Frontend 통합 완료
- ✅ Docker Compose 환경 구축
- ✅ Blog, Project, Newsletter API 구현
- ✅ 회원 인증 시스템 (JWT)

---

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 라이선스

MIT License

---

## 👥 팀

**데이터공작소 개발 TFT**

- GitHub: https://github.com/jeromwolf/gongjakso-tft
- Website: https://gongjakso-tft.up.railway.app

---

**Built with ❤️ by Data Workshop TFT**
