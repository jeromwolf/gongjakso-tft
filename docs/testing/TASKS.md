# 🚀 Gongjakso TFT Backend Integration Tasks

**프로젝트**: 블로그 & 뉴스레터 풀스택 개발
**브랜치**: `feature/backend-integration`
**시작일**: 2025-10-03
**전체 진행률**: 49/57 (86.0%)

---

## ✅ Phase 1: 기본 구조 설정 (완료 ✨)

### 완료된 작업
- [x] **Phase 1-1**: Git 브랜치 생성
  - [x] `feature/backend-integration` 브랜치 생성
  - [x] 브랜치 전환 확인

- [x] **Phase 1-2**: 디렉토리 구조 생성
  - [x] `backend/api/` 생성
  - [x] `backend/models/` 생성
  - [x] `backend/services/` 생성
  - [x] `backend/core/` 생성
  - [x] `backend/schemas/` 생성
  - [x] `backend/utils/` 생성
  - [x] 모든 `__init__.py` 파일 생성

- [x] **Phase 1-3**: `backend/requirements.txt` 작성
  - [x] FastAPI 의존성 추가
  - [x] PostgreSQL (asyncpg, SQLAlchemy) 추가
  - [x] AI 서비스 (anthropic, openai) 추가
  - [x] Email (resend) 추가
  - [x] 유틸리티 (loguru, pydantic) 추가

- [x] **Phase 1-4**: `backend/core/config.py` 작성
  - [x] Settings 클래스 정의
  - [x] Database URL 설정
  - [x] CORS 설정
  - [x] AI API 키 설정
  - [x] Email 설정
  - [x] Newsletter 스케줄 설정

- [x] **Phase 1-5**: `backend/core/database.py` 작성
  - [x] AsyncEngine 설정
  - [x] AsyncSession 설정
  - [x] Base 모델 정의
  - [x] get_db() 의존성 함수
  - [x] create_all_tables() 함수
  - [x] drop_all_tables() 함수

- [x] **Phase 1-6**: `backend/main.py` 작성
  - [x] FastAPI 앱 초기화
  - [x] CORS 미들웨어 추가
  - [x] lifespan 이벤트 (startup/shutdown)
  - [x] Health check 엔드포인트 (/, /api/health)
  - [x] API 라우터 등록 준비

- [x] **Phase 1-7**: Docker 환경 설정 (추가)
  - [x] `docker-compose.yml` 작성 (PostgreSQL + Backend + Frontend)
  - [x] `backend/Dockerfile` 작성
  - [x] `backend/.dockerignore` 작성
  - [x] `.env.example` 작성

---

## ✅ Phase 2: User & Auth (회원 관리) (완료 ✨)

- [x] **Phase 2-1**: `backend/models/user.py` 작성
  - [x] User 테이블 정의
  - [x] 컬럼: id, email, password_hash, name, role
  - [x] 타임스탬프: created_at, last_login
  - [x] 인덱스 및 제약조건
  - [x] Blog relationship 추가

- [x] **Phase 2-2**: `backend/schemas/user.py` 작성
  - [x] UserCreate 스키마
  - [x] UserLogin 스키마
  - [x] UserResponse 스키마
  - [x] Token 스키마
  - [x] PasswordChange 스키마

- [x] **Phase 2-3**: `backend/utils/auth.py` 작성
  - [x] 비밀번호 해싱 (bcrypt)
  - [x] JWT 토큰 생성/검증
  - [x] decode_access_token() 함수

- [x] **Phase 2-4**: `backend/utils/dependencies.py` 작성
  - [x] get_current_user() 의존성
  - [x] get_current_active_user() 의존성
  - [x] get_current_admin_user() 의존성
  - [x] get_optional_user() 의존성

- [x] **Phase 2-5**: `backend/api/auth.py` 작성
  - [x] POST /api/auth/signup - 회원가입
  - [x] POST /api/auth/login - 로그인
  - [x] GET /api/auth/me - 현재 사용자 정보
  - [x] PUT /api/auth/me - 프로필 수정
  - [x] POST /api/auth/change-password - 비밀번호 변경

---

## ✅ Phase 3: Blog 기능 (완료 ✨)

- [x] **Phase 3-1**: `backend/models/blog.py` 작성
  - [x] Blog 테이블 정의
  - [x] 컬럼: id, title, slug, content, excerpt, status, tags
  - [x] 타임스탬프 및 인덱스
  - [x] view_count 필드

- [x] **Phase 3-2**: `backend/schemas/blog.py` 작성
  - [x] BlogCreate 스키마
  - [x] BlogUpdate 스키마
  - [x] BlogResponse 스키마
  - [x] BlogListResponse 스키마
  - [x] BlogPublishRequest 스키마

- [x] **Phase 3-3**: Blog 모델에 User 관계 추가
  - [x] author_id 외래키 추가
  - [x] User relationship 설정
  - [x] to_dict() 메서드에 author 정보 포함

- [x] **Phase 3-4**: `backend/utils/slug.py` 작성
  - [x] slugify() 함수
  - [x] generate_unique_slug() 함수

- [x] **Phase 3-5**: `backend/services/blog_service.py` 작성
  - [x] create_blog() 함수
  - [x] get_blog_by_id() 함수
  - [x] get_blog_by_slug() 함수
  - [x] update_blog() 함수
  - [x] delete_blog() 함수
  - [x] list_blogs() 함수 (페이지네이션, 필터링)
  - [x] publish_blog() / unpublish_blog() 함수
  - [x] increment_view_count() 함수

- [x] **Phase 3-6**: `backend/api/blog.py` 작성
  - [x] GET /api/blog - 블로그 목록 조회 (페이지네이션)
  - [x] GET /api/blog/{id} - 블로그 상세 조회
  - [x] GET /api/blog/slug/{slug} - Slug로 조회
  - [x] POST /api/blog - 블로그 생성 (인증 필요)
  - [x] PUT /api/blog/{id} - 블로그 수정 (인증 필요)
  - [x] DELETE /api/blog/{id} - 블로그 삭제 (인증 필요)
  - [x] POST /api/blog/{id}/publish - 발행/취소 (인증 필요)

---

## ✅ Phase 4: Frontend 기본 설정 (완료 ✨)

- [x] **Phase 4-1**: Next.js 프로젝트 초기화
  - [x] `npx create-next-app` 실행
  - [x] TypeScript, TailwindCSS, ESLint 설정
  - [x] App Router 사용
  - [x] 의존성 설치 (axios, react-query, date-fns, react-markdown)

- [x] **Phase 4-2**: API 클라이언트 설정
  - [x] `frontend/src/lib/types.ts` - TypeScript 타입 정의
  - [x] `frontend/src/lib/api.ts` - Axios 클라이언트 + API 함수
  - [x] `frontend/.env.local` - 환경 변수 설정
  - [x] React Query Provider 설정

- [x] **Phase 4-3**: 홈페이지 & 블로그 목록
  - [x] `frontend/src/app/page.tsx` - 홈페이지
  - [x] `frontend/src/app/blog/page.tsx` - 블로그 목록
  - [x] 반응형 디자인 적용
  - [x] 백엔드 API 연동 테스트

---

## ✅ Phase 5: Project 시스템 (MVP) (완료 ✨)

- [x] **Phase 5-1**: `backend/models/project.py` 작성
  - [x] Project 테이블 정의
  - [x] 컬럼: name, slug, description, content
  - [x] github_url, demo_url, thumbnail_url
  - [x] tech_stack (JSON), status, category
  - [x] view_count, star_count
  - [x] 인덱스 및 제약조건

- [x] **Phase 5-2**: `backend/schemas/project.py` 작성
  - [x] ProjectCreate 스키마
  - [x] ProjectUpdate 스키마
  - [x] ProjectResponse 스키마
  - [x] ProjectListResponse 스키마

- [x] **Phase 5-3**: `backend/services/project_service.py` 작성
  - [x] create_project() 함수
  - [x] get_project_by_id() 함수
  - [x] get_project_by_slug() 함수
  - [x] list_projects() 함수 (페이지네이션, 필터링)
  - [x] update_project() 함수
  - [x] increment_view_count() 함수

- [x] **Phase 5-4**: `backend/api/project.py` 작성
  - [x] GET /api/projects - 프로젝트 목록 조회
  - [x] GET /api/projects/{id} - 프로젝트 상세 조회
  - [x] GET /api/projects/slug/{slug} - Slug로 조회
  - [x] POST /api/projects - 프로젝트 생성 (Admin)
  - [x] PUT /api/projects/{id} - 프로젝트 수정 (Admin)
  - [x] DELETE /api/projects/{id} - 프로젝트 삭제 (Admin)
  - [x] main.py에 router 등록

- [x] **Phase 5-5**: 12개 프로젝트 DB 마이그레이션
  - [x] 기존 프로젝트 데이터 준비 (홈페이지에서 추출)
  - [x] 마이그레이션 스크립트 작성 (backend/scripts/migrate_projects.py)
  - [x] DB에 INSERT 실행 (12개 프로젝트 성공)

- [x] **Phase 5-6**: Frontend 프로젝트 상세 페이지
  - [x] `frontend/src/lib/types.ts`에 Project 타입 추가
  - [x] `frontend/src/lib/api.ts`에 projectAPI 추가
  - [x] `frontend/src/app/project/[slug]/page.tsx` 작성
  - [x] 마크다운 렌더링 (react-markdown)
  - [x] GitHub, Demo 링크
  - [x] 기술 스택 표시

---

## ✅ Phase 6: Frontend 인증 (완료 ✨)

- [x] **Phase 6-1**: 인증 상태 관리
  - [x] `frontend/src/contexts/auth-context.tsx` 작성
  - [x] useAuth 훅 생성
  - [x] localStorage 토큰 관리
  - [x] 로그인 상태 전역 관리

- [x] **Phase 6-2**: 로그인 페이지
  - [x] `frontend/src/app/login/page.tsx` 작성
  - [x] 로그인 폼 (이메일, 비밀번호)
  - [x] API 연동 (authAPI.login)
  - [x] 에러 핸들링
  - [x] 로그인 성공 시 리다이렉트

- [x] **Phase 6-3**: 회원가입 페이지
  - [x] `frontend/src/app/signup/page.tsx` 작성
  - [x] 회원가입 폼 (이메일, 이름, 비밀번호)
  - [x] API 연동 (authAPI.signup)
  - [x] 유효성 검사
  - [x] 회원가입 성공 시 자동 로그인

- [x] **Phase 6-4**: 네비게이션 바
  - [x] `frontend/src/components/navbar.tsx` 작성
  - [x] 로그인/로그아웃 버튼
  - [x] 사용자 프로필 표시
  - [x] 모든 페이지에 적용 (layout.tsx)

---

## ✅ Phase 7: Frontend 블로그 기능 (완료 ✨)

- [x] **Phase 7-1**: 블로그 상세 페이지
  - [x] `frontend/src/app/blog/[slug]/page.tsx` 작성
  - [x] Markdown 렌더링 (react-markdown)
  - [x] 메타 태그 (SEO)
  - [x] 조회수 표시
  - [x] 태그, 작성일, 작성자 표시

- [x] **Phase 7-2**: 블로그 작성 페이지 (Admin)
  - [x] `frontend/src/app/admin/blog/new/page.tsx` 작성
  - [x] Markdown 에디터
  - [x] 제목, 내용, 태그 입력
  - [x] 초안/발행 선택
  - [x] 미리보기 기능

- [x] **Phase 7-3**: 블로그 수정 페이지 (Admin)
  - [x] `frontend/src/app/admin/blog/[id]/edit/page.tsx` 작성
  - [x] 기존 데이터 불러오기
  - [x] 수정 폼
  - [x] 삭제 기능
  - [x] 발행/비발행 토글

---

## ✅ Phase 8: Frontend 뉴스레터 (완료 ✨)

- [x] **Phase 8-1**: 뉴스레터 구독 기능
  - [x] 홈페이지 구독 폼 동작 구현
  - [x] API 연동 (newsletterAPI.subscribe)
  - [x] 성공/실패 메시지 표시
  - [x] 구독 완료 후 안내

- [x] **Phase 8-2**: 뉴스레터 관리 페이지 (Admin)
  - [x] `frontend/src/app/admin/newsletter/page.tsx` 작성
  - [x] 구독자 목록
  - [x] 뉴스레터 발송 내역
  - [x] 뉴스레터 생성/발송 버튼

---

## ✅ Phase 9: Backend Newsletter 기능 (완료 ✨)

- [x] **Phase 9-1**: `backend/models/newsletter.py` 작성
  - [x] Subscriber 테이블 (이메일, 구독 상태, 구독일)
  - [x] Newsletter 테이블 (제목, 내용, 발송일, 상태)
  - [x] NewsletterRequest 테이블 (요청 주제, 우선순위)
  - [x] 관계 설정

- [x] **Phase 9-2**: `backend/schemas/newsletter.py` 작성
  - [x] SubscriberCreate 스키마
  - [x] NewsletterCreate 스키마
  - [x] NewsletterRequestCreate 스키마
  - [x] NewsletterResponse 스키마
  - [x] UnsubscribeRequest 스키마

- [x] **Phase 9-3**: `backend/services/email_service.py` 작성
  - [x] Resend API 연동
  - [x] send_email() 함수
  - [x] send_newsletter() 함수
  - [x] HTML 템플릿 렌더링

- [x] **Phase 9-4**: `backend/services/newsletter_service.py` 작성
  - [x] subscribe() 함수
  - [x] unsubscribe() 함수
  - [x] create_newsletter() 함수
  - [x] send_newsletter_to_all() 함수
  - [x] create_newsletter_request() 함수

- [x] **Phase 9-5**: `backend/api/newsletter.py` 작성
  - [x] POST /api/newsletter/subscribe - 구독 신청
  - [x] POST /api/newsletter/unsubscribe - 구독 취소
  - [x] POST /api/newsletter/request - 뉴스레터 주제 요청
  - [x] POST /api/newsletter/send - 뉴스레터 발송 (Admin)
  - [x] GET /api/newsletter - 뉴스레터 목록
  - [x] main.py에 router 등록

---

## ✅ Phase 10: AI 콘텐츠 생성 (완료 ✨)

- [x] **Phase 10-1**: `backend/services/ai_service.py` 작성
  - [x] Claude API 클라이언트 초기화
  - [x] generate_blog_content() 함수
  - [x] generate_newsletter_content() 함수
  - [x] 프롬프트 템플릿 작성

- [x] **Phase 10-2**: `backend/utils/content_generator.py` 작성
  - [x] 프로젝트 정보 수집 (GitHub API)
  - [x] 콘텐츠 생성 워크플로우
  - [x] 마크다운 포맷팅

- [x] **Phase 10-3**: `backend/api/ai_content.py` 작성
  - [x] POST /api/ai/generate-blog - 블로그 자동 생성
  - [x] POST /api/ai/generate-newsletter - 뉴스레터 자동 생성
  - [x] POST /api/ai/preview - 콘텐츠 미리보기
  - [x] main.py에 router 등록

---

## ✅ Phase 11: 배포 설정 (완료 ✨)

- [x] **Phase 11-1**: `.env.example` 작성
  - [x] DATABASE_URL 템플릿
  - [x] ANTHROPIC_API_KEY 템플릿
  - [x] RESEND_API_KEY 템플릿
  - [x] SECRET_KEY 템플릿
  - [x] Newsletter 설정

- [x] **Phase 11-2**: `railway.json` 업데이트
  - [x] Frontend 서비스 설정 (frontend/railway.json)
  - [x] Backend 서비스 설정 (backend/railway.json)
  - [x] PostgreSQL 서비스 연결 가이드
  - [x] 환경 변수 매핑 문서화 (RAILWAY_DEPLOYMENT.md)

- [x] **Phase 11-3**: `backend/alembic.ini` 작성
  - [x] Alembic 초기화 (alembic.ini, env.py, script.py.mako)
  - [x] 마이그레이션 설정
  - [x] 마이그레이션 사용 가이드 (alembic/README.md)

---

## ✅ Phase 12: 테스트 & 통합 (완료 ✨)

- [x] **Phase 12-1**: 로컬 Docker 테스트
  - [x] Docker Compose 업데이트 (환경 변수, Frontend Dockerfile)
  - [x] `docker-compose up --build` 실행
  - [x] PostgreSQL 연결 확인 (healthy)
  - [x] Database 테이블 생성 확인 (6개 테이블)
  - [x] Backend API 엔드포인트 테스트
    - [x] GET / - Service info
    - [x] GET /api/health - Database 연결
    - [x] GET /api/blog - 블로그 목록
    - [x] GET /api/projects - 프로젝트 목록
  - [x] Frontend 시작 확인 (Next.js 15.5.4)
  - [x] 브라우저 테스트 (localhost:3000, localhost:8000/api/docs)

- [ ] **Phase 12-2**: Railway 배포 테스트 (선택 사항)
  - [ ] Railway PostgreSQL 생성
  - [ ] Backend 서비스 배포
  - [ ] 환경 변수 설정
  - [ ] 프로덕션 API 테스트
  - [ ] Frontend-Backend 통합 확인

---

## 🔄 Phase 13: 브랜치 병합 & 배포 (0/3)

- [ ] **Phase 13-1**: 최종 코드 리뷰
  - [ ] 모든 파일 검토
  - [ ] 불필요한 코드 제거
  - [ ] 주석 및 문서 정리

- [ ] **Phase 13-2**: Git 커밋 & 푸시
  - [ ] `git add .`
  - [ ] 상세한 커밋 메시지 작성
  - [ ] `git push origin feature/backend-integration`

- [ ] **Phase 13-3**: 메인 브랜치 병합
  - [ ] `git checkout main`
  - [ ] `git merge feature/backend-integration`
  - [ ] `git push origin main`
  - [ ] Railway 자동 배포 확인

---

## 📊 진행 상황 요약

| Phase | 작업 | 완료 | 진행률 |
|-------|------|------|--------|
| Phase 1 | 백엔드 기본 구조 + Docker | 7/7 | ✅ 100% |
| Phase 2 | 백엔드 User & Auth | 5/5 | ✅ 100% |
| Phase 3 | 백엔드 Blog 기능 | 6/6 | ✅ 100% |
| Phase 4 | 프론트엔드 기본 설정 | 3/3 | ✅ 100% |
| Phase 5 | 프로젝트 시스템 MVP | 6/6 | ✅ 100% |
| Phase 6 | 프론트엔드 인증 | 4/4 | ✅ 100% |
| Phase 7 | 프론트엔드 블로그 | 3/3 | ✅ 100% |
| Phase 8 | 프론트엔드 뉴스레터 | 2/2 | ✅ 100% |
| Phase 9 | 백엔드 Newsletter | 5/5 | ✅ 100% |
| Phase 10 | AI 콘텐츠 생성 | 3/3 | ✅ 100% |
| Phase 11 | 배포 설정 | 3/3 | ✅ 100% |
| Phase 12 | 테스트 & 통합 | 1/2 | ✅ 50% |
| Phase 13 | 브랜치 병합 | 0/3 | 0% |
| **전체** | **Total** | **49/57** | **86.0%** |

---

## 📝 작업 규칙

1. ✅ **각 Phase 완료 시 컨펌 요청**
2. 📋 **상세 태스크 완료 시마다 체크박스 업데이트**
3. 🔍 **코드 작성 후 반드시 검증**
4. 💬 **막히는 부분은 즉시 논의**

---

**마지막 업데이트**: 2025-10-03
**현재 작업**: ✅ Phase 1-12 완료! 다음: Phase 13 (브랜치 병합 & 배포)

---

## 📌 주요 변경 사항

### 구조 재설계 이유
- **회원 관리** 필요: 블로그 작성자 인증
- **뉴스레터 요청** 추가: 사용자가 원하는 주제 요청 기능

### 새로운 Phase 순서
1. **Phase 2: User & Auth** ← 가장 기본이 되는 회원 관리
2. **Phase 3: Blog** ← User와 연동
3. **Phase 4: Newsletter** ← Subscriber + Newsletter + NewsletterRequest
4. **Phase 5: AI 콘텐츠** ← 모든 데이터 활용
5. **Phase 6-8**: 배포, 테스트, 병합
