-- Insert 6 Real Blog Posts (author_id = 1)

INSERT INTO blogs (title, slug, excerpt, content, status, author_id, tags, view_count) VALUES
('FastAPI + Next.js로 풀스택 AI 블로그 플랫폼 개발하기', 'fastapi-nextjs-fullstack-blog-platform', 'FastAPI 백엔드와 Next.js 15 프론트엔드를 사용하여 AI 콘텐츠 자동 생성 기능이 포함된 풀스택 블로그 플랫폼을 만든 과정을 공유합니다.', '# Fast API + Next.js로 풀스택 AI 블로그 플랫폼 개발하기

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

기술 블로그는 [GitHub](https://github.com/jeromwolf/gongjakso-tft)에서 확인하실 수 있습니다!', 'PUBLISHED', 1, '["FastAPI", "Next.js", "AI", "풀스택"]'::jsonb, 0),

('Claude Code와 함께하는 AI 페어 프로그래밍', 'ai-pair-programming-with-claude-code', 'Claude Code를 활용한 AI 페어 프로그래밍 경험을 공유합니다. 개발 속도 향상과 코드 품질 개선 사례를 소개합니다.', '# Claude Code와 함께하는 AI 페어 프로그래밍

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

AI와 함께 더 나은 코드를 작성하세요! 🚀', 'PUBLISHED', 1, '["Claude", "AI", "개발도구", "생산성"]'::jsonb, 0),

('PostgreSQL 비동기 처리로 성능 10배 향상시키기', 'postgresql-async-performance-optimization', 'SQLAlchemy의 비동기 기능과 PostgreSQL을 활용하여 API 응답 속도를 10배 향상시킨 경험을 공유합니다.', '# PostgreSQL 비동기 처리로 성능 10배 향상시키기

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

성능 최적화는 끝이 없습니다. 계속해서 개선해 나가세요! 🚀', 'PUBLISHED', 1, '["PostgreSQL", "성능최적화", "비동기", "SQLAlchemy"]'::jsonb, 0),

('Alembic으로 데이터베이스 마이그레이션 안전하게 관리하기', 'safe-database-migration-with-alembic', 'Alembic을 사용하여 프로덕션 환경에서 안전하게 데이터베이스 스키마를 변경하는 방법과 베스트 프랙티스를 소개합니다.', '# Alembic으로 데이터베이스 마이그레이션 안전하게 관리하기

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

안전한 배포는 안전한 마이그레이션에서 시작됩니다! 🚀', 'PUBLISHED', 1, '["Alembic", "데이터베이스", "마이그레이션", "DevOps"]'::jsonb, 0),

('TypeScript + React Query로 타입 안전한 프론트엔드 만들기', 'type-safe-frontend-with-typescript-react-query', 'TypeScript와 React Query를 활용하여 런타임 에러를 줄이고, 개발 경험을 향상시킨 방법을 공유합니다.', '# TypeScript + React Query로 타입 안전한 프론트엔드 만들기

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

타입 안전성은 개발 속도와 품질을 동시에 향상시킵니다! 💎', 'PUBLISHED', 1, '["TypeScript", "React", "ReactQuery", "타입안전성"]'::jsonb, 0),

('슬로푸스의 Happy: 자연어 처리의 새로운 도전', 'sloopus-happy-nlp-challenge', 'AI 기반 자연어 처리 프로젝트인 ''슬로푸스의 Happy''를 통해 감정 분석과 텍스트 생성의 새로운 가능성을 탐구합니다.', '# 슬로푸스의 Happy: 자연어 처리의 새로운 도전

## 프로젝트 소개

''슬로푸스의 Happy''는 AI 기반 감정 분석 및 텍스트 생성 프로젝트입니다.

## 주요 기술

### NLP 모델
최신 자연어 처리 기술을 활용한 감정 분석

### 텍스트 생성
트랜스포머 기반 모델로 자연스러운 텍스트 생성

## 성과

다양한 감정 표현을 정확히 분석하고, 맥락에 맞는 응답을 생성합니다.

자연어 처리의 미래를 함께 만들어갑니다! 🌟', 'PUBLISHED', 1, '["NLP", "AI", "감정분석", "텍스트생성"]'::jsonb, 0);
