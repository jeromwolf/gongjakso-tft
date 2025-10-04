"""
프로덕션 데이터베이스에서 사용자를 admin으로 설정
"""
import asyncio
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from loguru import logger

# Render Production Database URL
# External URL from Render dashboard
DATABASE_URL = input("Render PostgreSQL External Database URL을 입력하세요: ").strip()

# Convert to sync URL (remove +asyncpg)
if '+asyncpg' in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace('+asyncpg', '')

ADMIN_EMAIL = "admin@example.com"


def set_admin_role():
    """Set user role to admin"""
    try:
        # Create sync engine
        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            # Check current role
            result = conn.execute(
                text("SELECT email, role FROM users WHERE email = :email"),
                {"email": ADMIN_EMAIL}
            )
            user = result.fetchone()

            if not user:
                logger.error(f"❌ User {ADMIN_EMAIL} not found")
                return False

            logger.info(f"현재 역할: {user[1]}")

            # Update to admin
            conn.execute(
                text("UPDATE users SET role = 'admin' WHERE email = :email"),
                {"email": ADMIN_EMAIL}
            )
            conn.commit()

            logger.success(f"✅ {ADMIN_EMAIL} 역할을 'admin'으로 변경했습니다!")
            return True

    except Exception as e:
        logger.error(f"❌ 에러 발생: {e}")
        return False


if __name__ == "__main__":
    if set_admin_role():
        print("\n이제 upload_to_production.py를 다시 실행하세요!")
        print("python3 backend/scripts/upload_to_production.py")
