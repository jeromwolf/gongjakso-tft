#!/bin/bash

###############################################################################
# Azure 완전 자동 배포 스크립트 - AI ON 프로젝트
# Render.com → Azure App Service 마이그레이션
#
# 사용법:
#   chmod +x azure-deploy.sh
#   ./azure-deploy.sh
#
# 필수 사항:
#   - Azure CLI 설치 (az --version)
#   - Azure 로그인 (az login)
#   - Docker 설치
###############################################################################

set -e  # 에러 발생 시 중단

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 제목 출력
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║   Azure 자동 배포 스크립트 - AI ON 프로젝트               ║"
echo "║   Render.com → Azure App Service 마이그레이션             ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

###############################################################################
# 1. 설정 변수
###############################################################################

log_info "설정 변수 초기화 중..."

# Azure 리소스 이름 (변경 가능)
RESOURCE_GROUP="aion-rg"
LOCATION="koreacentral"
POSTGRES_SERVER="aion-postgres"
POSTGRES_DB="aion_db"
POSTGRES_ADMIN="postgres"
ACR_NAME="aionregistry"
BACKEND_APP="aion-backend"
APP_SERVICE_PLAN="aion-plan"
STATIC_WEB_APP="aion-frontend"

# Docker 이미지
BACKEND_IMAGE="${ACR_NAME}.azurecr.io/aion-backend:latest"

# GitHub 정보
GITHUB_REPO="https://github.com/jeromwolf/gongjakso-tft"

log_success "설정 완료"

###############################################################################
# 2. 사전 확인
###############################################################################

log_info "Azure CLI 버전 확인 중..."
if ! command -v az &> /dev/null; then
    log_error "Azure CLI가 설치되어 있지 않습니다."
    log_info "설치 방법: https://docs.microsoft.com/cli/azure/install-azure-cli"
    exit 1
fi

az --version | head -n 1
log_success "Azure CLI 확인 완료"

log_info "Docker 확인 중..."
if ! command -v docker &> /dev/null; then
    log_error "Docker가 설치되어 있지 않습니다."
    exit 1
fi

docker --version
log_success "Docker 확인 완료"

log_info "Azure 로그인 확인 중..."
if ! az account show &> /dev/null; then
    log_warning "Azure에 로그인되어 있지 않습니다."
    log_info "로그인 시작..."
    az login
fi

ACCOUNT_NAME=$(az account show --query user.name -o tsv)
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
log_success "로그인 완료: $ACCOUNT_NAME"
log_info "구독 ID: $SUBSCRIPTION_ID"

###############################################################################
# 3. 민감 정보 입력 받기
###############################################################################

echo ""
log_info "민감 정보를 입력해주세요 (안전하게 저장됩니다)"
echo ""

# PostgreSQL 비밀번호
read -sp "PostgreSQL 관리자 비밀번호 (8자 이상, 대소문자+숫자+특수문자): " POSTGRES_PASSWORD
echo ""
if [ ${#POSTGRES_PASSWORD} -lt 8 ]; then
    log_error "비밀번호가 너무 짧습니다 (최소 8자)"
    exit 1
fi

# Secret Key
read -sp "JWT Secret Key (32자 이상, 랜덤 문자열): " SECRET_KEY
echo ""
if [ ${#SECRET_KEY} -lt 32 ]; then
    log_warning "Secret Key가 짧습니다. 랜덤 생성합니다..."
    SECRET_KEY=$(openssl rand -base64 48)
    log_info "생성된 Secret Key: $SECRET_KEY"
fi

# OpenAI API Key (선택)
read -p "OpenAI API Key (선택, Enter로 건너뛰기): " OPENAI_API_KEY

# Anthropic API Key (선택)
read -p "Anthropic API Key (선택, Enter로 건너뛰기): " ANTHROPIC_API_KEY

# Resend API Key (선택)
read -p "Resend API Key (선택, Enter로 건너뛰기): " RESEND_API_KEY

log_success "정보 입력 완료"

###############################################################################
# 4. 리소스 그룹 생성
###############################################################################

echo ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "Phase 1: 리소스 그룹 생성"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if az group show --name $RESOURCE_GROUP &> /dev/null; then
    log_warning "리소스 그룹 '$RESOURCE_GROUP'이 이미 존재합니다."
else
    log_info "리소스 그룹 생성 중: $RESOURCE_GROUP (위치: $LOCATION)"
    az group create \
        --name $RESOURCE_GROUP \
        --location $LOCATION \
        --output table
    log_success "리소스 그룹 생성 완료"
fi

###############################################################################
# 5. PostgreSQL Flexible Server 생성
###############################################################################

echo ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "Phase 2: PostgreSQL Flexible Server 생성"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if az postgres flexible-server show --resource-group $RESOURCE_GROUP --name $POSTGRES_SERVER &> /dev/null; then
    log_warning "PostgreSQL 서버 '$POSTGRES_SERVER'가 이미 존재합니다."
else
    log_info "PostgreSQL Flexible Server 생성 중 (약 5분 소요)..."
    az postgres flexible-server create \
        --resource-group $RESOURCE_GROUP \
        --name $POSTGRES_SERVER \
        --location $LOCATION \
        --admin-user $POSTGRES_ADMIN \
        --admin-password "$POSTGRES_PASSWORD" \
        --sku-name Standard_B1ms \
        --tier Burstable \
        --version 16 \
        --storage-size 32 \
        --public-access 0.0.0.0 \
        --output table

    log_success "PostgreSQL 서버 생성 완료"
fi

# Azure 서비스 접근 허용
log_info "방화벽 규칙 설정 중..."
az postgres flexible-server firewall-rule create \
    --resource-group $RESOURCE_GROUP \
    --name $POSTGRES_SERVER \
    --rule-name AllowAzureServices \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0 \
    --output table

log_success "방화벽 규칙 설정 완료"

# 데이터베이스 생성
log_info "데이터베이스 생성 중: $POSTGRES_DB"
az postgres flexible-server db create \
    --resource-group $RESOURCE_GROUP \
    --server-name $POSTGRES_SERVER \
    --database-name $POSTGRES_DB \
    --output table

log_success "데이터베이스 생성 완료"

# 연결 문자열 생성
POSTGRES_HOST="${POSTGRES_SERVER}.postgres.database.azure.com"
DATABASE_URL="postgresql+asyncpg://${POSTGRES_ADMIN}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}?ssl=require"

log_success "PostgreSQL 설정 완료"
log_info "호스트: $POSTGRES_HOST"

###############################################################################
# 6. Container Registry 생성
###############################################################################

echo ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "Phase 3: Azure Container Registry 생성"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if az acr show --resource-group $RESOURCE_GROUP --name $ACR_NAME &> /dev/null; then
    log_warning "Container Registry '$ACR_NAME'이 이미 존재합니다."
else
    log_info "Container Registry 생성 중..."
    az acr create \
        --resource-group $RESOURCE_GROUP \
        --name $ACR_NAME \
        --sku Basic \
        --location $LOCATION \
        --admin-enabled true \
        --output table

    log_success "Container Registry 생성 완료"
fi

# ACR 자격 증명 가져오기
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

log_success "Container Registry 설정 완료"
log_info "Registry: ${ACR_NAME}.azurecr.io"

###############################################################################
# 7. Backend Docker 이미지 빌드 및 푸시
###############################################################################

echo ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "Phase 4: Backend Docker 이미지 빌드 및 푸시"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ACR 로그인
log_info "Container Registry 로그인 중..."
echo "$ACR_PASSWORD" | docker login ${ACR_NAME}.azurecr.io -u $ACR_USERNAME --password-stdin

# 이미지 빌드
log_info "Backend Docker 이미지 빌드 중 (약 3분 소요)..."
cd backend
docker build -t $BACKEND_IMAGE .
cd ..

log_success "이미지 빌드 완료"

# 이미지 푸시
log_info "이미지를 Container Registry에 푸시 중..."
docker push $BACKEND_IMAGE

log_success "이미지 푸시 완료"

###############################################################################
# 8. App Service Plan 생성
###############################################################################

echo ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "Phase 5: App Service Plan 생성"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if az appservice plan show --resource-group $RESOURCE_GROUP --name $APP_SERVICE_PLAN &> /dev/null; then
    log_warning "App Service Plan '$APP_SERVICE_PLAN'이 이미 존재합니다."
else
    log_info "App Service Plan 생성 중..."
    az appservice plan create \
        --resource-group $RESOURCE_GROUP \
        --name $APP_SERVICE_PLAN \
        --location $LOCATION \
        --is-linux \
        --sku B1 \
        --output table

    log_success "App Service Plan 생성 완료"
fi

###############################################################################
# 9. Backend App Service 생성
###############################################################################

echo ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "Phase 6: Backend App Service 생성 및 배포"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if az webapp show --resource-group $RESOURCE_GROUP --name $BACKEND_APP &> /dev/null; then
    log_warning "App Service '$BACKEND_APP'이 이미 존재합니다."
else
    log_info "Backend App Service 생성 중..."
    az webapp create \
        --resource-group $RESOURCE_GROUP \
        --plan $APP_SERVICE_PLAN \
        --name $BACKEND_APP \
        --deployment-container-image-name $BACKEND_IMAGE \
        --output table

    log_success "Backend App Service 생성 완료"
fi

# ACR 연동
log_info "Container Registry 연동 중..."
az webapp config container set \
    --resource-group $RESOURCE_GROUP \
    --name $BACKEND_APP \
    --docker-custom-image-name $BACKEND_IMAGE \
    --docker-registry-server-url https://${ACR_NAME}.azurecr.io \
    --docker-registry-server-user $ACR_USERNAME \
    --docker-registry-server-password "$ACR_PASSWORD" \
    --output table

# 환경 변수 설정
log_info "환경 변수 설정 중..."

# Frontend URL (나중에 Static Web App 생성 후 업데이트 필요)
FRONTEND_URL="https://${STATIC_WEB_APP}.azurestaticapps.net"

az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $BACKEND_APP \
    --settings \
        DATABASE_URL="$DATABASE_URL" \
        SECRET_KEY="$SECRET_KEY" \
        DEBUG="false" \
        APP_NAME="AI ON API" \
        APP_VERSION="1.0.0" \
        FROM_EMAIL="noreply@aion.io.kr" \
        OPENAI_API_KEY="$OPENAI_API_KEY" \
        ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
        RESEND_API_KEY="$RESEND_API_KEY" \
    --output table

log_success "환경 변수 설정 완료"

# Always On 활성화 (콜드 스타트 방지)
log_info "Always On 활성화 중..."
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $BACKEND_APP \
    --always-on true \
    --output table

# 포트 설정
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $BACKEND_APP \
    --settings WEBSITES_PORT=8000 \
    --output table

log_success "Backend App Service 설정 완료"

BACKEND_URL="https://${BACKEND_APP}.azurewebsites.net"
log_info "Backend URL: $BACKEND_URL"

###############################################################################
# 10. Frontend Static Web App 생성 (GitHub 연동)
###############################################################################

echo ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "Phase 7: Frontend Static Web App 생성"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

log_warning "Static Web App은 GitHub 토큰이 필요합니다."
log_info "다음 중 하나를 선택하세요:"
echo "  1) GitHub Personal Access Token 입력 (자동 생성)"
echo "  2) Azure Portal에서 수동으로 생성 (건너뛰기)"
echo ""
read -p "선택 (1 또는 2): " SWA_CHOICE

if [ "$SWA_CHOICE" == "1" ]; then
    read -sp "GitHub Personal Access Token (repo 권한 필요): " GITHUB_TOKEN
    echo ""

    log_info "Static Web App 생성 중 (약 2분 소요)..."
    az staticwebapp create \
        --resource-group $RESOURCE_GROUP \
        --name $STATIC_WEB_APP \
        --location eastasia \
        --source $GITHUB_REPO \
        --branch main \
        --app-location "/frontend" \
        --output-location ".next" \
        --token "$GITHUB_TOKEN" \
        --output table

    log_success "Static Web App 생성 완료"

    # 환경 변수 설정
    log_info "Frontend 환경 변수 설정 중..."
    az staticwebapp appsettings set \
        --resource-group $RESOURCE_GROUP \
        --name $STATIC_WEB_APP \
        --setting-names \
            NEXT_PUBLIC_API_URL="$BACKEND_URL" \
            NODE_ENV="production" \
        --output table

    log_success "Frontend 설정 완료"
    log_info "Frontend URL: $FRONTEND_URL"
else
    log_warning "Static Web App 생성을 건너뜁니다."
    log_info "Azure Portal에서 수동으로 생성하세요:"
    log_info "  1. https://portal.azure.com"
    log_info "  2. Static Web Apps → + 만들기"
    log_info "  3. GitHub 리포지토리: jeromwolf/gongjakso-tft"
    log_info "  4. 앱 위치: /frontend"
    log_info "  5. 출력 위치: .next"
fi

###############################################################################
# 11. CORS 설정 업데이트
###############################################################################

echo ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "Phase 8: CORS 설정 업데이트"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

log_info "Backend에 Frontend URL 추가 중..."

# CORS_ORIGINS를 Backend 환경 변수에 추가
CORS_ORIGINS="[\"http://localhost:3000\",\"$FRONTEND_URL\",\"https://aion.io.kr\",\"https://www.aion.io.kr\"]"

az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $BACKEND_APP \
    --settings CORS_ORIGINS="$CORS_ORIGINS" \
    --output table

log_success "CORS 설정 완료"

###############################################################################
# 12. 배포 완료 및 테스트
###############################################################################

echo ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "배포 완료!"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

log_success "모든 리소스가 성공적으로 생성되었습니다!"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                    배포 정보                              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "📦 리소스 그룹: $RESOURCE_GROUP"
echo "🗄️  PostgreSQL:  $POSTGRES_HOST"
echo "🐳 Registry:    ${ACR_NAME}.azurecr.io"
echo "🔧 Backend:     $BACKEND_URL"
echo "🌐 Frontend:    $FRONTEND_URL"
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                    다음 단계                              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "1. Backend 헬스체크:"
echo "   curl $BACKEND_URL/api/health"
echo ""
echo "2. API 문서 확인:"
echo "   open $BACKEND_URL/api/docs"
echo ""
echo "3. 데이터 마이그레이션:"
echo "   cd backend"
echo "   python3 scripts/upload_to_production.py --api-url $BACKEND_URL"
echo ""
echo "4. Frontend 확인:"
echo "   open $FRONTEND_URL"
echo ""
echo "5. GitHub Actions 확인:"
echo "   https://github.com/jeromwolf/gongjakso-tft/actions"
echo ""

log_info "배포 로그를 저장합니다..."

# 배포 정보를 파일로 저장
cat > azure-deployment-info.txt <<EOF
Azure 배포 정보 - AI ON 프로젝트
배포 일시: $(date)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

리소스 그룹: $RESOURCE_GROUP
위치: $LOCATION

PostgreSQL:
  호스트: $POSTGRES_HOST
  데이터베이스: $POSTGRES_DB
  사용자: $POSTGRES_ADMIN
  비밀번호: ********

Container Registry:
  이름: $ACR_NAME
  URL: ${ACR_NAME}.azurecr.io
  사용자: $ACR_USERNAME
  비밀번호: ********

Backend App Service:
  이름: $BACKEND_APP
  URL: $BACKEND_URL
  이미지: $BACKEND_IMAGE

Frontend Static Web App:
  이름: $STATIC_WEB_APP
  URL: $FRONTEND_URL

환경 변수:
  DATABASE_URL: $DATABASE_URL
  SECRET_KEY: ********
  OPENAI_API_KEY: ${OPENAI_API_KEY:+설정됨}
  ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:+설정됨}
  RESEND_API_KEY: ${RESEND_API_KEY:+설정됨}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

다음 단계:
1. Backend 헬스체크: curl $BACKEND_URL/api/health
2. 데이터 마이그레이션: python3 backend/scripts/upload_to_production.py
3. DNS 설정: aion.io.kr → $FRONTEND_URL
4. SSL 인증서: Azure에서 자동 발급

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF

log_success "배포 정보가 'azure-deployment-info.txt'에 저장되었습니다."

echo ""
log_success "🎉 Azure 배포가 완료되었습니다!"
echo ""
