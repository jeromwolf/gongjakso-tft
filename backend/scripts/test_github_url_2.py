"""
MP4 압축 도구에 GitHub URL #2 직접 추가 (테스트)
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

        # MP4 압축 도구에 GitHub URL #2 추가
        test_url = "https://github.com/ryhyh98/MP4Compress_Windows"

        print(f"📝 MP4 압축 도구에 GitHub URL #2 추가 중...")
        print(f"   URL: {test_url}\n")

        cursor.execute("""
            UPDATE projects
            SET github_url_2 = %s
            WHERE slug = 'mp4-compress';
        """, (test_url,))

        conn.commit()
        print("✅ 업데이트 완료!")

        # 확인
        print("\n📋 업데이트된 프로젝트 정보:")
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

        cursor.close()
        conn.close()

        print("\n🎉 테스트 완료! 이제 프론트엔드에서 확인하세요:")
        print("   https://gongjakso-tft-frontend.onrender.com/project/mp4-compress")

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        raise

if __name__ == "__main__":
    main()
