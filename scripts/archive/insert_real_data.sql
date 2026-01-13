-- Insert 12 Real Projects

INSERT INTO projects (name, slug, description, content, github_url, demo_url, thumbnail_url, tech_stack, status, category, difficulty, view_count, star_count) VALUES
('CutStudio', 'cutstudio', '직관적이고 강력한 비디오 편집 도구로, 전문가부터 초보자까지 모두가 쉽게 사용할 수 있는 스튜디오급 편집 환경을 제공합니다.', '# CutStudio

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
- **Processing**: MoviePy, FFmpeg', 'https://github.com/jeromwolf/CutStudio', NULL, NULL, '["Python", "Streamlit", "Whisper", "PyAnnote", "Gemini", "MoviePy", "FFmpeg"]'::jsonb, 'COMPLETED', 'Video', 'Advanced', 0, 0),

('StockAI', 'stockai', 'AI 기반 주식 분석 플랫폼으로 머신러닝과 빅데이터를 활용하여 투자자들에게 정확한 시장 분석과 예측을 제공합니다.', '# StockAI

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
- **Deployment**: uvicorn', 'https://github.com/jeromwolf/greatworld', NULL, NULL, '["FastAPI", "Python", "Next.js", "PostgreSQL", "Redis"]'::jsonb, 'COMPLETED', 'AI/ML', 'Advanced', 0, 0),

('MP4 압축 도구', 'mp4-compress', '고품질을 유지하면서 동영상 파일 크기를 효율적으로 줄여주는 강력한 압축 유틸리티입니다.', '# MP4 압축 도구

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
```', 'https://github.com/ryhyh98/MP4Compress', NULL, NULL, '["Python", "FFmpeg", "Tkinter", "PyInstaller"]'::jsonb, 'COMPLETED', 'Video', 'Intermediate', 0, 0),

('유튜브 다운로더', 'youtube-downloader', '유튜브 영상과 음악을 고품질로 다운로드할 수 있는 사용자 친화적인 유틸리티입니다.', '# 유튜브 다운로더

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
YouTube URL 붙여넣기 → 해상도 선택 → 다운로드 버튼 클릭', 'https://github.com/ryhyh98/YoutubeDownload', NULL, NULL, '["Python", "yt-dlp", "FFmpeg", "Tkinter"]'::jsonb, 'COMPLETED', 'Video', 'Beginner', 0, 0),

('도커 관리 사이트', 'docker-management', 'Docker 컨테이너와 이미지를 쉽게 관리할 수 있는 웹 기반 대시보드로 개발 워크플로우를 향상시킵니다.', '# 도커 관리 사이트

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
- **Deployment**: Docker', NULL, 'https://codeindocker.com/mains/list', NULL, '["Python", "Flask", "Docker SDK", "HTML", "CSS", "JavaScript"]'::jsonb, 'COMPLETED', 'DevOps', 'Intermediate', 0, 0),

('Crypto Factory', 'crypto-factory', '실시간 암호화폐 시장 데이터와 차트 분석을 제공하는 종합 플랫폼입니다.', '# Crypto Factory

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
전략 코드 작성 → 백테스팅 실행 → 결과 분석 → 실전 자동 거래 적용', NULL, 'https://crypto-factory.cloud', NULL, '["Python", "FastAPI", "PostgreSQL", "Docker"]'::jsonb, 'IN_PROGRESS', 'Finance', 'Advanced', 0, 0),

('PayLens', 'paylens', '한국과 미국의 공식 정부 통계를 기반으로 연봉 퍼센타일을 분석해주는 현대적인 웹 애플리케이션입니다.', '# PayLens

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
연봉 입력 시 실시간으로 상위 몇%인지 분석하고 목표 소득과의 격차 확인', 'https://github.com/jeromwolf/paylens', 'https://paylens-kappa.vercel.app', NULL, '["Next.js", "TypeScript", "Tailwind CSS", "Vercel"]'::jsonb, 'COMPLETED', 'Finance', 'Intermediate', 0, 0),

('백테스팅 프레임워크 (소스코드)', 'backtesting-framework', '트레이딩 전략을 검증하는 오픈소스 백테스팅 프레임워크입니다.', '# 백테스팅 프레임워크

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
전략 함수 정의 → 과거 데이터 로드 → 백테스트 실행 → 성과 지표 확인', 'https://github.com/simverse/TradingBackTester', NULL, NULL, '["Python", "pandas", "numpy", "matplotlib", "TA-Lib"]'::jsonb, 'COMPLETED', 'Finance', 'Advanced', 0, 0),

('백테스팅 시스템 (웹 UI)', 'backtesting-webui', '웹 브라우저에서 바로 사용할 수 있는 인터랙티브 백테스팅 시스템입니다.', '# 백테스팅 시스템 (웹 UI)

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
전략 블록 조합 → 종목 및 기간 선택 → 백테스트 실행 → 대시보드에서 결과 확인', 'https://github.com/jeromwolf/Backtesting', 'https://backtesting-flux.up.railway.app', NULL, '["React", "TypeScript", "FastAPI", "Python", "Chart.js", "D3.js"]'::jsonb, 'COMPLETED', 'Finance', 'Intermediate', 0, 0),

('종합소득세 계산기', 'income-tax-calculator', '금융이자소득, 배당금, 양도소득세 등 복잡한 소득세 항목별 세액을 정확하게 계산해주는 종합 세무 프로그램입니다.', '# 종합소득세 계산기

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
근로소득과 금융소득 입력 → 공식 세율표 기반 종합소득세 계산 → 추가 세금, ETF 세금, 건강보험료 확인', 'https://github.com/ryhyh98/TaxVibe', NULL, NULL, '["Python", "Flask", "HTML", "CSS", "JavaScript"]'::jsonb, 'COMPLETED', 'Finance', 'Intermediate', 0, 0),

('WorldFlow', 'worldflow', 'AI 기반 PDF 번역 시스템으로 한국어 강의 자료를 해외 강사에게 빠르고 정확하게 전달합니다.', '# WorldFlow

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
PDF 업로드 → Markdown 변환 → AI 번역 → 실시간 편집 → PDF 생성 및 다운로드', 'https://github.com/jeromwolf/WorldFlow', 'https://worldflow-frontend.up.railway.app', NULL, '["Python", "FastAPI", "PostgreSQL", "Redis", "Celery", "TypeScript", "React", "Vite", "TailwindCSS"]'::jsonb, 'COMPLETED', 'AI/ML', 'Advanced', 0, 0),

('사업계획서 도우미 MCP', 'business-plan-mcp', 'AI를 활용하여 전문적인 사업계획서 작성을 도와주는 혁신적인 Model Context Protocol 기반 도구입니다.', '# 사업계획서 도우미 MCP

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
앱 실행 → Excel 파일 드래그 앤 드롭 → 템플릿 선택 → 특수문자 처리된 DOCX 변환 → AI MCP 분석 및 개선 제안 → 최종 HWP 문서 생성', 'https://github.com/jeromwolf/business-plan-hwp-mcp', NULL, NULL, '["TypeScript", "Electron", "React", "MCP", "xlsx", "docx"]'::jsonb, 'IN_PROGRESS', 'AI/ML', 'Advanced', 0, 0);
