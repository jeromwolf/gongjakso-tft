# Azure 마이그레이션 가이드 - AI ON

Render.com → Azure App Service 완전 마이그레이션 가이드

**목표**: 무료 플랜 만료로 인해 Render에서 Azure로 전환

**선택한 아키텍처**:
- Backend: Azure App Service (Docker)
- Frontend: Azure Static Web Apps (추천) 또는 App Service
- Database: Azure Database for PostgreSQL (Flexible Server)

---

## 📋 마이그레이션 체크리스트

- [ ] Azure 리소스 생성
- [ ] PostgreSQL 데이터베이스 설정
- [ ] Backend App Service 배포
- [ ] Frontend Static Web Apps 배포
- [ ] 환경 변수 설정
- [ ] 데이터 마이그레이션 (스크립트 실행)
- [ ] DNS 설정 (aion.io.kr)
- [ ] 테스트 및 검증

---

## 💰 예상 비용 (월간)

### Azure 무료 플랜 활용
- **PostgreSQL Flexible Server**: Burstable B1ms (~$12/월)
- **App Service (Backend)**: Free/Basic B1 (~$13/월)
- **Static Web Apps (Frontend)**: Free (100GB 대역폭)
- **총 예상**: $25-30/월 (Render와 비슷하거나 저렴)

**무료 크레딧 $200 사용 시**: 약 6-8개월 무료 운영 가능 🎉

---

## 🏗️ Phase 1: Azure 리소스 생성

### 1-1. 리소스 그룹 생성

Azure Portal (https://portal.azure.com) 접속 후:

```bash
# Azure CLI 사용 (선택)
az login
az group create \
  --name aion-rg \
  --location koreacentral  # 한국 중부
```

**Portal에서**:
1. "리소스 그룹" 검색
2. "+ 만들기" 클릭
3. 이름: `aion-rg`
4. 지역: `Korea Central` (한국 중부)

---

### 1-2. PostgreSQL Flexible Server 생성

**Portal에서**:
1. "Azure Database for PostgreSQL flexible servers" 검색
2. "+ 만들기" 클릭

**설정**:
- **리소스 그룹**: `aion-rg`
- **서버 이름**: `aion-postgres` (전역 고유 이름)
- **지역**: Korea Central
- **PostgreSQL 버전**: 16 또는 17
- **컴퓨팅 + 스토리지**:
  - 계층: Burstable
  - 컴퓨팅 크기: B1ms (1 vCore, 2GB RAM)
  - 스토리지: 32GB
- **인증**:
  - 관리자 사용자 이름: `postgres`
  - 암호: 강력한 비밀번호 설정 (메모할 것!)

**네트워크**:
- 연결 방법: "공용 액세스(허용된 IP 주소)"
- 방화벽 규칙: "Azure 서비스 및 리소스가 이 서버에 액세스하도록 허용" 체크

**생성 후**:
```bash
# 연결 문자열 (메모)
Server: aion-postgres.postgres.database.azure.com
Database: postgres (기본) → 나중에 aion_db 생성
User: postgres
Password: <설정한 비밀번호>
```

---

### 1-3. 데이터베이스 생성

**Azure Cloud Shell 또는 로컬 psql**:
```bash
# 접속
psql "host=aion-postgres.postgres.database.azure.com port=5432 dbname=postgres user=postgres password=<비밀번호> sslmode=require"

# 데이터베이스 생성
CREATE DATABASE aion_db;

# 확인
\l
\q
```

**DATABASE_URL** (메모):
```
postgresql+asyncpg://postgres:<비밀번호>@aion-postgres.postgres.database.azure.com:5432/aion_db?ssl=require
```

---

## 🐳 Phase 2: Backend App Service 배포

### 2-1. Azure Container Registry (선택사항)

Docker 이미지를 Azure에 푸시하려면 필요:

```bash
# 1. Container Registry 생성
az acr create \
  --resource-group aion-rg \
  --name aionregistry \
  --sku Basic \
  --location koreacentral

# 2. 관리자 사용자 활성화
az acr update -n aionregistry --admin-enabled true

# 3. 자격 증명 확인
az acr credential show -n aionregistry
# 메모: loginServer, username, password
```

---

### 2-2. Backend Dockerfile 수정 (선택)

현재 `backend/Dockerfile`을 Azure 최적화:

**옵션 A: 현재 Dockerfile 그대로 사용** (권장)
- 이미 프로덕션 준비됨

**옵션 B: Multi-stage 빌드로 최적화**:
```dockerfile
# backend/Dockerfile.azure (새 파일)
FROM python:3.11-slim as builder

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 프로덕션 스테이지
FROM python:3.11-slim

WORKDIR /app

# 빌더에서 패키지 복사
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 앱 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 2-3. Docker 이미지 빌드 및 푸시

**방법 1: 로컬에서 빌드 (권장)**

```bash
# 1. Azure Container Registry 로그인
az acr login --name aionregistry

# 2. 이미지 빌드
cd backend
docker build -t aionregistry.azurecr.io/aion-backend:latest .

# 3. 푸시
docker push aionregistry.azurecr.io/aion-backend:latest
```

**방법 2: Azure에서 직접 빌드 (더 간단)**

```bash
# GitHub 리포지토리에서 직접 빌드
az acr build \
  --registry aionregistry \
  --image aion-backend:latest \
  --file backend/Dockerfile \
  https://github.com/jeromwolf/gongjakso-tft.git#main
```

---

### 2-4. Backend App Service 생성

**Portal에서**:
1. "App Services" 검색 → "+ 만들기"

**설정**:
- **리소스 그룹**: `aion-rg`
- **이름**: `aion-backend` (전역 고유)
- **게시**: 컨테이너
- **운영 체제**: Linux
- **지역**: Korea Central
- **가격 책정 계획**:
  - 새로 만들기: `aion-plan`
  - SKU: B1 (Basic, $13/월) 또는 F1 (Free, 제한적)

**Docker 설정**:
- **옵션**: 단일 컨테이너
- **이미지 원본**: Azure Container Registry
- **레지스트리**: `aionregistry`
- **이미지**: `aion-backend`
- **태그**: `latest`

**만들기** 클릭!

---

### 2-5. Backend 환경 변수 설정

App Service 생성 후:

1. 왼쪽 메뉴 → **구성** → **애플리케이션 설정**
2. "+ 새 애플리케이션 설정" 클릭

**필수 환경 변수**:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:<비밀번호>@aion-postgres.postgres.database.azure.com:5432/aion_db?ssl=require

SECRET_KEY=<32자 이상 강력한 랜덤 키>

CORS_ORIGINS=["http://localhost:3000","https://aion-frontend.azurestaticapps.net","https://aion.io.kr","https://www.aion.io.kr"]

DEBUG=false

# AI Services (있으면)
ANTHROPIC_API_KEY=<키>
OPENAI_API_KEY=<키>

# Email (있으면)
RESEND_API_KEY=<키>
FROM_EMAIL=noreply@aion.io.kr

# App Info
APP_NAME=AI ON API
APP_VERSION=1.0.0
```

**저장** 후 **다시 시작**

---

### 2-6. Backend 접속 테스트

URL: `https://aion-backend.azurewebsites.net`

```bash
# Health Check
curl https://aion-backend.azurewebsites.net/api/health

# API Docs
open https://aion-backend.azurewebsites.net/api/docs
```

---

## 🌐 Phase 3: Frontend Static Web Apps 배포

### 3-1. Static Web Apps 생성

**Portal에서**:
1. "Static Web Apps" 검색 → "+ 만들기"

**설정**:
- **리소스 그룹**: `aion-rg`
- **이름**: `aion-frontend`
- **계획 유형**: Free
- **지역**: East Asia (무료는 지역 선택 불가)
- **배포 세부 정보**:
  - **소스**: GitHub
  - **조직**: jeromwolf
  - **리포지토리**: gongjakso-tft
  - **분기**: main

**빌드 세부 정보**:
- **빌드 사전 설정**: Next.js
- **앱 위치**: `/frontend`
- **API 위치**: (비워두기)
- **출력 위치**: `.next`

**만들기** 클릭!

---

### 3-2. Frontend 환경 변수 설정

1. Static Web App → **구성** → **애플리케이션 설정**
2. 추가:

```bash
NEXT_PUBLIC_API_URL=https://aion-backend.azurewebsites.net
NODE_ENV=production
```

---

### 3-3. 배포 확인

GitHub Actions가 자동으로 트리거됨:
- GitHub 리포지토리 → **Actions** 탭에서 진행 상황 확인
- 완료 후 URL: `https://aion-frontend.azurestaticapps.net`

---

## 📦 Phase 4: 데이터 마이그레이션

### 4-1. Admin 계정 및 데이터 생성

```bash
cd backend

# Python 가상환경
python3 -m venv venv
source venv/bin/activate

# 환경 변수 설정
export DATABASE_URL="postgresql+asyncpg://postgres:<비밀번호>@aion-postgres.postgres.database.azure.com:5432/aion_db?ssl=require"
export OPENAI_API_KEY="<키>"

# 프로덕션 데이터 업로드 스크립트 실행
python3 scripts/upload_to_production.py \
  --api-url https://aion-backend.azurewebsites.net
```

**스크립트 동작**:
1. Admin 계정 생성 (`admin@example.com` / `admin123`)
2. 블로그 6개 업로드
3. 프로젝트 12개 업로드

---

### 4-2. Admin 권한 확인

```bash
# PostgreSQL 접속
psql "host=aion-postgres.postgres.database.azure.com port=5432 dbname=aion_db user=postgres password=<비밀번호> sslmode=require"

# Admin 역할 확인
SELECT email, role FROM users WHERE email = 'admin@example.com';

# 데이터 확인
SELECT COUNT(*) FROM blogs;
SELECT COUNT(*) FROM projects;
```

---

## 🌍 Phase 5: DNS 설정 (aion.io.kr)

### 5-1. 커스텀 도메인 추가

**Static Web App (Frontend)**:
1. Static Web App → **사용자 지정 도메인**
2. "+ 추가" 클릭
3. 도메인 이름: `aion.io.kr`
4. **검증 레코드 추가**:

도메인 등록 업체에서 TXT 레코드 추가:
```
호스트: @
유형: TXT
값: <Azure에서 제공하는 값>
```

5. **CNAME 레코드 추가**:
```
호스트: @
유형: A 또는 ALIAS
값: <Azure Static Web Apps IP 또는 URL>
```

**App Service (Backend)**:
1. App Service → **사용자 지정 도메인**
2. 서브도메인 추가: `api.aion.io.kr`
3. CNAME 레코드:
```
호스트: api
유형: CNAME
값: aion-backend.azurewebsites.net
```

---

### 5-2. SSL 인증서 (무료)

Azure는 자동으로 무료 SSL 인증서 제공:
- Static Web Apps: 자동 HTTPS
- App Service: **사용자 지정 도메인** → **바인딩 추가** → 무료 관리형 인증서

---

## 🧪 Phase 6: 테스트 및 검증

### 6-1. 백엔드 테스트

```bash
# Health Check
curl https://aion-backend.azurewebsites.net/api/health
curl https://api.aion.io.kr/api/health  # DNS 설정 후

# API Docs
open https://aion-backend.azurewebsites.net/api/docs

# 블로그 목록
curl https://aion-backend.azurewebsites.net/api/blog
```

### 6-2. 프론트엔드 테스트

```bash
# 홈페이지 접속
open https://aion-frontend.azurestaticapps.net
open https://aion.io.kr  # DNS 설정 후

# 블로그 페이지
open https://aion.io.kr/blog

# 프로젝트 페이지
open https://aion.io.kr/projects
```

### 6-3. 전체 플로우 테스트

1. 홈페이지 → 블로그 목록 표시 (6개)
2. 블로그 → 프로젝트 목록 표시 (12개)
3. Admin 로그인 (`admin@example.com` / `admin123`)
4. 블로그 작성/수정
5. 프로젝트 작성/수정
6. 뉴스레터 구독

---

## 🔄 Phase 7: GitHub Actions CI/CD 설정

### 7-1. Backend 자동 배포

`.github/workflows/azure-backend.yml` 생성:

```yaml
name: Deploy Backend to Azure

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Login to Azure Container Registry
      uses: docker/login-action@v2
      with:
        registry: aionregistry.azurecr.io
        username: ${{ secrets.ACR_USERNAME }}
        password: ${{ secrets.ACR_PASSWORD }}

    - name: Build and Push Docker Image
      run: |
        cd backend
        docker build -t aionregistry.azurecr.io/aion-backend:${{ github.sha }} .
        docker build -t aionregistry.azurecr.io/aion-backend:latest .
        docker push aionregistry.azurecr.io/aion-backend:${{ github.sha }}
        docker push aionregistry.azurecr.io/aion-backend:latest

    - name: Deploy to Azure App Service
      uses: azure/webapps-deploy@v2
      with:
        app-name: aion-backend
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        images: aionregistry.azurecr.io/aion-backend:latest
```

**GitHub Secrets 추가**:
1. GitHub 리포지토리 → **Settings** → **Secrets and variables** → **Actions**
2. 추가:
   - `ACR_USERNAME`: Azure Container Registry 사용자 이름
   - `ACR_PASSWORD`: Azure Container Registry 비밀번호
   - `AZURE_WEBAPP_PUBLISH_PROFILE`: App Service → **게시 프로필 가져오기**

---

### 7-2. Frontend 자동 배포

Static Web Apps는 자동으로 GitHub Actions 생성됨:
- `.github/workflows/azure-static-web-apps-*.yml` 파일 자동 생성
- `main` 브랜치 푸시 시 자동 배포

---

## 📊 모니터링 및 로그

### Application Insights 활성화

1. App Service → **Application Insights**
2. "Application Insights 켜기"
3. 새로 만들기 또는 기존 리소스 선택

**로그 확인**:
- Azure Portal → App Service → **로그 스트림**
- Application Insights → **로그**, **트랜잭션 검색**

---

## 💡 최적화 팁

### 1. 성능 최적화
- **App Service**: "Always On" 활성화 (콜드 스타트 방지)
- **Static Web Apps**: CDN 자동 활성화됨
- **PostgreSQL**: Connection Pooling (SQLAlchemy 설정 이미 있음)

### 2. 비용 절감
- **App Service**: 개발/스테이징 슬롯 비활성화
- **PostgreSQL**: Burstable 계층 사용 (B1ms)
- **모니터링**: Application Insights 샘플링 조정

### 3. 보안
- **Key Vault**: 중요한 API 키 저장
- **Managed Identity**: App Service가 PostgreSQL에 비밀번호 없이 접속

---

## 🚨 트러블슈팅

### 문제 1: Database Connection 실패

**원인**: PostgreSQL 방화벽 규칙

**해결**:
```bash
# Azure Portal → PostgreSQL → 네트워킹
# "Azure 서비스 및 리소스가 이 서버에 액세스하도록 허용" 체크
```

### 문제 2: CORS 에러

**원인**: CORS_ORIGINS 환경 변수

**해결**:
```bash
# App Service → 구성 → CORS_ORIGINS 확인
# Frontend URL이 포함되어 있는지 확인
```

### 문제 3: Static Web App 빌드 실패

**원인**: 잘못된 빌드 경로

**해결**:
```yaml
# GitHub Actions 워크플로우 확인
app_location: "/frontend"
output_location: ".next"
```

---

## 📝 최종 체크리스트

배포 완료 후 확인:

- [ ] Backend Health: https://aion-backend.azurewebsites.net/api/health
- [ ] Backend API Docs: https://aion-backend.azurewebsites.net/api/docs
- [ ] Frontend: https://aion-frontend.azurestaticapps.net
- [ ] 블로그 목록 표시 (6개)
- [ ] 프로젝트 목록 표시 (12개)
- [ ] Admin 로그인 작동
- [ ] DNS 설정 완료 (aion.io.kr, api.aion.io.kr)
- [ ] SSL 인증서 활성화
- [ ] GitHub Actions CI/CD 작동

---

## 🎯 다음 단계

1. **모니터링 설정**: Application Insights 알림 구성
2. **백업 자동화**: PostgreSQL 자동 백업 활성화
3. **성능 테스트**: JMeter 또는 Artillery로 부하 테스트
4. **문서 업데이트**: README.md, claude.md Azure 정보 추가

---

## 📚 참고 링크

- [Azure App Service 문서](https://docs.microsoft.com/azure/app-service/)
- [Azure Static Web Apps 문서](https://docs.microsoft.com/azure/static-web-apps/)
- [Azure Database for PostgreSQL](https://docs.microsoft.com/azure/postgresql/)
- [Azure Container Registry](https://docs.microsoft.com/azure/container-registry/)

---

**작성일**: 2025-11-17
**작성자**: Elon (Claude Code AI Assistant)

**질문이나 문제가 있으면 언제든지 말씀해주세요!** 🚀
