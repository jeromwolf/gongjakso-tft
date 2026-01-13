# 🧪 AI ON 자동화 시스템 테스트 가이드

## 완성된 기능 목록

### ✅ 1. 블로그 자동 생성
- **파일**: `backend/services/blog_generator.py`, `backend/services/blog_scheduler.py`
- **스크립트**: `backend/scripts/run_blog_scheduler.py`
- **기능**: GPT-4로 매일 기술 블로그 자동 작성

### ✅ 2. 뉴스레터 자동 생성 및 발송
- **파일**: `backend/services/newsletter_generator.py`, `backend/services/newsletter_scheduler.py`
- **스크립트**: `backend/scripts/run_newsletter_scheduler.py`
- **기능**: 최근 콘텐츠 기반 뉴스레터 생성 및 발송

### ✅ 3. 통합 자동화 스케줄러
- **스크립트**: `backend/scripts/run_daily_automation.py`
- **기능**: 블로그 + 뉴스레터를 하나의 스크립트로 실행

### ✅ 4. 로그 분석 시스템
- **백엔드**: `backend/services/log_analyzer.py`, `backend/api/logs.py`
- **프론트엔드**: `frontend/src/app/admin/logs/page.tsx`
- **기능**: 에러 추적, 활동 분석, API 통계, 자동화 통계

---

## 📝 테스트 순서

### 1단계: 블로그 자동 생성 테스트

```bash
cd backend

# 즉시 실행 (DRAFT 모드)
python3 scripts/run_blog_scheduler.py --now

# 자동 발행 모드
python3 scripts/run_blog_scheduler.py --now --auto-publish

# 특정 주제로 생성
python3 scripts/run_blog_scheduler.py --now --topic "Next.js 15 새로운 기능"
```

**확인사항:**
- [ ] 터미널에 생성 진행 상황 표시
- [ ] GPT-4 API 호출 성공
- [ ] 데이터베이스에 블로그 저장
- [ ] Admin 페이지에서 블로그 확인 (https://your-domain.com/admin/blog)
- [ ] DRAFT 모드: status가 'draft'
- [ ] 자동 발행 모드: status가 'published'

### 2단계: 뉴스레터 생성 테스트

```bash
# 즉시 실행 (DRAFT 모드)
python3 scripts/run_newsletter_scheduler.py --now

# 자동 발송 모드
python3 scripts/run_newsletter_scheduler.py --now --auto-send
```

**확인사항:**
- [ ] 최근 블로그/프로젝트 수집
- [ ] GPT-4로 뉴스레터 작성
- [ ] 데이터베이스에 저장
- [ ] Admin 페이지에서 확인 (https://your-domain.com/admin/newsletter)
- [ ] DRAFT 모드: 저장만
- [ ] 자동 발송 모드: 구독자에게 이메일 발송

### 3단계: 통합 자동화 테스트

```bash
# 블로그 + 뉴스레터 둘 다 즉시 실행 (DRAFT)
python3 scripts/run_daily_automation.py --now

# 완전 자동 모드 (발행 + 발송)
python3 scripts/run_daily_automation.py --now --auto-publish-blog --auto-send-newsletter
```

**확인사항:**
- [ ] 블로그 생성 → 뉴스레터 생성 순서대로 실행
- [ ] 각 단계별 로그 출력
- [ ] 두 작업 모두 성공

### 4단계: 로그 분석 시스템 테스트

#### Backend API 테스트

```bash
# 서버 실행
cd backend
uvicorn main:app --reload --port 8000
```

브라우저에서 API Docs 접속: http://localhost:8000/api/docs

**테스트할 엔드포인트:**
1. `GET /api/logs/errors` - 에러 요약
2. `GET /api/logs/activity` - 활동 요약
3. `GET /api/logs/api-stats` - API 통계
4. `GET /api/logs/automation` - 자동화 통계
5. `GET /api/logs/recent` - 최근 로그
6. `GET /api/logs/dashboard` - 종합 대시보드

**확인사항:**
- [ ] 각 엔드포인트 응답 성공 (200 OK)
- [ ] JSON 데이터 형식 정확
- [ ] Admin 인증 필요 (토큰 없으면 401 에러)

#### Frontend 테스트

```bash
cd frontend
npm run dev
```

**접속:**
1. Admin 로그인: http://localhost:3000/login
2. 로그 분석 페이지: http://localhost:3000/admin/logs

**확인사항:**
- [ ] 에러 요약 카드 표시
- [ ] 활동 요약 (INFO, WARNING, ERROR, SUCCESS 카운트)
- [ ] API 통계 (요청 수, 에러 수)
- [ ] 자동화 통계 (블로그 생성/발행, 뉴스레터 생성/발송)
- [ ] 최근 로그 목록
- [ ] 시간 범위 필터 (1시간, 6시간, 24시간)
- [ ] 로그 레벨 필터 (ALL, INFO, WARNING, ERROR)
- [ ] 자동 새로고침 (30초~1분)

### 5단계: 스케줄러 테스트 (선택)

```bash
# 매일 오전 9시 블로그, 오후 6시 뉴스레터
python3 scripts/run_daily_automation.py

# 커스텀 시간 (블로그 10시, 뉴스레터 8시)
python3 scripts/run_daily_automation.py --blog-hour 10 --newsletter-hour 20
```

**확인사항:**
- [ ] 스케줄러 시작 메시지
- [ ] 설정된 시간에 자동 실행
- [ ] Ctrl+C로 정상 종료

---

## 🐛 예상 문제 및 해결

### 문제 1: OPENAI_API_KEY 오류

```
ValueError: OPENAI_API_KEY is not configured
```

**해결:**
```bash
# .env 파일에 추가
OPENAI_API_KEY=sk-your-api-key-here
```

### 문제 2: 데이터베이스 연결 오류

```
asyncpg.exceptions.InvalidPasswordError
```

**해결:**
- `.env` 파일의 `DATABASE_URL` 확인
- 비밀번호에 특수문자가 있으면 URL 인코딩

### 문제 3: 로그 파일 없음

```
WARNING: Failed to read log file...
```

**해결:**
```bash
# logs 디렉토리 생성
mkdir -p backend/logs

# 서버를 한 번 실행하면 자동으로 로그 파일 생성
uvicorn main:app --reload
```

### 문제 4: Admin 권한 없음 (401 Unauthorized)

**해결:**
```sql
-- PostgreSQL에서 Admin 권한 부여
UPDATE users SET role = 'ADMIN' WHERE email = 'your@email.com';
```

### 문제 5: Frontend에서 API 연결 안됨

**해결:**
```bash
# .env.local 파일 확인 (frontend/)
NEXT_PUBLIC_API_URL=http://localhost:8000

# CORS 설정 확인 (backend/core/config.py)
CORS_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend-domain.com"
]
```

---

## 📊 테스트 체크리스트

### Backend
- [ ] 블로그 생성 스크립트 실행 성공
- [ ] 뉴스레터 생성 스크립트 실행 성공
- [ ] 통합 자동화 스크립트 실행 성공
- [ ] 로그 API 엔드포인트 모두 작동
- [ ] Admin 인증 정상 작동
- [ ] 데이터베이스 저장 확인

### Frontend
- [ ] 로그 분석 페이지 로딩
- [ ] 에러 요약 표시
- [ ] 활동 요약 표시
- [ ] API 통계 표시
- [ ] 자동화 통계 표시
- [ ] 최근 로그 목록 표시
- [ ] 필터 기능 작동
- [ ] 자동 새로고침 작동

### Integration
- [ ] 블로그 생성 → Admin 페이지에 표시
- [ ] 뉴스레터 생성 → Admin 페이지에 표시
- [ ] 자동화 실행 → 로그 분석에 반영
- [ ] Frontend ↔ Backend 통신 정상

---

## 📈 다음 단계

### 로컬 테스트 완료 후

1. **프로덕션 배포**
   - Backend: Render.com 자동 배포 (main → deploy/backend-root 머지)
   - Frontend: Render.com 자동 배포 (main 푸시)

2. **환경변수 설정** (Render)
   ```bash
   OPENAI_API_KEY=sk-...
   DATABASE_URL=postgresql+asyncpg://...
   RESEND_API_KEY=re_...
   FROM_EMAIL=noreply@your-domain.com
   ```

3. **스케줄러 배포**
   - GitHub Actions로 cron job 설정
   - 또는 Render Cron Jobs 사용 ($7/month)

4. **모니터링 설정**
   - 로그 분석 페이지를 매일 확인
   - 에러 알림 설정 (선택)

---

## 💡 사용 팁

### DRAFT 모드 (권장)
- AI가 생성한 콘텐츠를 검토 후 발행
- 품질 관리 가능
- 수정 가능

### 완전 자동 모드
- 사람 개입 없이 자동 발행/발송
- 신뢰도가 높을 때 사용
- 로그 모니터링 필수

### 커스터마이징
- AI 프롬프트 수정: `blog_generator.py`, `newsletter_generator.py`
- 스케줄 시간 변경: `--blog-hour`, `--newsletter-hour`
- 로그 보존 기간 설정: `log_analyzer.py`

---

**마지막 업데이트**: 2025-11-17
**테스트 환경**: Python 3.11, Node.js 18+, PostgreSQL 17
