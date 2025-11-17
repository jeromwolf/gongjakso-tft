# 🤖 AI 뉴스레터 자동 생성 가이드

## 📋 개요

AI ON의 주간 콘텐츠를 자동으로 수집하고 Claude AI로 뉴스레터를 생성한 후, 구독자들에게 자동 발송하는 시스템입니다.

### 작동 방식

```
📅 매주 월요일 오전 9시 (스케줄러)
    ↓
🔍 지난 주 콘텐츠 수집
    ├─ 블로그 포스트 (AI ON DB)
    ├─ 프로젝트 업데이트
    └─ IT 뉴스
    ↓
🤖 Claude AI로 뉴스레터 작성
    ├─ 제목 생성
    ├─ 요약 생성
    └─ HTML 콘텐츠 생성
    ↓
💾 데이터베이스 저장 (DRAFT 또는 SENT)
    ↓
📧 구독자에게 이메일 발송 (optional)
```

---

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# .env 파일에 추가
ANTHROPIC_API_KEY=sk-ant-...  # Claude API 키
RESEND_API_KEY=re_...         # Resend API 키 (이메일 발송용)
```

### 2. 의존성 설치

```bash
cd backend
pip install -r requirements.txt
```

설치되는 주요 패키지:
- `anthropic==0.39.0` - Claude API
- `apscheduler==3.10.4` - 스케줄러
- `resend==0.6.0` - 이메일 발송

### 3. 즉시 실행 (테스트)

```bash
# DRAFT 모드 (발송 안 함, 검토용)
python scripts/run_newsletter_scheduler.py --now

# 자동 발송 모드 (바로 발송)
python scripts/run_newsletter_scheduler.py --now --auto-send
```

### 4. 자동 스케줄러 실행

```bash
# 매주 월요일 오전 9시에 실행 (DRAFT 모드)
python scripts/run_newsletter_scheduler.py

# 매주 월요일 오전 9시에 실행 (자동 발송)
python scripts/run_newsletter_scheduler.py --auto-send

# 커스텀 스케줄 (금요일 오후 2시)
python scripts/run_newsletter_scheduler.py --day fri --hour 14 --minute 0
```

---

## 📖 사용법 상세

### 옵션 1: DRAFT 모드 (권장)

AI가 뉴스레터를 생성하고 데이터베이스에 DRAFT 상태로 저장합니다.
Admin이 검토 후 수동으로 발송 버튼을 클릭합니다.

```bash
python scripts/run_newsletter_scheduler.py --now
```

**장점:**
- ✅ AI 생성 내용 검토 가능
- ✅ 수정 가능
- ✅ 발송 전 최종 확인

**프로세스:**
1. 스크립트 실행 → DRAFT 뉴스레터 생성
2. Admin 대시보드에서 확인
3. 필요 시 수정
4. "발송" 버튼 클릭

### 옵션 2: 자동 발송 모드

AI가 뉴스레터를 생성하고 즉시 전체 구독자에게 발송합니다.

```bash
python scripts/run_newsletter_scheduler.py --now --auto-send
```

**장점:**
- ✅ 완전 자동화
- ✅ 사람 개입 불필요

**주의:**
- ⚠️ 검토 없이 바로 발송
- ⚠️ AI 생성 내용 그대로 전송

---

## 🕐 스케줄 설정

### macOS/Linux (cron)

```bash
# cron 편집
crontab -e

# 매주 월요일 오전 9시 (DRAFT 모드)
0 9 * * 1 cd /path/to/backend && python3 scripts/run_newsletter_scheduler.py --now

# 매주 월요일 오전 9시 (자동 발송)
0 9 * * 1 cd /path/to/backend && python3 scripts/run_newsletter_scheduler.py --now --auto-send
```

### Windows (Task Scheduler)

1. "작업 스케줄러" 열기
2. "기본 작업 만들기" 클릭
3. **트리거**: 매주 월요일 오전 9시
4. **동작**: 프로그램 시작
   - 프로그램: `python`
   - 인수: `scripts/run_newsletter_scheduler.py --now`
   - 시작 위치: `C:\path\to\backend`

---

## 📊 생성 예시

### 입력 (지난 주 콘텐츠)

```
블로그:
- FastAPI 성능 최적화 10가지 팁
- Next.js 15의 새로운 기능 살펴보기
- PostgreSQL 인덱스 전략

프로젝트:
- CutStudio: AI 비디오 편집 도구
- StockAI: 주식 분석 챗봇
```

### 출력 (AI 생성 뉴스레터)

```
제목: 🚀 이번 주 AI ON: FastAPI 최적화 & Next.js 15 신기능

요약: FastAPI 성능 향상과 Next.js 최신 기능을 다룬 3개의 블로그 게시

본문:
안녕하세요, AI ON 구독자 여러분!

이번 주는 백엔드 성능 최적화부터 최신 프론트엔드 기술까지
다양한 주제를 다루었습니다.

## 📝 이번 주 블로그 포스트

### FastAPI 성능 최적화 10가지 팁
FastAPI 애플리케이션의 성능을 극대화하는 실전 팁을 소개합니다...
[자세히 보기](https://aion.io.kr/blogs/fastapi-optimization)

...
```

---

## 🔧 커스터마이징

### AI 프롬프트 수정

`backend/services/newsletter_generator.py` 파일의 `generate_newsletter()` 함수에서 프롬프트를 수정할 수 있습니다:

```python
prompt = f"""
당신은 'AI ON'의 주간 뉴스레터를 작성하는 전문 작가입니다.

# 작성 가이드라인
1. **톤**: 친근하지만 전문적
2. **길이**: 800-1200자
3. **구조**: 인사 → 하이라이트 → 블로그 → 프로젝트 → 마무리
...
"""
```

### 스케줄 변경

```bash
# 매주 금요일 오후 2시
python scripts/run_newsletter_scheduler.py --day fri --hour 14 --minute 0

# 매일 오전 10시 (일간 뉴스레터)
python scripts/run_newsletter_scheduler.py --day "*" --hour 10 --minute 0
```

---

## 🐛 트러블슈팅

### 1. ANTHROPIC_API_KEY 오류

```
ValueError: ANTHROPIC_API_KEY is not configured
```

**해결:**
```bash
# .env 파일에 추가
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

### 2. 데이터베이스 연결 오류

```
asyncpg.exceptions.InvalidPasswordError
```

**해결:**
- `.env` 파일의 `DATABASE_URL` 확인
- Azure PostgreSQL 방화벽 설정 확인

### 3. 이메일 발송 실패

```
Failed to send newsletter
```

**해결:**
```bash
# .env 파일에 추가
RESEND_API_KEY=re_your_api_key_here
FROM_EMAIL=noreply@aion.io.kr
```

### 4. 콘텐츠가 없음

```
이번 주 새로운 블로그 포스트가 없습니다.
```

**해결:**
- 지난 7일 동안 블로그 포스트가 있는지 확인
- 테스트용 블로그 포스트 생성
- 스크립트의 `days` 파라미터 조정 (예: `days=14`)

---

## 📈 다음 단계

### 현재 상태 (로컬)
- ✅ 로컬 컴퓨터에서 실행
- ✅ Azure PostgreSQL 연결
- ✅ AI 뉴스레터 생성
- ✅ 이메일 발송

### 향후 계획 (클라우드)

검증 완료 후 다음 중 하나로 이전:

#### 옵션 A: GitHub Actions (무료, 추천)
```yaml
# .github/workflows/newsletter.yml
on:
  schedule:
    - cron: '0 0 * * 1'  # 매주 월요일
```

#### 옵션 B: Render Cron Jobs (유료)
- $7/month
- 완전 관리형

---

## 💰 비용

- **Anthropic Claude API**:
  - Sonnet 4.5: ~$0.01/뉴스레터
  - 월 4회: ~$0.04/월

- **Resend API**:
  - 무료 티어: 월 3,000통
  - 구독자 100명: 월 400통 사용
  - **무료**

**총 비용**: ~$0.04/월 (거의 무료!)

---

## 📞 문의

문제가 발생하면:
1. 로그 확인: `backend/logs/`
2. 이슈 등록: GitHub Issues
3. 이메일: kelly@aion.io.kr

---

**마지막 업데이트**: 2025-11-17
