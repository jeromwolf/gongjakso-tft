# 🤖 AI ON 일일 자동화 가이드

## 📋 개요

AI ON의 블로그와 뉴스레터를 매일 자동으로 생성하고 발송하는 완전 자동화 시스템입니다.

### 작동 방식

```
📅 매일 자동 실행
    ↓
📝 오전 9시: AI 블로그 생성
    ├─ GPT-4로 기술 블로그 작성
    ├─ Markdown 형식
    └─ DRAFT 또는 자동 발행
    ↓
📧 오후 6시: 뉴스레터 생성 & 발송
    ├─ 지난 24시간 콘텐츠 수집
    ├─ GPT-4로 뉴스레터 작성
    └─ DRAFT 또는 자동 발송
```

---

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# .env 파일에 추가
OPENAI_API_KEY=sk-...         # OpenAI API 키 (GPT-4)
DATABASE_URL=postgresql+asyncpg://...  # 데이터베이스 URL
```

### 2. 의존성 설치

```bash
cd backend
pip install -r requirements.txt
```

설치되는 주요 패키지:
- `openai==1.54.0` - OpenAI API (GPT-4)
- `apscheduler==3.10.4` - 스케줄러
- `resend==0.6.0` - 이메일 발송

### 3. 즉시 실행 (테스트)

```bash
# 블로그 + 뉴스레터 즉시 생성 (DRAFT 모드)
python scripts/run_daily_automation.py --now

# 자동 발행/발송 모드
python scripts/run_daily_automation.py --now --auto-publish-blog --auto-send-newsletter
```

### 4. 자동 스케줄러 실행

```bash
# 매일 자동 실행 (DRAFT 모드)
python scripts/run_daily_automation.py

# 완전 자동 모드 (발행 + 발송)
python scripts/run_daily_automation.py --auto-publish-blog --auto-send-newsletter

# 커스텀 스케줄 (블로그 오전 10시, 뉴스레터 오후 8시)
python scripts/run_daily_automation.py --blog-hour 10 --newsletter-hour 20
```

---

## 📖 사용법 상세

### 옵션 1: DRAFT 모드 (권장)

AI가 콘텐츠를 생성하고 데이터베이스에 DRAFT 상태로 저장합니다.
Admin이 검토 후 수동으로 발행/발송합니다.

```bash
python scripts/run_daily_automation.py
```

**장점:**
- ✅ AI 생성 내용 검토 가능
- ✅ 수정 가능
- ✅ 발행 전 최종 확인

**프로세스:**
1. 스크립트 실행 → DRAFT 생성
2. Admin 대시보드에서 확인
   - 블로그: https://your-domain.com/admin/blog
   - 뉴스레터: https://your-domain.com/admin/newsletter
3. 필요 시 수정
4. "발행" 또는 "발송" 버튼 클릭

### 옵션 2: 완전 자동 모드

AI가 콘텐츠를 생성하고 즉시 발행/발송합니다.

```bash
python scripts/run_daily_automation.py --auto-publish-blog --auto-send-newsletter
```

**장점:**
- ✅ 완전 자동화
- ✅ 사람 개입 불필요

**주의:**
- ⚠️ 검토 없이 바로 발행/발송
- ⚠️ AI 생성 내용 그대로 게시

---

## 📝 개별 실행

### 블로그만 생성

```bash
# DRAFT 모드
python scripts/run_blog_scheduler.py --now

# 자동 발행
python scripts/run_blog_scheduler.py --now --auto-publish

# 특정 주제로 생성
python scripts/run_blog_scheduler.py --now --topic "FastAPI 성능 최적화"
```

### 뉴스레터만 생성

```bash
# DRAFT 모드
python scripts/run_newsletter_scheduler.py --now

# 자동 발송
python scripts/run_newsletter_scheduler.py --now --auto-send
```

---

## 🕐 스케줄 설정

### macOS/Linux (cron)

```bash
# cron 편집
crontab -e

# 매일 오전 9시: 블로그 생성 (DRAFT)
0 9 * * * cd /path/to/backend && source venv/bin/activate && python3 scripts/run_blog_scheduler.py --now

# 매일 오후 6시: 뉴스레터 생성 (DRAFT)
0 18 * * * cd /path/to/backend && source venv/bin/activate && python3 scripts/run_newsletter_scheduler.py --now

# 또는 통합 스크립트 사용
0 0 * * * cd /path/to/backend && source venv/bin/activate && python3 scripts/run_daily_automation.py --now
```

### Windows (Task Scheduler)

1. "작업 스케줄러" 열기
2. "기본 작업 만들기" 클릭

**블로그 작업:**
- **트리거**: 매일 오전 9시
- **동작**: 프로그램 시작
  - 프로그램: `python`
  - 인수: `scripts/run_blog_scheduler.py --now`
  - 시작 위치: `C:\path\to\backend`

**뉴스레터 작업:**
- **트리거**: 매일 오후 6시
- **동작**: 프로그램 시작
  - 프로그램: `python`
  - 인수: `scripts/run_newsletter_scheduler.py --now`
  - 시작 위치: `C:\path\to\backend`

---

## 📊 생성 예시

### 블로그 생성

**입력:** AI가 자동으로 트렌딩 주제 선택

**출력:**
```
제목: FastAPI와 PostgreSQL 비동기 처리로 API 성능 10배 향상시키기
Slug: fastapi-postgresql-async-performance
태그: FastAPI, PostgreSQL, Python, Backend, Performance
길이: 1,800자

내용:
## FastAPI 비동기 처리의 중요성

최근 API 개발에서 성능은 필수적인 요소가 되었습니다...

## SQLAlchemy 2.0 비동기 ORM 활용

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()
```

...
```

### 뉴스레터 생성

**입력:** 최근 24시간 블로그 + 프로젝트

**출력:**
```
제목: 🚀 오늘의 AI ON: FastAPI 성능 최적화 & 새로운 프로젝트 소개
요약: 오늘은 FastAPI 성능 향상과 신규 AI 프로젝트를 소개합니다

본문:
안녕하세요, AI ON 구독자 여러분!

오늘은 FastAPI 비동기 처리를 통한 성능 최적화와
새롭게 추가된 AI 프로젝트를 소개합니다.

## 📝 오늘의 블로그
- FastAPI 비동기 처리로 API 성능 10배 향상
...
```

---

## 🔧 커스터마이징

### AI 프롬프트 수정

블로그 프롬프트: `backend/services/blog_generator.py`
```python
prompt = f"""
당신은 'AI ON'의 기술 블로그 작가입니다.

# 작성 가이드라인
1. **톤**: 전문적이지만 친근함
2. **길이**: 1500-2000자
...
"""
```

뉴스레터 프롬프트: `backend/services/newsletter_generator.py`

### 스케줄 변경

```bash
# 블로그: 매일 오전 10시, 뉴스레터: 매일 오후 8시
python scripts/run_daily_automation.py --blog-hour 10 --newsletter-hour 20
```

### Author ID 변경

```bash
# 블로그 작성자 ID 지정
python scripts/run_blog_scheduler.py --author-id 2
```

---

## 🐛 트러블슈팅

### 1. OPENAI_API_KEY 오류

```
ValueError: OPENAI_API_KEY is not configured
```

**해결:**
```bash
# .env 파일에 추가
OPENAI_API_KEY=sk-your-api-key-here
```

### 2. 데이터베이스 연결 오류

```
asyncpg.exceptions.InvalidPasswordError
```

**해결:**
- `.env` 파일의 `DATABASE_URL` 확인
- 비밀번호에 특수문자가 있으면 URL 인코딩 필요:
  - `!` → `%21`
  - `@` → `%40`

### 3. 블로그 slug 중복 오류

자동으로 타임스탬프를 추가하여 해결됩니다.

### 4. 뉴스레터 발송 실패

```bash
# .env 파일에 추가
RESEND_API_KEY=re_your_api_key_here
FROM_EMAIL=noreply@your-domain.com
```

---

## 📈 다음 단계

### 현재 상태 (로컬)
- ✅ 로컬 컴퓨터에서 실행
- ✅ Azure PostgreSQL 연결
- ✅ AI 콘텐츠 생성
- ✅ Admin 대시보드에서 확인

### 향후 계획 (클라우드)

검증 완료 후 다음 중 하나로 이전:

#### 옵션 A: GitHub Actions (무료, 추천)
```yaml
# .github/workflows/daily-automation.yml
on:
  schedule:
    - cron: '0 0 * * *'  # 매일 오전 9시 (UTC 0시 = KST 9시)
    - cron: '0 9 * * *'  # 매일 오후 6시 (UTC 9시 = KST 18시)
```

#### 옵션 B: Render Cron Jobs (유료)
- $7/month
- 완전 관리형

---

## 💰 비용

- **OpenAI GPT-4 API**:
  - 블로그: ~$0.03/개
  - 뉴스레터: ~$0.02/개
  - 하루 2회: ~$0.05/일
  - **월 비용**: ~$1.50/월

- **Resend API**:
  - 무료 티어: 월 3,000통
  - 구독자 100명: 월 3,000통 사용
  - **무료**

**총 비용**: ~$1.50/월

---

## 📊 Admin 대시보드

### 블로그 관리
- URL: `/admin/blog`
- 기능:
  - 생성된 블로그 목록 확인
  - DRAFT 블로그 수정
  - 발행/미발행 상태 관리

### 뉴스레터 관리
- URL: `/admin/newsletter`
- 기능:
  - 생성된 뉴스레터 목록 확인
  - DRAFT 뉴스레터 미리보기
  - 발송 버튼으로 수동 발송
  - 구독자 목록 확인

---

## 📞 문의

문제가 발생하면:
1. 로그 확인: `backend/logs/`
2. 이슈 등록: GitHub Issues
3. 이메일: kelly@aion.io.kr

---

**마지막 업데이트**: 2025-11-17
