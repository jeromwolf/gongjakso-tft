# 데이터공작소 TFT 풀스택 프로젝트

## 프로젝트 개요

**프로젝트명**: 데이터공작소 개발 TFT 홈페이지 (풀스택)
**배포 URL**:
- Frontend: https://gongjakso-tft-frontend.onrender.com
- Backend API: https://gongjakso-tft.onrender.com
- API Docs: https://gongjakso-tft.onrender.com/api/docs

**GitHub**: https://github.com/jeromwolf/gongjakso-tft
**배포 플랫폼**: Render.com
**개발 도구**: Claude Code

---

## 기술 스택

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 17 (Render)
- **ORM**: SQLAlchemy (Async)
- **Auth**: JWT
- **AI**: Anthropic Claude API, OpenAI API
- **Email**: Resend API
- **Migration**: Alembic

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: React Query (TanStack Query)
- **UI Components**: Radix UI, shadcn/ui

### DevOps
- **Deployment**: Render.com (Docker)
- **Database**: Render PostgreSQL
- **CI/CD**: GitHub → Render 자동 배포
- **Containerization**: Docker, Docker Compose

---

## 프로젝트 구조

```
gongjakso-tft/
├── backend/                   # FastAPI 백엔드
│   ├── api/                   # API 라우터
│   ├── core/                  # 설정, DB
│   ├── models/                # SQLAlchemy 모델
│   ├── schemas/               # Pydantic 스키마
│   ├── services/              # 비즈니스 로직
│   ├── utils/                 # 유틸리티
│   ├── scripts/               # 데이터 마이그레이션 스크립트
│   ├── alembic/               # DB 마이그레이션
│   ├── main.py                # FastAPI 앱
│   ├── Dockerfile             # Docker 이미지
│   └── requirements.txt       # Python 의존성
│
├── frontend/                  # Next.js 프론트엔드
│   ├── app/                   # App Router 페이지
│   ├── components/            # React 컴포넌트
│   ├── lib/                   # 유틸리티
│   ├── hooks/                 # Custom Hooks
│   ├── types/                 # TypeScript 타입
│   └── public/                # 정적 파일
│
└── docker-compose.yml         # 로컬 개발 환경
```

---

## 브랜치 관리 전략 ⚠️

### 현재 브랜치 구조

```
main                           # 메인 개발 브랜치 (프론트엔드 배포용)
└── deploy/backend-root        # Render 백엔드 배포 전용 ⚠️
```

### ⚠️ 중요: deploy/backend-root 브랜치

**왜 별도 브랜치를 사용하나요?**

Render 배포 시도:
- ❌ `main` + Root Directory: `backend` → **타임아웃 발생**
- ✅ `deploy/backend-root` + Root Directory: (없음) → **정상 작동**

**deploy/backend-root 브랜치 특징:**
- `backend/` 디렉토리 내용이 **루트에 평평하게** 배치
- Railway 배포용으로 원래 만들었지만 Render에서도 잘 작동
- Root Directory 설정 없이 바로 Docker 빌드

**브랜치 업데이트 방법:**

```bash
# 1. main에서 백엔드 작업 후 커밋
git checkout main
git add backend/
git commit -m "백엔드 기능 추가"

# 2. deploy/backend-root로 전환
git checkout deploy/backend-root

# 3. main 변경사항 머지
git merge main

# 4. 충돌 해결 (backend/ 디렉토리 관련)
# backend/* 파일들이 루트로 이동했는지 확인

# 5. 푸시 (자동 배포 트리거)
git push origin deploy/backend-root
```

---

## Render 배포 설정

### Backend 설정

**Settings → Build & Deploy:**

| 항목 | 값 |
|------|-----|
| Branch | `deploy/backend-root` ⚠️ |
| Root Directory | **(비어있음)** |
| Dockerfile Path | `Dockerfile` |
| Docker Build Context | `.` |
| Docker Command | **(비어있음)** |

**Environment Variables:**

```bash
# 필수
DATABASE_URL=postgresql+asyncpg://...  # Render 자동 설정
SECRET_KEY=<강력한-랜덤-키>

# 선택 (AI 기능 사용 시)
ANTHROPIC_API_KEY=<키>
OPENAI_API_KEY=<키>

# 선택 (이메일 기능 사용 시)
RESEND_API_KEY=<키>
FROM_EMAIL=noreply@gongjakso-tft.onrender.com

# 앱 설정
DEBUG=false
NEWSLETTER_ENABLED=true
```

⚠️ **CORS_ORIGINS 환경변수는 설정하지 마세요!**
- 코드의 기본값이 이미 프론트엔드 URL 포함
- 환경변수 설정 시 Pydantic 파싱 에러 발생

### Frontend 설정

**Settings → Build & Deploy:**

| 항목 | 값 |
|------|-----|
| Branch | `main` |
| Root Directory | `frontend` |
| Build Command | `npm install && npm run build` |
| Start Command | `npm start` |

**Environment Variables:**

```bash
NEXT_PUBLIC_API_URL=https://gongjakso-tft.onrender.com
NODE_ENV=production
```

---

## 로컬 개발 환경

### 1. Docker Compose로 전체 스택 실행

```bash
# 전체 서비스 시작 (PostgreSQL + Backend + Frontend)
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

**접속:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### 2. 개별 실행 (권장)

**Backend:**
```bash
cd backend

# PostgreSQL만 실행
docker-compose up -d postgres

# Python 가상환경
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

---

## 데이터베이스 관리

### Admin 계정 생성 및 데이터 업로드

```bash
cd backend

# 프로덕션 데이터 업로드 스크립트 실행
python3 scripts/upload_to_production.py
```

**스크립트 동작:**
1. Admin 계정 생성 (`admin@example.com` / `admin123`)
2. 로그인 및 토큰 획득
3. 기존 블로그/프로젝트 삭제
4. 새로운 블로그 6개 업로드
5. 새로운 프로젝트 12개 업로드

### Admin 권한 부여

**Render PostgreSQL Shell에서:**

```sql
-- Admin 역할 부여
UPDATE users SET role = 'ADMIN' WHERE email = 'admin@example.com';

-- 확인
SELECT email, role FROM users WHERE email = 'admin@example.com';
```

---

## 주요 기능

### 1. 블로그 시스템
- Markdown 콘텐츠 작성/수정
- 태그 기반 분류
- 조회수 추적
- AI 자동 콘텐츠 생성 (Claude API)

### 2. 프로젝트 전시
- 12개 프로젝트 소개
- GitHub 링크, 데모 URL
- 기술 스택 표시
- 난이도 및 카테고리 분류

### 3. 뉴스레터
- 구독자 관리
- 뉴스레터 발송 (Resend API)
- 스케줄링 (Celery)

### 4. 인증/권한
- JWT 기반 인증
- Admin/User 역할 구분
- 비밀번호 해싱 (bcrypt)

---

## 트러블슈팅

### 1. CORS 에러

**증상:**
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**해결:**

1. `backend/core/config.py` 확인:
   ```python
   CORS_ORIGINS: list[str] = [
       "http://localhost:3000",
       "https://gongjakso-tft-frontend.onrender.com"  # 필수!
   ]
   ```

2. `deploy/backend-root` 브랜치에 머지:
   ```bash
   git checkout deploy/backend-root
   git merge main
   git push origin deploy/backend-root
   ```

### 2. 환경변수 파싱 에러

**증상:**
```
pydantic_settings.sources.SettingsError: error parsing value for field "CORS_ORIGINS"
```

**원인:** CORS_ORIGINS 환경변수를 JSON 배열로 설정

**해결:** Render에서 CORS_ORIGINS 환경변수 **삭제**

### 3. 배포 타임아웃

**증상:** Build exceeded maximum time limit

**원인:** `main` 브랜치 + `backend` Root Directory 조합

**해결:** `deploy/backend-root` 브랜치 사용

### 4. Database Connection 에러

**증상:** `asyncpg` 드라이버 에러

**원인:** DATABASE_URL 형식 오류

**해결:**
```bash
# 올바른 형식
postgresql+asyncpg://user:pass@host:5432/dbname

# 잘못된 형식
postgresql://user:pass@host:5432/dbname  # asyncpg 누락
```

---

## 배포 체크리스트

### 배포 전

- [ ] `deploy/backend-root`가 최신 코드 포함
- [ ] CORS_ORIGINS에 프론트엔드 URL 포함
- [ ] 환경변수 설정 완료 (DATABASE_URL, SECRET_KEY)
- [ ] Dockerfile 빌드 테스트

### 배포 후

- [ ] Backend Health Check: https://gongjakso-tft.onrender.com/api/health
- [ ] Frontend 정상 로딩
- [ ] API Docs 접근: https://gongjakso-tft.onrender.com/api/docs
- [ ] 블로그 목록 표시 확인
- [ ] 프로젝트 목록 표시 확인
- [ ] CORS 에러 없음

---

## Git 워크플로우

### 일반 개발

```bash
# 1. main 브랜치에서 작업
git checkout main
git pull origin main

# 2. 기능 개발
git add .
git commit -m "기능 추가"

# 3. 푸시
git push origin main
```

**자동 배포:**
- Frontend: main 푸시 → Render 자동 배포
- Backend: deploy/backend-root 푸시 → Render 자동 배포

### 백엔드 배포

```bash
# main 작업 후
git checkout deploy/backend-root
git merge main
git push origin deploy/backend-root
```

---

## 참고 링크

- **Frontend**: https://gongjakso-tft-frontend.onrender.com
- **Backend API**: https://gongjakso-tft.onrender.com
- **API Docs**: https://gongjakso-tft.onrender.com/api/docs
- **Render Dashboard**: https://dashboard.render.com
- **GitHub**: https://github.com/jeromwolf/gongjakso-tft

---

## 개발 히스토리

### Phase 1: 정적 사이트 (완료)
- HTML/CSS/JS 기반 랜딩 페이지
- Railway 배포

### Phase 2: 풀스택 전환 (완료)
- FastAPI 백엔드 구축
- Next.js 프론트엔드 구축
- PostgreSQL 데이터베이스
- Render 배포 전환

### Phase 3: 데이터 마이그레이션 (완료)
- 블로그 6개, 프로젝트 12개 업로드
- Admin 계정 설정
- CORS 설정 완료

---

**마지막 업데이트**: 2025-10-04
**작성자**: Claude Code AI Assistant
