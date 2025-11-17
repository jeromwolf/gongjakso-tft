# 하이브리드 구성: Azure PostgreSQL + Render 배포

## 🎯 아키텍처

**최적화된 하이브리드 구성**:
- 🗄️ **Database**: Azure PostgreSQL Flexible Server (유료, 안정적)
- 🔧 **Backend**: Render.com (무료/저렴, Docker)
- 🌐 **Frontend**: Render.com Static Site (무료)

### 장점
- ✅ 비용 효율적 (Render 무료 플랜 활용)
- ✅ 안정적인 DB (Azure 관리형)
- ✅ 배포 간단 (Render 자동 배포)
- ✅ 확장 가능 (필요시 Render도 유료 플랜으로)

---

## 📋 현재 Azure 리소스

### PostgreSQL Flexible Server
- **이름**: `aion-postgres`
- **호스트**: `aion-postgres.postgres.database.azure.com`
- **포트**: `5432`
- **데이터베이스**: `aion_db`
- **사용자**: `postgres`
- **비밀번호**: `AionDb2025!Secure@1`
- **버전**: PostgreSQL 16
- **SKU**: Standard_B1ms (약 $12/월)

### 연결 문자열
```
postgresql+asyncpg://postgres:AionDb2025!Secure@1@aion-postgres.postgres.database.azure.com:5432/aion_db?ssl=require
```

---

## 🔧 Render 설정 방법

### 1. Render Dashboard 접속

https://dashboard.render.com → 기존 Backend 서비스 선택

### 2. 환경 변수 업데이트

**Environment → Environment Variables**

기존 `DATABASE_URL` 값을 Azure PostgreSQL로 변경:

```
DATABASE_URL=postgresql+asyncpg://postgres:AionDb2025!Secure@1@aion-postgres.postgres.database.azure.com:5432/aion_db?ssl=require
```

**주의사항**:
- ⚠️ `ssl=require` 파라미터 필수! (Azure SSL 강제)
- ⚠️ 비밀번호에 특수문자 있어도 URL 인코딩 불필요 (asyncpg가 처리)

### 3. 저장 및 재배포

- "Save Changes" 클릭
- 자동으로 재배포 시작 (약 2-3분 소요)

### 4. 배포 완료 대기

**Logs** 탭에서 진행 상황 확인:
```
==> Building...
==> Deploying...
==> Your service is live 🎉
```

---

## ✅ 연결 테스트

### 1. Backend Health Check

배포 완료 후:
```bash
curl https://gongjakso-tft.onrender.com/api/health
```

**예상 응답**:
```json
{
  "status": "healthy",
  "message": "All systems operational",
  "database": "connected"
}
```

### 2. Database 연결 확인

API Docs에서 테스트:
```
https://gongjakso-tft.onrender.com/api/docs
```

### 3. 블로그 목록 확인

```bash
curl https://gongjakso-tft.onrender.com/api/blog
```

---

## 🗄️ 데이터 마이그레이션

### 옵션 A: 스크립트 실행 (권장)

```bash
cd backend

# 환경 변수 설정
export DATABASE_URL="postgresql+asyncpg://postgres:AionDb2025!Secure@1@aion-postgres.postgres.database.azure.com:5432/aion_db?ssl=require"

# Python 가상환경
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 데이터 업로드
python3 scripts/upload_to_production.py \
  --api-url https://gongjakso-tft.onrender.com
```

**스크립트 동작**:
1. Admin 계정 생성 (`admin@example.com` / `admin123`)
2. 블로그 6개 업로드
3. 프로젝트 12개 업로드

### 옵션 B: Azure Cloud Shell에서 직접 연결

```bash
# PostgreSQL 접속
psql "host=aion-postgres.postgres.database.azure.com port=5432 dbname=aion_db user=postgres password=AionDb2025!Secure@1 sslmode=require"

# 테이블 확인
\dt

# 데이터 확인
SELECT * FROM users;
SELECT COUNT(*) FROM blogs;
SELECT COUNT(*) FROM projects;
```

---

## 🔒 보안 설정

### Azure PostgreSQL 방화벽

현재 설정: **모든 IP 허용** (0.0.0.0-255.255.255.255)

**권장**: Render IP만 허용

1. Render Backend의 Outbound IP 확인:
   - Dashboard → Service → Settings → Outbound IPs

2. Azure Portal → PostgreSQL → Networking → Firewall rules
   - Render IP 추가
   - "Allow All" 규칙 삭제

### 환경 변수 보안

Render 환경 변수는 암호화되어 저장됨:
- ✅ 대시보드에서 마스킹 처리
- ✅ 로그에 노출되지 않음
- ✅ API로 조회 불가

---

## 💰 예상 비용

### 월간 비용 (USD)

| 항목 | 서비스 | 플랜 | 비용 |
|------|--------|------|------|
| Database | Azure PostgreSQL | B1ms | ~$12 |
| Backend | Render.com | Free | $0 |
| Frontend | Render.com | Free | $0 |
| **총계** | | | **~$12/월** |

### Azure 무료 크레딧 활용

- 무료 크레딧 $200 있으면 → 약 16개월 무료!
- 크레딧 소진 후 → $12/월만 지불

### Render 무료 플랜 제한

- ⚠️ 15분 미사용 시 슬립 모드
- ⚠️ 첫 요청 시 웜업 시간 (30초~1분)
- ✅ 트래픽 제한 없음
- ✅ 자동 SSL 인증서

**해결책**: Render 유료 플랜 ($7/월) 또는 핑 서비스 사용

---

## 🔧 트러블슈팅

### 1. "Connection refused" 에러

**원인**: Azure 방화벽에서 Render IP 차단

**해결**:
```bash
# Azure에서 Render IP 허용
az postgres flexible-server firewall-rule create \
  --resource-group aion-rg \
  --name aion-postgres \
  --rule-name AllowRender \
  --start-ip-address <Render-IP> \
  --end-ip-address <Render-IP>
```

### 2. "SSL required" 에러

**원인**: 연결 문자열에 `sslmode=require` 누락

**해결**:
```
DATABASE_URL=...?ssl=require  ✅
DATABASE_URL=...?sslmode=require  ✅
```

### 3. "Password authentication failed"

**원인**: 비밀번호 오타 또는 특수문자 문제

**해결**:
- 비밀번호 재확인: `AionDb2025!Secure@1`
- URL에서 직접 입력 (인코딩 불필요)

### 4. Render 배포 실패

**원인**: 환경 변수 잘못 설정

**해결**:
1. Render Dashboard → Environment
2. DATABASE_URL 값 다시 확인
3. "Save Changes" 후 재배포

---

## 📊 모니터링

### Render 모니터링

**Dashboard → Metrics**:
- CPU 사용량
- 메모리 사용량
- 응답 시간
- 에러 로그

**Logs**:
- 실시간 로그 스트림
- 에러 트래킹
- 배포 히스토리

### Azure PostgreSQL 모니터링

**Azure Portal → PostgreSQL → Monitoring**:
- CPU %
- 메모리 %
- Storage %
- 연결 수
- 쿼리 성능

---

## 🚀 추가 최적화

### 1. 연결 풀링

현재 설정 (이미 최적화됨):
```python
# backend/core/database.py
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,        # 기본 10개 연결
    max_overflow=20      # 최대 30개까지 확장
)
```

### 2. 백업 자동화

Azure PostgreSQL:
- 자동 백업: 매일 (기본 활성화)
- 보관 기간: 7일
- 복구: Azure Portal에서 1-클릭

### 3. 성능 튜닝

**인덱스 최적화**:
```sql
-- 이미 구현됨 (models/*)
- blogs: idx_blog_status_created
- projects: idx_project_status_created
```

---

## 📝 체크리스트

배포 전:
- [ ] Azure PostgreSQL 정상 작동 확인
- [ ] 연결 문자열 복사
- [ ] Render 환경 변수 업데이트

배포 후:
- [ ] Backend Health Check 통과
- [ ] API Docs 접근 가능
- [ ] 데이터 마이그레이션 완료
- [ ] Admin 로그인 테스트
- [ ] 방화벽 규칙 최적화 (선택)

---

## 🎯 다음 단계

1. **지금 바로**: Render 환경 변수 업데이트
2. **5분 후**: Health Check 확인
3. **10분 후**: 데이터 마이그레이션
4. **완료!**: 하이브리드 구성 완성

---

## 📚 참고 링크

- **Render Dashboard**: https://dashboard.render.com
- **Azure Portal**: https://portal.azure.com
- **Backend API Docs**: https://gongjakso-tft.onrender.com/api/docs

---

**작성일**: 2025-11-17
**구성**: Azure PostgreSQL + Render Backend/Frontend

**질문이나 문제가 있으면 언제든지 말씀해주세요!** 🚀
