"""
MP4 압축 도구 프로젝트의 GitHub URL 정보 확인
"""
import psycopg2

# Render PostgreSQL 연결 정보
DATABASE_URL = "postgresql://gongjakso_tft_db_user:MesPXkHwYedGakacqgMMUojrtde1GdXB@dpg-d3g8n095pdvs73e9rg9g-a.singapore-postgres.render.com/gongjakso_tft_db"

def main():
    print("🔌 Render PostgreSQL에 연결 중...")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        print("✅ 연결 성공!\n")

        # MP4 압축 도구 프로젝트 확인
        print("📋 MP4 압축 도구 프로젝트 정보:")
        cursor.execute("""
            SELECT id, name, slug, github_url, github_url_2
            FROM projects
            WHERE slug = 'mp4-compress';
        """)
        project = cursor.fetchone()

        if project:
            print(f"   ID: {project[0]}")
            print(f"   Name: {project[1]}")
            print(f"   Slug: {project[2]}")
            print(f"   GitHub URL: {project[3]}")
            print(f"   GitHub URL #2: {project[4]}")
        else:
            print("   ❌ MP4 압축 도구 프로젝트를 찾을 수 없습니다.")

        # 모든 프로젝트의 github_url_2 상태 확인
        print("\n📊 모든 프로젝트의 GitHub URL #2 상태:")
        cursor.execute("""
            SELECT name, slug,
                   CASE WHEN github_url_2 IS NULL THEN '❌ NULL'
                        WHEN github_url_2 = '' THEN '⚠️  Empty'
                        ELSE '✅ ' || github_url_2 END as url2_status
            FROM projects
            ORDER BY id;
        """)
        projects = cursor.fetchall()

        for project in projects:
            print(f"   {project[0]}: {project[2]}")

        cursor.close()
        conn.close()

        print("\n✅ 조회 완료!")

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        raise

if __name__ == "__main__":
    main()
