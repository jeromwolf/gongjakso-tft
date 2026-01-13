# AI ON 플랫폼

AI 기술 스터디와 바이브코딩 프로젝트를 공유하는 플랫폼입니다.

**배포 URL**:
- Frontend: https://gongjakso-tft-frontend.onrender.com
- Backend API: https://gongjakso-tft.onrender.com
- API Docs: https://gongjakso-tft.onrender.com/api/docs

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
│   ├── scripts/         # 데이터 마이그레이션 스크립트
│   └── main.py          # 엔트리포인트
│
├── frontend/            # Next.js 프론트엔드
│   ├── app/            # App Router 페이지
│   ├── components/     # React 컴포넌트
│   ├── lib/            # 유틸리티, API 클라이언트
│   ├── hooks/          # Custom Hooks
│   ├── types/          # TypeScript 타입
│   └── public/         # 정적 파일
│
├── docs/                # 문서
│   └── IMPLEMENTATION_PLAN.md  # Phase 1-8 구현 계획
│
├── archive/             # 아카이브
│   └── v1-static-site/ # 기존 정적 사이트
│
├── claude.md           # 프로젝트 개발 기록 및 배포 가이드
├── TEST_REPORT.md      # 테스트 결과
└── docker-compose.yml  # 로컬 개발 환경
```

---

## 🚀 기능

### 현재 구현 완료 ✅
- **회원 인증**: 회원가입, 로그인 (JWT)
- **블로그**: 기술 블로그 게시판 (6개 게시물)
- **프로젝트**: 프로젝트 쇼케이스 (12개 프로젝트)
  - GitHub URL #2 지원 (메인/서브 리포지토리)
  - Markdown 상세 콘텐츠
  - ✨ **AI 자동 정보 생성** - GitHub URL만 입력하면 자동 작성
- **Newsletter**: 이메일 구독 관리
- **AI 컨텐츠**: OpenAI GPT-4 기반 컨텐츠 생성
- **자동화**: Slug 자동 생성, 중복 처리

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
- **Database**: PostgreSQL 17 (Neon Serverless) + SQLAlchemy (async)
- **Auth**: JWT (python-jose)
- **AI**: OpenAI API (GPT-4)
- **Email**: Resend API

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: React Query (TanStack Query)
- **UI Components**: Radix UI, shadcn/ui

### Infrastructure
- **Hosting**: Render.com (Docker)
- **Database**: Neon PostgreSQL 17 (Serverless)
- **CI/CD**: GitHub → Render 자동 배포

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

## 🌐 Render 배포

자세한 배포 가이드는 [claude.md](./claude.md)를 참고하세요.

### 🚨 중요: 브랜치 전략

- **Frontend**: `main` 브랜치 사용
- **Backend**: `deploy/backend-root` 브랜치 사용 (필수!)
  - Root Directory 설정 없이 사용
  - `main` + Root Directory 조합은 타임아웃 발생

### Backend 배포 설정

**Render Settings:**
- Branch: `deploy/backend-root` 🚨
- Root Directory: (비워두기) 🚨
- Dockerfile Path: `Dockerfile`
- Docker Build Context: `.`

**Environment Variables:**
```bash
DATABASE_URL=postgresql+asyncpg://...@neon.tech/neondb?ssl=require  # Neon DB
SECRET_KEY=<강력한-랜덤-키>
OPENAI_API_KEY=<키>
RESEND_API_KEY=<키>
FROM_EMAIL=noreply@gongjakso-tft.onrender.com
DEBUG=false
```

⚠️ **CORS_ORIGINS 환경변수는 설정하지 마세요** (코드 기본값 사용)

### Frontend 배포 설정

**Render Settings:**
- Branch: `main`
- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Start Command: `npm start`

**Environment Variables:**
```bash
NEXT_PUBLIC_API_URL=https://gongjakso-tft.onrender.com
NODE_ENV=production
```

### 배포 후 체크리스트

- [ ] Backend Health: https://gongjakso-tft.onrender.com/api/health
- [ ] API Docs: https://gongjakso-tft.onrender.com/api/docs
- [ ] Frontend: https://gongjakso-tft-frontend.onrender.com
- [ ] 블로그 목록 표시 확인 (6개)
- [ ] 프로젝트 목록 표시 확인 (12개)
- [ ] CORS 에러 없음

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
ANTHROPIC_API_KEY=<your-anthropic-api-key>
OPENAI_API_KEY=<your-openai-api-key>
RESEND_API_KEY=<your-resend-api-key>
FROM_EMAIL=<your-email>@resend.dev
DEBUG=true
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📚 문서

- [개발 기록 & 배포 가이드](./claude.md) - 프로젝트 전체 문서 (Render 배포 포함)
- [구현 계획](./docs/IMPLEMENTATION_PLAN.md) - Phase 1-8 상세 계획 (20개월)
- [테스트 리포트](./TEST_REPORT.md) - 배포 전 테스트 결과
- [운영 정책](./docs/공작소%20TFT%20사이트%20운영%20정책(가상).pdf) - 회원 등급, 행동 규칙
- [SWOT 분석](./docs/공작소%20TFT%20SWOT%20분석.pdf) - 전략적 방향성

---

## 🔄 최근 변경사항

### 2025-01-13
- ✅ **Neon DB 마이그레이션 완료** (Azure → Neon 전환)
  - 비용 절감을 위한 Serverless PostgreSQL 전환
  - 데이터 완전 이전 (Users 4, Blogs 7, Projects 12)

### 2025-10-04
- ✅ **Render.com 배포 완료** (Railway → Render 전환)
- ✅ 프로덕션 데이터 업로드 (블로그 6개, 프로젝트 12개)
- ✅ 브랜치 전략 최적화 (`deploy/backend-root` 브랜치 생성)
- ✅ CORS 설정 완료
- ✅ 로그인/회원가입 에러 메시지 UX 개선
- ✅ 전체 시스템 테스트 완료 (Docker)
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

**AI ON**

- GitHub: https://github.com/jeromwolf/gongjakso-tft
- Website: https://gongjakso-tft-frontend.onrender.com
- YouTube: https://www.youtube.com/channel/UCzwPW_BSlr4Art7ckUYK5kw

---

**Built with ❤️ by AI ON**
