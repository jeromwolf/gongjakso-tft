"""
프로덕션 환경(Render)에 로컬 데이터 업로드
"""
import requests
import time
import json
import sys
from typing import List, Dict, Any

# Production API URL
BASE_URL = "https://gongjakso-tft.onrender.com/api"

# Admin credentials
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

def create_admin_user():
    """Create admin user if not exists"""
    print("👤 Admin 계정 생성 중...")

    signup_data = {
        "email": ADMIN_EMAIL,
        "name": "Admin User",
        "password": ADMIN_PASSWORD
    }

    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)

    if response.status_code == 201:
        print("✅ Admin 계정 생성 완료")
        return True
    elif response.status_code == 400 and "already registered" in response.text.lower():
        print("ℹ️  Admin 계정이 이미 존재합니다")
        return True
    else:
        print(f"❌ Admin 계정 생성 실패: {response.text}")
        return False


def login() -> str:
    """Login and get access token"""
    print("\n🔐 로그인 중...")

    login_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    if response.status_code != 200:
        print(f"❌ 로그인 실패: {response.text}")
        sys.exit(1)

    token = response.json()["access_token"]
    print("✅ 로그인 성공")
    return token


def delete_existing_blogs(headers: Dict[str, str]):
    """Delete all existing blogs"""
    print("\n🗑️  기존 블로그 삭제 중...")

    response = requests.get(f"{BASE_URL}/blog", headers=headers)

    if response.status_code == 200:
        blogs = response.json()["items"]
        if not blogs:
            print("  ℹ️  삭제할 블로그가 없습니다")
        else:
            for blog in blogs:
                requests.delete(f"{BASE_URL}/blog/{blog['id']}", headers=headers)
                print(f"  ✅ '{blog['title']}' 삭제")


def delete_existing_projects(headers: Dict[str, str]):
    """Delete all existing projects"""
    print("\n🗑️  기존 프로젝트 삭제 중...")

    response = requests.get(f"{BASE_URL}/projects", headers=headers)

    if response.status_code == 200:
        projects = response.json()["items"]
        if not projects:
            print("  ℹ️  삭제할 프로젝트가 없습니다")
        else:
            for project in projects:
                requests.delete(f"{BASE_URL}/projects/{project['id']}", headers=headers)
                print(f"  ✅ '{project['name']}' 삭제")


def upload_blogs(headers: Dict[str, str], blogs_data: List[Dict[str, Any]]):
    """Upload blog posts"""
    print(f"\n📝 {len(blogs_data)}개 블로그 포스트 업로드 중...")

    success_count = 0
    fail_count = 0

    for blog_data in blogs_data:
        response = requests.post(f"{BASE_URL}/blog", json=blog_data, headers=headers)

        if response.status_code == 201:
            print(f"  ✅ '{blog_data['title']}'")
            success_count += 1
        else:
            print(f"  ❌ '{blog_data['title']}' 실패: {response.text}")
            fail_count += 1

        time.sleep(0.3)  # Rate limiting

    print(f"\n📊 블로그 업로드 완료: {success_count}개 성공, {fail_count}개 실패")


def upload_projects(headers: Dict[str, str], projects_data: List[Dict[str, Any]]):
    """Upload projects"""
    print(f"\n🚀 {len(projects_data)}개 프로젝트 업로드 중...")

    success_count = 0
    fail_count = 0

    for project_data in projects_data:
        response = requests.post(f"{BASE_URL}/projects", json=project_data, headers=headers)

        if response.status_code == 201:
            print(f"  ✅ '{project_data['name']}'")
            success_count += 1
        else:
            print(f"  ❌ '{project_data['name']}' 실패: {response.text}")
            fail_count += 1

        time.sleep(0.3)  # Rate limiting

    print(f"\n📊 프로젝트 업로드 완료: {success_count}개 성공, {fail_count}개 실패")


# Blog posts data (from local database)
BLOGS_DATA = [
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
    },
    {
        "title": "슬로푸스의 Happy: 자연어 처리의 새로운 도전",
        "slug": "sloopus-happy-nlp-challenge",
        "excerpt": "AI 기반 자연어 처리 프로젝트인 '슬로푸스의 Happy'를 통해 감정 분석과 텍스트 생성의 새로운 가능성을 탐구합니다.",
        "content": """# 슬로푸스의 Happy: 자연어 처리의 새로운 도전

## 프로젝트 소개

'슬로푸스의 Happy'는 AI 기반 감정 분석 및 텍스트 생성 프로젝트입니다.

## 주요 기술

### NLP 모델
최신 자연어 처리 기술을 활용한 감정 분석

### 텍스트 생성
트랜스포머 기반 모델로 자연스러운 텍스트 생성

## 성과

다양한 감정 표현을 정확히 분석하고, 맥락에 맞는 응답을 생성합니다.

자연어 처리의 미래를 함께 만들어갑니다! 🌟
""",
        "status": "published",
        "tags": ["NLP", "AI", "감정분석", "텍스트생성"]
    }
]

# Projects data (from migrate_projects.py)
PROJECTS_DATA = [
    {
        "name": "CutStudio",
        "slug": "cutstudio",
        "description": "직관적이고 강력한 비디오 편집 도구로, 전문가부터 초보자까지 모두가 쉽게 사용할 수 있는 스튜디오급 편집 환경을 제공합니다.",
        "content": """# CutStudio

AI 기반 비디오 편집 자동화 도구로 교육용 영상 편집 시간을 10시간에서 15분으로 단축합니다. 화자 분리, 자동 침묵 제거, 음성-텍스트 변환을 통해 편집 효율을 97.5% 향상시킵니다.

## 주요 기능
- 최대 10명의 화자를 개별 타임라인으로 자동 분리
- 3초 이상 침묵 및 말더듬(음, 어) 자동 제거로 영상 길이 50% 단축
- 95% 정확도의 음성 인식 및 SRT 자막 자동 생성
- Gemini AI 기반 영상 요약
- Streamlit 기반 직관적인 웹 인터페이스

## 기술 스택
- **Language**: Python 3.11+
- **Framework**: Streamlit 1.29.0
- **AI**: Whisper, PyAnnote, Gemini
- **Processing**: MoviePy, FFmpeg
""",
        "github_url": "https://github.com/jeromwolf/CutStudio",
        "demo_url": None,
        "thumbnail_url": None,
        "tech_stack": ["Python", "Streamlit", "Whisper", "PyAnnote", "Gemini", "MoviePy", "FFmpeg"],
        "status": "completed",
        "category": "Video",
        "difficulty": "Advanced"
    },
    {
        "name": "StockAI",
        "slug": "stockai",
        "description": "AI 기반 주식 분석 플랫폼으로 머신러닝과 빅데이터를 활용하여 투자자들에게 정확한 시장 분석과 예측을 제공합니다.",
        "content": """# StockAI

A2A 멀티에이전트 시스템을 기반으로 한 실시간 주식 분석 챗봇 서비스입니다. 5개의 전문 AI 에이전트가 협업하여 자연어 질문을 분석하고 기술적/재무적 분석 결과를 제공합니다.

## 주요 기능
- 자연어 이해, 재무 분석, 기술적 분석, 감성 분석, 실시간 가격 데이터 에이전트 협업
- Yahoo Finance, DART, SEC 공시 데이터 통합 분석
- Reddit, StockTwits 등 소셜 미디어 감성 분석
- WebSocket 기반 실시간 데이터 스트리밍
- 가중치 기반 데이터 소스 신뢰도 시스템

## 기술 스택
- **Backend**: FastAPI, Python 3.8+
- **Frontend**: Next.js
- **Database**: PostgreSQL 12+, Redis 6+
- **Deployment**: uvicorn
""",
        "github_url": "https://github.com/jeromwolf/greatworld",
        "demo_url": None,
        "thumbnail_url": None,
        "tech_stack": ["FastAPI", "Python", "Next.js", "PostgreSQL", "Redis"],
        "status": "completed",
        "category": "AI/ML",
        "difficulty": "Advanced"
    },
    {
        "name": "MP4 압축 도구",
        "slug": "mp4-compress",
        "description": "고품질을 유지하면서 동영상 파일 크기를 효율적으로 줄여주는 강력한 압축 유틸리티입니다.",
        "content": """# MP4 압축 도구

MP4 영상 파일의 용량을 고품질을 유지하면서 대폭 줄여주는 압축 유틸리티입니다. H.265(HEVC) 코덱을 사용하여 CLI와 GUI 두 가지 인터페이스를 제공하며, CRF 값 조정을 통해 품질과 용량의 균형을 맞출 수 있습니다.

## 주요 기능
- H.265(HEVC) 코덱 기반 고효율 압축
- CLI 및 GUI 인터페이스 모두 지원
- CRF(Constant Rate Factor) 값 조정으로 압축률 제어
- 실시간 압축 진행률 표시
- 특수문자 포함 파일 경로 처리 지원

## 기술 스택
- **Language**: Python 3.x
- **Processing**: FFmpeg
- **GUI**: Tkinter
- **Packaging**: PyInstaller

## 사용 예시
```bash
python mp4_compressor.py video.mp4 --crf 26
```
""",
        "github_url": "https://github.com/ryhyh98/MP4Compress",
        "demo_url": None,
        "thumbnail_url": None,
        "tech_stack": ["Python", "FFmpeg", "Tkinter", "PyInstaller"],
        "status": "completed",
        "category": "Video",
        "difficulty": "Intermediate"
    },
    {
        "name": "유튜브 다운로더",
        "slug": "youtube-downloader",
        "description": "유튜브 영상과 음악을 고품질로 다운로드할 수 있는 사용자 친화적인 유틸리티입니다.",
        "content": """# 유튜브 다운로더

YouTube 동영상과 오디오를 간편하게 다운로드할 수 있는 GUI 애플리케이션입니다. 1080p, 720p, 480p 등 다양한 해상도를 지원하며, MP3 오디오 추출 기능도 제공합니다.

## 주요 기능
- 1080p, 720p, 480p 등 다양한 해상도 선택 가능
- MP3 오디오 전용 다운로드 지원
- 직관적인 GUI 인터페이스
- 실시간 다운로드 진행률 표시
- downloads 폴더에 자동 저장

## 기술 스택
- **Language**: Python 3
- **Downloader**: yt-dlp
- **Processing**: FFmpeg
- **GUI**: Tkinter

## 사용 예시
YouTube URL 붙여넣기 → 해상도 선택 → 다운로드 버튼 클릭
""",
        "github_url": "https://github.com/ryhyh98/YoutubeDownload",
        "demo_url": None,
        "thumbnail_url": None,
        "tech_stack": ["Python", "yt-dlp", "FFmpeg", "Tkinter"],
        "status": "completed",
        "category": "Video",
        "difficulty": "Beginner"
    },
    {
        "name": "도커 관리 사이트",
        "slug": "docker-management",
        "description": "Docker 컨테이너와 이미지를 쉽게 관리할 수 있는 웹 기반 대시보드로 개발 워크플로우를 향상시킵니다.",
        "content": """# 도커 관리 사이트

Docker 컨테이너, 이미지, 볼륨, 네트워크를 웹 인터페이스에서 관리할 수 있는 관리 도구입니다. 복잡한 CLI 명령어 없이 직관적인 대시보드에서 Docker 리소스를 모니터링하고 제어할 수 있습니다.

## 주요 기능
- 컨테이너 시작/중지/재시작 원클릭 제어
- 이미지 풀/삭제 관리 및 태그 조회
- 볼륨 및 네트워크 생성/삭제 기능
- 실시간 컨테이너 로그 모니터링
- 리소스 사용량 대시보드

## 기술 스택
- **Backend**: Python, Flask
- **API**: Docker SDK for Python
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker
""",
        "github_url": None,
        "demo_url": "https://codeindocker.com/mains/list",
        "thumbnail_url": None,
        "tech_stack": ["Python", "Flask", "Docker SDK", "HTML", "CSS", "JavaScript"],
        "status": "completed",
        "category": "DevOps",
        "difficulty": "Intermediate"
    },
    {
        "name": "Crypto Factory",
        "slug": "crypto-factory",
        "description": "실시간 암호화폐 시장 데이터와 차트 분석을 제공하는 종합 플랫폼입니다.",
        "content": """# Crypto Factory

암호화폐 자동 거래 및 백테스팅 플랫폼으로, 다양한 거래소 API를 통합하고 사용자 정의 전략을 테스트할 수 있습니다. 실시간 시장 데이터 분석과 자동 매매 실행을 지원합니다.

## 주요 기능
- 다중 거래소 API 통합 (Binance, Upbit 등)
- 사용자 정의 매매 전략 백테스팅
- 실시간 시장 데이터 모니터링
- 자동 매매 실행 엔진
- 수익률 및 리스크 분석 대시보드

## 기술 스택
- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Deployment**: Docker

## 사용 예시
전략 코드 작성 → 백테스팅 실행 → 결과 분석 → 실전 자동 거래 적용
""",
        "github_url": None,
        "demo_url": "https://crypto-factory.cloud",
        "thumbnail_url": None,
        "tech_stack": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "status": "in_progress",
        "category": "Finance",
        "difficulty": "Advanced"
    },
    {
        "name": "PayLens",
        "slug": "paylens",
        "description": "한국과 미국의 공식 정부 통계를 기반으로 연봉 퍼센타일을 분석해주는 현대적인 웹 애플리케이션입니다.",
        "content": """# PayLens

내 연봉은 상위 몇%? 정확한 데이터로 당신의 소득 위치를 렌즈처럼 선명하게 보여드립니다. 국세청과 US Census Bureau의 2024년 공식 데이터를 기반으로 한국과 미국의 소득 분위를 실시간으로 분석합니다.

## 주요 기능
- 실시간 소득 백분위 분석 (한국/미국)
- 국세청 및 US Census Bureau 2024년 공식 데이터 기반
- 목표 소득 설정 및 격차 분석
- 국가 간 소득 비교 기능
- Framer Motion 기반 부드러운 애니메이션

## 기술 스택
- **Framework**: Next.js 15.5.3
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Deployment**: Vercel

## 사용 예시
연봉 입력 시 실시간으로 상위 몇%인지 분석하고 목표 소득과의 격차 확인
""",
        "github_url": "https://github.com/jeromwolf/paylens",
        "demo_url": "https://paylens-kappa.vercel.app",
        "thumbnail_url": None,
        "tech_stack": ["Next.js", "TypeScript", "Tailwind CSS", "Vercel"],
        "status": "completed",
        "category": "Finance",
        "difficulty": "Intermediate"
    },
    {
        "name": "백테스팅 프레임워크 (소스코드)",
        "slug": "backtesting-framework",
        "description": "트레이딩 전략을 검증하는 오픈소스 백테스팅 프레임워크입니다.",
        "content": """# 백테스팅 프레임워크

주식 및 암호화폐 거래 전략을 과거 데이터로 검증하는 백테스팅 프레임워크입니다. 다양한 기술적 지표와 커스텀 전략을 지원하며, 상세한 성과 분석 리포트를 제공합니다.

prd.md 파일만으로 원하는 도구에서 직접 코드를 생성할 수 있어, 개발자가 자신만의 백테스팅 시스템을 빠르게 구축할 수 있습니다.

## 주요 기능
- 다양한 기술적 지표 내장 (MA, RSI, MACD, Bollinger Bands 등)
- 커스텀 전략 작성 및 테스트
- 상세한 수익률, 샤프 비율, MDD 분석
- 캔들스틱 차트와 매매 시점 시각화
- CSV 데이터 임포트 지원

## 기술 스택
- **Language**: Python
- **Libraries**: pandas, numpy, matplotlib
- **Indicators**: TA-Lib
- **Analysis**: scipy, sklearn

## 사용 예시
전략 함수 정의 → 과거 데이터 로드 → 백테스트 실행 → 성과 지표 확인
""",
        "github_url": "https://github.com/simverse/TradingBackTester",
        "demo_url": None,
        "thumbnail_url": None,
        "tech_stack": ["Python", "pandas", "numpy", "matplotlib", "TA-Lib"],
        "status": "completed",
        "category": "Finance",
        "difficulty": "Advanced"
    },
    {
        "name": "백테스팅 시스템 (웹 UI)",
        "slug": "backtesting-webui",
        "description": "웹 브라우저에서 바로 사용할 수 있는 인터랙티브 백테스팅 시스템입니다.",
        "content": """# 백테스팅 시스템 (웹 UI)

백테스팅 프레임워크를 웹 인터페이스로 제공하는 대시보드입니다. 코딩 없이 드래그 앤 드롭으로 전략을 구성하고, 실시간으로 백테스트 결과를 시각화할 수 있습니다.

다양한 트레이딩 전략을 선택하고, 기간 설정 및 초기 자본을 조정하며 상세한 성과 분석과 차트를 확인할 수 있습니다.

## 주요 기능
- 노코드 전략 빌더 (드래그 앤 드롭)
- 실시간 백테스트 결과 시각화
- 인터랙티브 차트 및 성과 대시보드
- 다중 전략 비교 분석
- 전략 템플릿 라이브러리

## 기술 스택
- **Frontend**: React, TypeScript
- **Backend**: FastAPI, Python
- **Charts**: Chart.js, D3.js
- **Deployment**: Vercel, Railway

## 사용 예시
전략 블록 조합 → 종목 및 기간 선택 → 백테스트 실행 → 대시보드에서 결과 확인
""",
        "github_url": "https://github.com/jeromwolf/Backtesting",
        "demo_url": "https://backtesting-flux.up.railway.app",
        "thumbnail_url": None,
        "tech_stack": ["React", "TypeScript", "FastAPI", "Python", "Chart.js", "D3.js"],
        "status": "completed",
        "category": "Finance",
        "difficulty": "Intermediate"
    },
    {
        "name": "종합소득세 계산기",
        "slug": "income-tax-calculator",
        "description": "금융이자소득, 배당금, 양도소득세 등 복잡한 소득세 항목별 세액을 정확하게 계산해주는 종합 세무 프로그램입니다.",
        "content": """# 종합소득세 계산기

근로소득이 있으면서 금융소득이 2백만원을 초과하는 개인을 위한 웹 기반 종합 금융소득세 계산기입니다. 추가 세금, 해외 ETF 양도소득세, 외국 ETF 배당금 원천징수세, 추가 건강보험료를 정확하게 계산합니다.

## 주요 기능
- MAX(A, B) 방식의 종합소득세 정확한 계산
- 해외 ETF 양도소득세 자동 계산
- 외국 ETF 배당금 원천징수세 정보 제공
- 금융소득 기반 추가 건강보험료 계산
- 직관적인 단일 페이지 인터페이스와 투명한 계산 과정
- 다양한 금융소득 시나리오 지원 (이자, 배당, 양도차익)

## 기술 스택
- **Language**: Python 3.8+
- **Backend**: Flask
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Flask app / Windows exe

## 사용 예시
근로소득과 금융소득 입력 → 공식 세율표 기반 종합소득세 계산 → 추가 세금, ETF 세금, 건강보험료 확인
""",
        "github_url": "https://github.com/ryhyh98/TaxVibe",
        "demo_url": None,
        "thumbnail_url": None,
        "tech_stack": ["Python", "Flask", "HTML", "CSS", "JavaScript"],
        "status": "completed",
        "category": "Finance",
        "difficulty": "Intermediate"
    },
    {
        "name": "WorldFlow",
        "slug": "worldflow",
        "description": "AI 기반 PDF 번역 시스템으로 한국어 강의 자료를 해외 강사에게 빠르고 정확하게 전달합니다.",
        "content": """# WorldFlow

AI 기반 PDF 번역 플랫폼으로 한국어 교육 자료를 국제 학술 활동에 맞게 영문으로 번역합니다. 표, 차트, 이미지를 포함한 원본 레이아웃을 유지하면서 3-5분 내에 빠른 번역이 가능합니다.

PDF → Markdown → AI 번역 → 편집 → PDF 생성까지 한 번에 처리하는 통합 솔루션입니다.

## 주요 기능
- 🚀 Quick Mode: 3-5분 내 빠른 번역 처리
- 👨‍🏫 Pro Mode: 실시간 마크다운 편집 및 고품질 전문 번역
- 📊 원본 문서 레이아웃 보존 (표, 차트, 이미지 유지)
- ✏️ 실시간 마크다운 편집 인터페이스 및 라이브 프리뷰
- 🔧 번역 전체에 걸친 용어 일관성 유지

## 기술 스택
- **Backend**: Python 3.11+, FastAPI, PostgreSQL, Redis, Celery
- **Frontend**: TypeScript, React 18, Vite, TailwindCSS
- **Processing**: PyMuPDF
- **Deployment**: Railway

## 사용 예시
PDF 업로드 → Markdown 변환 → AI 번역 → 실시간 편집 → PDF 생성 및 다운로드
""",
        "github_url": "https://github.com/jeromwolf/WorldFlow",
        "demo_url": "https://worldflow-frontend.up.railway.app",
        "thumbnail_url": None,
        "tech_stack": ["Python", "FastAPI", "PostgreSQL", "Redis", "Celery", "TypeScript", "React", "Vite", "TailwindCSS"],
        "status": "completed",
        "category": "AI/ML",
        "difficulty": "Advanced"
    },
    {
        "name": "사업계획서 도우미 MCP",
        "slug": "business-plan-mcp",
        "description": "AI를 활용하여 전문적인 사업계획서 작성을 도와주는 혁신적인 Model Context Protocol 기반 도구입니다.",
        "content": """# 사업계획서 도우미 MCP

엑셀 사업계획서 데이터를 한글(HWP) 문서로 자동 변환하는 AI 기반 도구입니다. Model Context Protocol(MCP)을 활용하여 AI 기반 콘텐츠 분석 및 개선 제안을 제공하며, 전문적인 사업계획서 작성을 쉽고 효율적으로 만듭니다.

## 주요 기능
- Excel → HWP 변환 (DOCX 중간 포맷 처리)
- HWP 호환성을 위한 특수문자 자동 처리
- 한글 텍스트를 위한 멀티 인코딩 지원 (UTF-8, EUC-KR, CP949)
- 변환 중 복잡한 표 구조 보존
- 드래그 앤 드롭 파일 업로드 및 실시간 미리보기
- 3개 전문 템플릿: 표준 사업계획서, VC 투자제안서, 정부 프로젝트 제안서
- MCP 기반 AI 콘텐츠 분석 및 개선 제안
- 대용량 파일 지원 (10,000+ 행)
- 커스터마이징 가능한 템플릿

## 기술 스택
- **Language**: TypeScript
- **Framework**: Electron (Windows, macOS, Linux)
- **Frontend**: React
- **AI**: MCP (Model Context Protocol)
- **Libraries**: xlsx, docx, iconv-lite, sharp

## 사용 예시
앱 실행 → Excel 파일 드래그 앤 드롭 → 템플릿 선택 → 특수문자 처리된 DOCX 변환 → AI MCP 분석 및 개선 제안 → 최종 HWP 문서 생성
""",
        "github_url": "https://github.com/jeromwolf/business-plan-hwp-mcp",
        "demo_url": None,
        "thumbnail_url": None,
        "tech_stack": ["TypeScript", "Electron", "React", "MCP", "xlsx", "docx"],
        "status": "in_progress",
        "category": "AI/ML",
        "difficulty": "Advanced"
    }
]


def main():
    """Main function"""
    print("=" * 60)
    print("🚀 Render 프로덕션 데이터 업로드")
    print(f"📍 API URL: {BASE_URL}")
    print("=" * 60)

    # Step 1: Create admin user
    create_admin_user()

    # Step 2: Login
    token = login()
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Delete existing data
    delete_existing_blogs(headers)
    delete_existing_projects(headers)

    # Step 4: Upload new data
    upload_blogs(headers, BLOGS_DATA)
    upload_projects(headers, PROJECTS_DATA)

    print("\n" + "=" * 60)
    print("🎉 업로드 완료!")
    print(f"📊 Frontend: https://gongjakso-tft-frontend.onrender.com")
    print(f"📊 Backend: {BASE_URL}")
    print("=" * 60)


if __name__ == "__main__":
    main()
