# Azure CLI 완전 자동 배포 가이드

## 🚀 빠른 시작 (3단계)

### 1단계: 사전 준비

```bash
# Azure CLI 설치 확인
az --version

# 없으면 설치
# macOS
brew install azure-cli

# Windows
# https://aka.ms/installazurecliwindows 다운로드

# Linux (Ubuntu/Debian)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

```bash
# Docker 설치 확인
docker --version

# 없으면 설치
# macOS: Docker Desktop 설치
# Linux: sudo apt-get install docker.io
```

```bash
# Azure 로그인
az login
```

### 2단계: 자동 배포 실행

```bash
# 스크립트 실행 권한 부여
chmod +x azure-deploy.sh

# 배포 시작!
./azure-deploy.sh
```

**입력 필요 사항**:
- PostgreSQL 비밀번호 (8자 이상, 대소문자+숫자+특수문자)
- JWT Secret Key (32자 이상) - 자동 생성 가능
- OpenAI API Key (선택)
- Anthropic API Key (선택)
- Resend API Key (선택)

**소요 시간**: 약 10-15분

### 3단계: GitHub Actions 설정 (선택)

```bash
# GitHub CLI 설치
brew install gh

# GitHub 로그인
gh auth login

# Secrets 자동 설정
chmod +x azure-setup-secrets.sh
./azure-setup-secrets.sh
```

---

## 📋 스크립트가 하는 일

`azure-deploy.sh` 스크립트는 다음을 자동으로 수행합니다:

### Phase 1: 리소스 그룹 생성
- Azure 리소스 그룹 `aion-rg` 생성 (한국 중부)

### Phase 2: PostgreSQL 생성
- PostgreSQL Flexible Server 생성 (Standard_B1ms)
- 데이터베이스 `aion_db` 생성
- 방화벽 규칙 설정 (Azure 서비스 허용)

### Phase 3: Container Registry 생성
- Azure Container Registry `aionregistry` 생성
- 관리자 사용자 활성화

### Phase 4: Backend Docker 빌드
- `backend/Dockerfile`로 이미지 빌드
- Container Registry에 푸시

### Phase 5: App Service Plan 생성
- Linux B1 플랜 생성 (Basic tier)

### Phase 6: Backend App Service 배포
- Docker 컨테이너로 App Service 생성
- 환경 변수 자동 설정
- Always On 활성화

### Phase 7: Frontend Static Web App 생성 (선택)
- GitHub 연동 Static Web App 생성
- 자동 빌드/배포 설정

### Phase 8: CORS 설정
- Backend에 Frontend URL 추가

---

## 🛠️ 수동 명령어 (단계별)

스크립트를 사용하지 않고 수동으로 하려면:

### 1. 리소스 그룹 생성

```bash
az group create \
  --name aion-rg \
  --location koreacentral
```

### 2. PostgreSQL 생성

```bash
az postgres flexible-server create \
  --resource-group aion-rg \
  --name aion-postgres \
  --location koreacentral \
  --admin-user postgres \
  --admin-password '<강력한비밀번호>' \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 16 \
  --storage-size 32 \
  --public-access 0.0.0.0
```

```bash
# 방화벽 규칙
az postgres flexible-server firewall-rule create \
  --resource-group aion-rg \
  --name aion-postgres \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

```bash
# 데이터베이스 생성
az postgres flexible-server db create \
  --resource-group aion-rg \
  --server-name aion-postgres \
  --database-name aion_db
```

### 3. Container Registry 생성

```bash
az acr create \
  --resource-group aion-rg \
  --name aionregistry \
  --sku Basic \
  --admin-enabled true
```

```bash
# 자격 증명 확인
az acr credential show --name aionregistry
```

### 4. Docker 이미지 빌드 및 푸시

```bash
# ACR 로그인
az acr login --name aionregistry

# 이미지 빌드
cd backend
docker build -t aionregistry.azurecr.io/aion-backend:latest .

# 푸시
docker push aionregistry.azurecr.io/aion-backend:latest
```

### 5. App Service Plan 생성

```bash
az appservice plan create \
  --resource-group aion-rg \
  --name aion-plan \
  --location koreacentral \
  --is-linux \
  --sku B1
```

### 6. Backend App Service 생성

```bash
az webapp create \
  --resource-group aion-rg \
  --plan aion-plan \
  --name aion-backend \
  --deployment-container-image-name aionregistry.azurecr.io/aion-backend:latest
```

```bash
# ACR 연동
ACR_USERNAME=$(az acr credential show --name aionregistry --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name aionregistry --query passwords[0].value -o tsv)

az webapp config container set \
  --resource-group aion-rg \
  --name aion-backend \
  --docker-custom-image-name aionregistry.azurecr.io/aion-backend:latest \
  --docker-registry-server-url https://aionregistry.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password "$ACR_PASSWORD"
```

### 7. 환경 변수 설정

```bash
az webapp config appsettings set \
  --resource-group aion-rg \
  --name aion-backend \
  --settings \
    DATABASE_URL="postgresql+asyncpg://postgres:<비밀번호>@aion-postgres.postgres.database.azure.com:5432/aion_db?ssl=require" \
    SECRET_KEY="<32자이상랜덤키>" \
    DEBUG="false" \
    APP_NAME="AI ON API" \
    OPENAI_API_KEY="<키>" \
    WEBSITES_PORT=8000
```

### 8. Always On 활성화

```bash
az webapp config set \
  --resource-group aion-rg \
  --name aion-backend \
  --always-on true
```

### 9. Frontend Static Web App 생성

```bash
# GitHub Personal Access Token 필요
az staticwebapp create \
  --resource-group aion-rg \
  --name aion-frontend \
  --location eastasia \
  --source https://github.com/jeromwolf/gongjakso-tft \
  --branch main \
  --app-location "/frontend" \
  --output-location ".next" \
  --token "<GitHub-Token>"
```

```bash
# 환경 변수
az staticwebapp appsettings set \
  --resource-group aion-rg \
  --name aion-frontend \
  --setting-names \
    NEXT_PUBLIC_API_URL="https://aion-backend.azurewebsites.net" \
    NODE_ENV="production"
```

---

## 🧪 배포 후 테스트

### Backend 헬스체크

```bash
curl https://aion-backend.azurewebsites.net/api/health
```

**예상 응답**:
```json
{
  "status": "healthy",
  "message": "All systems operational",
  "database": "connected"
}
```

### API Docs 확인

```bash
open https://aion-backend.azurewebsites.net/api/docs
```

### 로그 확인

```bash
# 실시간 로그 스트림
az webapp log tail \
  --resource-group aion-rg \
  --name aion-backend
```

### 데이터 마이그레이션

```bash
cd backend

# 환경 변수 설정
export DATABASE_URL="postgresql+asyncpg://postgres:<비밀번호>@aion-postgres.postgres.database.azure.com:5432/aion_db?ssl=require"

# Python 가상환경
python3 -m venv venv
source venv/bin/activate

# 스크립트 실행
python3 scripts/upload_to_production.py \
  --api-url https://aion-backend.azurewebsites.net
```

---

## 🔧 유용한 CLI 명령어

### 리소스 목록 확인

```bash
# 리소스 그룹의 모든 리소스
az resource list \
  --resource-group aion-rg \
  --output table
```

### App Service 재시작

```bash
az webapp restart \
  --resource-group aion-rg \
  --name aion-backend
```

### 환경 변수 확인

```bash
az webapp config appsettings list \
  --resource-group aion-rg \
  --name aion-backend \
  --output table
```

### PostgreSQL 연결 문자열 확인

```bash
az postgres flexible-server show-connection-string \
  --server-name aion-postgres \
  --database-name aion_db \
  --admin-user postgres
```

### Container Registry 이미지 목록

```bash
az acr repository list \
  --name aionregistry \
  --output table
```

### Static Web App 배포 토큰 확인

```bash
az staticwebapp secrets list \
  --resource-group aion-rg \
  --name aion-frontend
```

---

## 🗑️ 리소스 삭제 (정리)

**⚠️ 주의: 모든 데이터가 삭제됩니다!**

### 전체 리소스 그룹 삭제

```bash
az group delete \
  --name aion-rg \
  --yes \
  --no-wait
```

### 개별 리소스 삭제

```bash
# Backend App Service만 삭제
az webapp delete \
  --resource-group aion-rg \
  --name aion-backend

# PostgreSQL만 삭제
az postgres flexible-server delete \
  --resource-group aion-rg \
  --name aion-postgres \
  --yes
```

---

## 🚨 트러블슈팅

### 1. Docker 로그인 실패

```bash
# ACR 자격 증명 재확인
az acr credential show --name aionregistry

# Docker 로그인 재시도
az acr login --name aionregistry
```

### 2. App Service 컨테이너 시작 실패

```bash
# 로그 확인
az webapp log tail --resource-group aion-rg --name aion-backend

# 환경 변수 확인
az webapp config appsettings list --resource-group aion-rg --name aion-backend
```

### 3. PostgreSQL 연결 실패

```bash
# 방화벽 규칙 확인
az postgres flexible-server firewall-rule list \
  --resource-group aion-rg \
  --name aion-postgres

# 연결 테스트
psql "host=aion-postgres.postgres.database.azure.com port=5432 dbname=aion_db user=postgres sslmode=require"
```

### 4. Static Web App 빌드 실패

```bash
# GitHub Actions 로그 확인
gh run list --repo jeromwolf/gongjakso-tft

# 워크플로우 재실행
gh run rerun <run-id> --repo jeromwolf/gongjakso-tft
```

---

## 📊 비용 모니터링

### 현재 비용 확인

```bash
# 리소스 그룹 비용
az consumption usage list \
  --start-date $(date -v-30d +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d) \
  --output table
```

### Cost Management

Azure Portal → Cost Management → Cost Analysis에서 시각적으로 확인

---

## 🎯 다음 단계

1. **DNS 설정**: `aion.io.kr` → Static Web App
2. **SSL 인증서**: 자동 발급 확인
3. **모니터링**: Application Insights 설정
4. **백업**: PostgreSQL 자동 백업 활성화
5. **CI/CD**: GitHub Actions 완성

---

**작성일**: 2025-11-17
**질문이나 문제가 있으면 언제든지 말씀해주세요!** 🚀
