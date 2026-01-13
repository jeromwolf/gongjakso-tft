#!/bin/bash

###############################################################################
# GitHub Secrets 설정 스크립트
# GitHub CLI (gh) 필요
#
# 사용법:
#   chmod +x azure-setup-secrets.sh
#   ./azure-setup-secrets.sh
###############################################################################

set -e

# 색상 코드
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║   GitHub Secrets 자동 설정 스크립트                       ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# GitHub CLI 확인
if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}GitHub CLI (gh)가 설치되어 있지 않습니다.${NC}"
    echo "설치 방법:"
    echo "  macOS: brew install gh"
    echo "  Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
    exit 1
fi

# GitHub 로그인 확인
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}GitHub에 로그인되어 있지 않습니다.${NC}"
    gh auth login
fi

echo -e "${BLUE}GitHub 로그인 확인 완료${NC}"

# Azure 리소스 이름
ACR_NAME="aionregistry"
RESOURCE_GROUP="aion-rg"
BACKEND_APP="aion-backend"

echo ""
echo -e "${BLUE}Azure Container Registry 자격 증명 가져오는 중...${NC}"

# ACR 자격 증명
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

echo -e "${GREEN}ACR 자격 증명 확인 완료${NC}"

echo ""
echo -e "${BLUE}Azure 서비스 주체 생성 중...${NC}"

# Service Principal 생성
AZURE_CREDENTIALS=$(az ad sp create-for-rbac \
  --name "aion-github-actions" \
  --role contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP \
  --sdk-auth)

echo -e "${GREEN}서비스 주체 생성 완료${NC}"

echo ""
echo -e "${BLUE}GitHub Secrets 설정 중...${NC}"

# GitHub Repository 확인
REPO="jeromwolf/gongjakso-tft"

# Secrets 설정
gh secret set ACR_USERNAME --body "$ACR_USERNAME" --repo $REPO
gh secret set ACR_PASSWORD --body "$ACR_PASSWORD" --repo $REPO
gh secret set AZURE_CREDENTIALS --body "$AZURE_CREDENTIALS" --repo $REPO

echo -e "${GREEN}✅ GitHub Secrets 설정 완료!${NC}"

echo ""
echo "설정된 Secrets:"
echo "  - ACR_USERNAME"
echo "  - ACR_PASSWORD"
echo "  - AZURE_CREDENTIALS"
echo ""
echo -e "${GREEN}이제 GitHub Actions가 자동으로 배포할 수 있습니다!${NC}"
