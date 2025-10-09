"""
프로덕션 DB에 github_url_2 컬럼 추가
"""
import psycopg2

# Render PostgreSQL 연결 정보
DATABASE_URL = "postgresql://gongjakso_tft_db_user:MesPXkHwYedGakacqgMMUojrtde1GdXB@dpg-d3g8n095pdvs73e9rg9g-a.singapore-postgres.render.com/gongjakso_tft_db"

def main():
    print("🔌 Render PostgreSQL에 연결 중...")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        print("✅ 연결 성공!")

        # 프로젝트 개수 확인
        print("\n📊 현재 프로젝트 개수 확인...")
        cursor.execute("SELECT COUNT(*) FROM projects;")
        count = cursor.fetchone()[0]
        print(f"   프로젝트: {count}개")

        # 기존 컬럼 확인
        print("\n🔍 기존 컬럼 구조 확인...")
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'projects'
            ORDER BY ordinal_position;
        """)
        columns = [row[0] for row in cursor.fetchall()]
        print(f"   컬럼: {', '.join(columns)}")

        # github_url_2 컬럼 추가
        if 'github_url_2' in columns:
            print("\n⚠️  github_url_2 컬럼이 이미 존재합니다.")
        else:
            print("\n🔧 github_url_2 컬럼 추가 중...")
            cursor.execute("""
                ALTER TABLE projects
                ADD COLUMN github_url_2 VARCHAR(500) NULL;
            """)
            conn.commit()
            print("✅ 컬럼 추가 완료!")

        # 추가 후 컬럼 확인
        print("\n🔍 업데이트된 컬럼 구조:")
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'projects'
            ORDER BY ordinal_position;
        """)
        columns = [row[0] for row in cursor.fetchall()]
        print(f"   컬럼: {', '.join(columns)}")

        # 프로젝트 샘플 확인
        print("\n📋 프로젝트 샘플 (처음 3개):")
        cursor.execute("""
            SELECT id, name, github_url, github_url_2
            FROM projects
            LIMIT 3;
        """)
        projects = cursor.fetchall()
        for project in projects:
            print(f"   ID: {project[0]}, Name: {project[1]}")
            print(f"      GitHub: {project[2]}")
            print(f"      GitHub #2: {project[3]}")

        cursor.close()
        conn.close()

        print("\n🎉 마이그레이션 완료!")

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        raise

if __name__ == "__main__":
    main()
