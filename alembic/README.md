# Alembic 마이그레이션 가이드

## 개요

Alembic은 SQLAlchemy를 위한 데이터베이스 마이그레이션 도구입니다.

## 마이그레이션 생성

### 자동 생성 (권장)

모델 변경 사항을 자동으로 감지하여 마이그레이션 생성:

```bash
cd backend
alembic revision --autogenerate -m "마이그레이션 메시지"
```

### 수동 생성

빈 마이그레이션 파일 생성:

```bash
cd backend
alembic revision -m "마이그레이션 메시지"
```

## 마이그레이션 실행

### 최신 버전으로 업그레이드

```bash
cd backend
alembic upgrade head
```

### 특정 버전으로 업그레이드/다운그레이드

```bash
alembic upgrade <revision_id>
alembic downgrade <revision_id>
```

### 한 단계 되돌리기

```bash
alembic downgrade -1
```

## 마이그레이션 히스토리 확인

```bash
# 현재 버전 확인
alembic current

# 마이그레이션 히스토리 확인
alembic history

# 상세 히스토리
alembic history --verbose
```

## 초기 마이그레이션 생성 (프로젝트 시작 시)

1. 모든 모델이 정의되어 있는지 확인
2. 초기 마이그레이션 생성:

```bash
cd backend
alembic revision --autogenerate -m "Initial migration"
```

3. 생성된 마이그레이션 파일 확인 (`alembic/versions/`)
4. 마이그레이션 실행:

```bash
alembic upgrade head
```

## 환경 변수

Alembic은 `core/config.py`의 `DATABASE_URL`을 사용합니다.

```bash
# .env 파일에 설정
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
```

## 주의사항

1. **프로덕션 배포 전**: 반드시 로컬에서 마이그레이션을 테스트하세요
2. **다운그레이드**: 프로덕션에서는 신중하게 사용하세요
3. **자동 생성 확인**: `--autogenerate`로 생성된 마이그레이션은 반드시 검토하세요
4. **백업**: 프로덕션 DB 마이그레이션 전 백업 필수

## Railway 배포 시 마이그레이션

Railway에서는 배포 시 자동으로 마이그레이션을 실행하려면 `Procfile` 또는 start 스크립트에 추가:

```bash
# 예시: start.sh
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 문제 해결

### "target database is not up to date" 에러

```bash
# 현재 버전 확인
alembic current

# 강제로 특정 버전으로 설정 (주의!)
alembic stamp head
```

### "can't locate revision" 에러

마이그레이션 파일이 없거나 순서가 꼬인 경우. `alembic/versions/` 디렉토리 확인.

## 참고 자료

- Alembic 공식 문서: https://alembic.sqlalchemy.org/
- SQLAlchemy 문서: https://docs.sqlalchemy.org/
