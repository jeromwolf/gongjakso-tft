"""
API를 통해 블로그 포스트 시드 데이터 생성
"""
import requests
import time

BASE_URL = "http://localhost:8000/api"

# 1. Login to get token
login_data = {
    "email": "admin@example.com",
    "password": "admin123"
}

print("🔐 로그인 중...")
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

if response.status_code != 200:
    print("❌ 로그인 실패. admin 계정을 먼저 생성하세요.")
    print(f"Error: {response.text}")
    exit(1)

token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("✅ 로그인 성공")

# 2. Delete existing blogs
print("\n🗑️  기존 블로그 삭제 중...")
response = requests.get(f"{BASE_URL}/blog", headers=headers)
if response.status_code == 200:
    blogs = response.json()["items"]
    for blog in blogs:
        requests.delete(f"{BASE_URL}/blog/{blog['id']}", headers=headers)
        print(f"  ✅ '{blog['title']}' 삭제")

# 3. Create new blogs
blogs_data = [
    {
        "title": "FastAPI + Next.js로 풀스택 AI 블로그 플랫폼 개발하기",
        "slug": "fastapi-nextjs-fullstack-blog-platform",
        "excerpt": "FastAPI 백엔드와 Next.js 15 프론트엔드를 사용하여 AI 콘텐츠 자동 생성 기능이 포함된 풀스택 블로그 플랫폼을 만든 과정을 공유합니다.",
        "content": """# Fast API + Next.js로 풀스택 AI 블로그 플랫폼 개발하기

## 프로젝트 개요

데이터공작소 TFT에서 FastAPI와 Next.js를 사용하여 AI 콘텐츠 자동 생성 기능이 포함된 풀스택 블로그 플랫폼을 개발했습니다.

## 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **SQLAlchemy**: ORM (비동기 지원)
- **PostgreSQL**: 메인 데이터베이스
- **Anthropic Claude API**: AI 콘텐츠 생성

### Frontend
- **Next.js 15**: React 기반 풀스택 프레임워크
- **TailwindCSS**: 유틸리티 우선 CSS
- **React Query**: 서버 상태 관리
- **TypeScript**: 타입 안정성

## 주요 기능

AI 콘텐츠 자동 생성, 비동기 데이터베이스 처리, 실시간 검색 & 필터링 등의 기능을 구현했습니다.

기술 블로그는 [GitHub](https://github.com/jeromwolf/gongjakso-tft)에서 확인하실 수 있습니다!
""",
        "status": "published",
        "tags": ["FastAPI", "Next.js", "AI", "풀스택"]
    },
    {
        "title": "Claude Code와 함께하는 AI 페어 프로그래밍",
        "slug": "ai-pair-programming-with-claude-code",
        "excerpt": "Claude Code를 활용한 AI 페어 프로그래밍 경험을 공유합니다. 개발 속도 향상과 코드 품질 개선 사례를 소개합니다.",
        "content": """# Claude Code와 함께하는 AI 페어 프로그래밍

## AI 개발 도구의 진화

Claude Code는 Anthropic의 Claude AI를 터미널에서 직접 사용할 수 있는 혁신적인 개발 도구입니다.

## 주요 활용 사례

### 1. 빠른 프로토타이핑
복잡한 기능도 자연어로 설명하면 바로 구현 가능합니다.

### 2. 코드 리뷰 자동화
작성한 코드에 대한 즉각적인 피드백을 받을 수 있습니다.

### 3. 버그 디버깅
에러 메시지를 보여주면 원인 분석과 해결책을 제시합니다.

## 실제 성과

- **코드 작성 시간**: 40% 단축
- **디버깅 시간**: 60% 단축
- **문서화 시간**: 70% 단축

AI와 함께 더 나은 코드를 작성하세요! 🚀
""",
        "status": "published",
        "tags": ["Claude", "AI", "개발도구", "생산성"]
    },
    {
        "title": "PostgreSQL 비동기 처리로 성능 10배 향상시키기",
        "slug": "postgresql-async-performance-optimization",
        "excerpt": "SQLAlchemy의 비동기 기능과 PostgreSQL을 활용하여 API 응답 속도를 10배 향상시킨 경험을 공유합니다.",
        "content": """# PostgreSQL 비동기 처리로 성능 10배 향상시키기

## 문제 상황

초기 블로그 플랫폼에서 동기 SQLAlchemy를 사용했을 때:
- **평균 응답 시간**: 500ms
- **동시 요청 처리**: 50 req/s
- **데이터베이스 연결**: 병목 현상 발생

## 해결 방법: 비동기 SQLAlchemy

비동기 엔진 설정, 비동기 세션 사용, 병렬 쿼리 실행 등을 통해 성능을 대폭 개선했습니다.

## 성능 개선 결과

### Before (동기)
- Requests per second: 50
- Average response time: 500ms

### After (비동기)
- Requests per second: 500 (10배 향상!)
- Average response time: 50ms (10배 개선!)

성능 최적화는 끝이 없습니다. 계속해서 개선해 나가세요! 🚀
""",
        "status": "published",
        "tags": ["PostgreSQL", "성능최적화", "비동기", "SQLAlchemy"]
    },
    {
        "title": "Alembic으로 데이터베이스 마이그레이션 안전하게 관리하기",
        "slug": "safe-database-migration-with-alembic",
        "excerpt": "Alembic을 사용하여 프로덕션 환경에서 안전하게 데이터베이스 스키마를 변경하는 방법과 베스트 프랙티스를 소개합니다.",
        "content": """# Alembic으로 데이터베이스 마이그레이션 안전하게 관리하기

## 왜 Alembic인가?

데이터베이스 스키마는 애플리케이션과 함께 진화합니다. Alembic은 SQLAlchemy와 완벽하게 통합되어 안전한 마이그레이션을 제공합니다.

## 안전한 마이그레이션 패턴

### 1. 컬럼 추가 (안전)
NULL 허용으로 컬럼 추가 → 기본값 설정 → NOT NULL 제약조건 추가

### 2. 컬럼 이름 변경 (무중단)
새 컬럼 추가 → 데이터 복사 → 애플리케이션 배포 → 이전 컬럼 삭제

### 3. 인덱스 추가 (CONCURRENTLY)
PostgreSQL CONCURRENTLY 옵션으로 락 없이 인덱스 생성

## 베스트 프랙티스

1. 작은 단위로 마이그레이션
2. 항상 downgrade 구현
3. 프로덕션 데이터로 테스트
4. 문서화
5. 백업

안전한 배포는 안전한 마이그레이션에서 시작됩니다! 🚀
""",
        "status": "published",
        "tags": ["Alembic", "데이터베이스", "마이그레이션", "DevOps"]
    },
    {
        "title": "TypeScript + React Query로 타입 안전한 프론트엔드 만들기",
        "slug": "type-safe-frontend-with-typescript-react-query",
        "excerpt": "TypeScript와 React Query를 활용하여 런타임 에러를 줄이고, 개발 경험을 향상시킨 방법을 공유합니다.",
        "content": """# TypeScript + React Query로 타입 안전한 프론트엔드 만들기

## 타입 안전성의 중요성

JavaScript의 동적 타이핑은 유연하지만, 런타임 에러의 주요 원인입니다. TypeScript와 React Query를 조합하면 이를 해결할 수 있습니다.

## 구현 방법

### 1. API 타입 정의

백엔드 응답을 정확히 반영한 TypeScript 인터페이스를 작성합니다.

### 2. React Query 통합

타입 안전한 API 호출과 자동 캐싱을 동시에 얻을 수 있습니다.

### 3. 에러 처리

TypeScript의 타입 가드를 활용한 안전한 에러 처리를 구현합니다.

## 개발 경험 향상

- **자동 완성**: IDE가 모든 속성을 인식
- **리팩토링**: 안전한 코드 변경
- **문서화**: 타입이 곧 문서

타입 안전성은 개발 속도와 품질을 동시에 향상시킵니다! 💎
""",
        "status": "published",
        "tags": ["TypeScript", "React", "ReactQuery", "타입안전성"]
    }
]

print("\n📝 새로운 블로그 포스트 생성 중...")
for blog_data in blogs_data:
    response = requests.post(f"{BASE_URL}/blog", json=blog_data, headers=headers)
    if response.status_code == 201:
        print(f"  ✅ '{blog_data['title']}' 생성")
    else:
        print(f"  ❌ '{blog_data['title']}' 생성 실패: {response.text}")
    time.sleep(0.5)  # Rate limiting

print(f"\n🎉 블로그 포스트 생성 완료!")
print(f"📊 http://localhost:3000/blog 에서 확인하세요!")
