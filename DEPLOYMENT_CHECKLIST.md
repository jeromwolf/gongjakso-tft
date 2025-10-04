# 🚀 Railway 배포 체크리스트

**배포 대상**: https://gongjakso-tft.up.railway.app
**날짜**: 2025-10-04
**브랜치**: feature/backend-integration

---

## ✅ 배포 전 체크리스트

### 1. 코드 준비
- [x] 모든 변경사항 테스트 완료
- [x] 에러 메시지 UX 개선 완료
- [ ] Git commit 및 push
```bash
git add .
git commit -m "Fix: 로그인/회원가입 에러 메시지 UX 개선

- 로그인: email/password 입력 시 에러 메시지 초기화
- 회원가입: 모든 필드 입력 시 에러 메시지 초기화
- 사용자가 입력을 시작할 때까지 에러 메시지 유지

Ref: TEST_REPORT.md"
git push origin feature/backend-integration
```

### 2. 환경 변수 설정

#### Backend 환경 변수 (Railway)
```bash
# 데이터베이스
DATABASE_URL=postgresql+asyncpg://postgres:${PASSWORD}@${HOST}:5432/railway

# 보안
SECRET_KEY=<32자 이상의 강력한 랜덤 키>
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI 서비스
OPENAI_API_KEY=<your-openai-api-key>
ANTHROPIC_API_KEY=<optional>

# 이메일
RESEND_API_KEY=<your-resend-api-key>
FROM_EMAIL=<your-email>@resend.dev

# CORS
CORS_ORIGINS=["https://gongjakso-tft.up.railway.app","https://gongjakso-tft-frontend.up.railway.app"]

# 앱 정보
APP_NAME=Gongjakso TFT Backend
APP_VERSION=1.0.0
DEBUG=false

# Newsletter
NEWSLETTER_ENABLED=true
NEWSLETTER_SCHEDULE=0 9 * * *
```

#### Frontend 환경 변수 (Railway)
```bash
# API URL
NEXT_PUBLIC_API_URL=https://gongjakso-tft-backend.up.railway.app

# Node 환경
NODE_ENV=production
```

### 3. Railway 설정

#### Backend 서비스
- [ ] **서비스 이름**: gongjakso-tft-backend
- [ ] **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] **Working Directory**: `/backend`
- [ ] **환경 변수**: 위의 Backend 환경 변수 모두 등록
- [ ] **도메인**: gongjakso-tft-backend.up.railway.app (자동 할당)

#### Frontend 서비스
- [ ] **서비스 이름**: gongjakso-tft-frontend (또는 main)
- [ ] **Start Command**: `npm start` (또는 자동 감지)
- [ ] **Working Directory**: `/frontend`
- [ ] **환경 변수**: 위의 Frontend 환경 변수 모두 등록
- [ ] **도메인**: gongjakso-tft.up.railway.app

#### PostgreSQL Database
- [ ] Railway에서 PostgreSQL 플러그인 추가
- [ ] DATABASE_URL 자동 생성 확인
- [ ] Backend 서비스에 연결

### 4. 보안 체크

- [ ] **SECRET_KEY 생성**
```bash
# Python으로 강력한 키 생성
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

- [ ] **.env 파일 Git 제외** - .gitignore에 추가 확인
- [ ] **API 키 노출 여부** - 프론트엔드 코드에 하드코딩된 키 없는지 확인
- [ ] **CORS 설정** - 프로덕션 도메인만 허용

### 5. 데이터베이스 마이그레이션

Railway에서 Backend 서비스가 시작되면 자동으로 마이그레이션 실행:
```python
# backend/core/database.py의 create_all_tables() 함수가 자동 실행
await create_all_tables()
```

수동 마이그레이션 필요 시:
```bash
# Railway CLI 사용
railway run python -c "from core.database import create_all_tables; import asyncio; asyncio.run(create_all_tables())"
```

### 6. 배포 후 테스트

#### Backend 헬스 체크
```bash
curl https://gongjakso-tft-backend.up.railway.app/
# Expected: {"service":"Gongjakso TFT Backend","version":"1.0.0","status":"healthy"}

curl https://gongjakso-tft-backend.up.railway.app/api/health
# Expected: {"status":"healthy","message":"All systems operational","database":"connected"}
```

#### Frontend 페이지 확인
- [ ] https://gongjakso-tft.up.railway.app/ - 홈페이지
- [ ] https://gongjakso-tft.up.railway.app/blog - 블로그 페이지
- [ ] https://gongjakso-tft.up.railway.app/projects - 프로젝트 페이지
- [ ] https://gongjakso-tft.up.railway.app/login - 로그인 페이지
- [ ] https://gongjakso-tft.up.railway.app/signup - 회원가입 페이지

#### API 엔드포인트 테스트
```bash
# Blog API
curl https://gongjakso-tft-backend.up.railway.app/api/blog

# Projects API
curl https://gongjakso-tft-backend.up.railway.app/api/projects

# Newsletter API (인증 필요)
curl -H "Authorization: Bearer <token>" \
     https://gongjakso-tft-backend.up.railway.app/api/newsletter/subscribers
```

#### 회원가입 및 로그인 테스트
- [ ] 신규 사용자 회원가입
- [ ] 로그인 성공 확인
- [ ] JWT 토큰 발급 확인
- [ ] 보호된 페이지 접근 확인 (/admin/*)

#### Newsletter 기능 테스트
- [ ] 홈페이지에서 이메일 구독
- [ ] 관리자 페이지에서 구독자 확인 (/admin/newsletter/subscribers)
- [ ] 뉴스레터 작성 (/admin/newsletter/new)
- [ ] 뉴스레터 발송 테스트

### 7. 모니터링 설정

#### Railway 대시보드
- [ ] CPU/메모리 사용량 확인
- [ ] 로그 확인 (에러 없는지)
- [ ] 응답 시간 확인

#### Sentry 설정 (선택사항)
```bash
# Frontend
NEXT_PUBLIC_SENTRY_DSN=<your-sentry-dsn>

# Backend
SENTRY_DSN=<your-sentry-dsn>
```

---

## 🔄 배포 프로세스

### Option 1: Railway GitHub 연동 (권장)
1. Railway 대시보드에서 GitHub 저장소 연결
2. Branch 선택: `feature/backend-integration`
3. 환경 변수 설정
4. 자동 배포 확인

### Option 2: Railway CLI
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# Backend 배포
cd backend
railway up

# Frontend 배포
cd ../frontend
railway up
```

---

## 🐛 배포 시 예상 이슈 및 해결 방법

### Issue 1: Database 연결 실패
**증상**: `database connection failed`
**해결**:
- DATABASE_URL 환경 변수 확인
- `postgresql+asyncpg://` 프로토콜 사용 확인
- Railway PostgreSQL 플러그인 연결 확인

### Issue 2: CORS 에러
**증상**: Frontend에서 API 호출 시 CORS 에러
**해결**:
```python
# backend/main.py
CORS_ORIGINS = [
    "https://gongjakso-tft.up.railway.app",
    "https://gongjakso-tft-frontend.up.railway.app"
]
```

### Issue 3: Static 파일 404
**증상**: `/toss-qr.png` 등 이미지 파일 404
**해결**:
- Frontend의 `public/` 디렉토리에 파일 존재 확인
- Next.js 빌드 시 `public/` 디렉토리가 포함되는지 확인

### Issue 4: 환경 변수 미적용
**증상**: `NEXT_PUBLIC_API_URL` 등 환경 변수가 undefined
**해결**:
- `NEXT_PUBLIC_` 접두사 확인 (클라이언트 사이드 노출용)
- Railway에서 환경 변수 등록 후 재배포

---

## 📊 배포 후 성능 목표

### 응답 시간
- [ ] Backend API: 평균 < 200ms
- [ ] Frontend 페이지: 평균 < 1s (First Contentful Paint)
- [ ] Database 쿼리: 평균 < 100ms

### 가용성
- [ ] Uptime: > 99.9%
- [ ] 에러율: < 1%

---

## 📝 배포 후 작업

### 1. 초기 데이터 생성
- [ ] 관리자 계정 생성
- [ ] 샘플 블로그 포스트 확인
- [ ] 샘플 프로젝트 데이터 확인

### 2. SEO 최적화
- [ ] sitemap.xml 생성
- [ ] robots.txt 설정
- [ ] Open Graph 이미지 확인
- [ ] Google Search Console 등록

### 3. 분석 도구 설정
- [ ] Google Analytics 연동
- [ ] Hotjar / Mixpanel 연동 (선택)

### 4. 문서화
- [ ] API 문서 업데이트 (/api/docs)
- [ ] README.md 업데이트
- [ ] 운영 가이드 작성

---

## ✅ 최종 승인

배포 담당자: ________________
날짜: 2025-10-04
승인: [ ] 예 / [ ] 아니오

---

**참고 문서**:
- [TEST_REPORT.md](./TEST_REPORT.md) - 배포 전 테스트 결과
- [IMPLEMENTATION_PLAN.md](./docs/IMPLEMENTATION_PLAN.md) - 향후 기능 구현 계획
- [Railway 배포 가이드](https://docs.railway.app/)

**마지막 업데이트**: 2025-10-04 00:27 KST
