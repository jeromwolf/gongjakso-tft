#!/usr/bin/env python3
"""
Newsletter Viewer

View generated newsletters from database
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import AsyncSessionLocal
from models.newsletter import Newsletter
from sqlalchemy import select
from loguru import logger


async def view_newsletters(limit: int = 10):
    """View recent newsletters"""

    print("\n" + "="*70)
    print("📧 AI ON 뉴스레터 목록")
    print("="*70 + "\n")

    async with AsyncSessionLocal() as db:
        # Get recent newsletters
        stmt = (
            select(Newsletter)
            .order_by(Newsletter.created_at.desc())
            .limit(limit)
        )
        result = await db.execute(stmt)
        newsletters = result.scalars().all()

        if not newsletters:
            print("❌ 생성된 뉴스레터가 없습니다.\n")
            print("다음 명령으로 뉴스레터를 생성하세요:")
            print("  python scripts/run_newsletter_scheduler.py --now\n")
            return

        print(f"총 {len(newsletters)}개의 뉴스레터\n")

        for i, newsletter in enumerate(newsletters, 1):
            print(f"{'='*70}")
            print(f"[{i}] ID: {newsletter.id}")
            print(f"제목: {newsletter.title}")
            print(f"상태: {newsletter.status.value.upper()}")
            print(f"생성일: {newsletter.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

            if newsletter.sent_at:
                print(f"발송일: {newsletter.sent_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"수신자: {newsletter.recipient_count}명")
            else:
                print(f"발송: 미발송 (DRAFT)")

            if newsletter.summary:
                print(f"요약: {newsletter.summary}")

            print(f"{'='*70}\n")


async def view_newsletter_detail(newsletter_id: int):
    """View newsletter detail including content"""

    print("\n" + "="*70)
    print(f"📧 뉴스레터 상세 (ID: {newsletter_id})")
    print("="*70 + "\n")

    async with AsyncSessionLocal() as db:
        # Get newsletter by ID
        stmt = select(Newsletter).where(Newsletter.id == newsletter_id)
        result = await db.execute(stmt)
        newsletter = result.scalar_one_or_none()

        if not newsletter:
            print(f"❌ ID {newsletter_id}인 뉴스레터를 찾을 수 없습니다.\n")
            return

        print(f"제목: {newsletter.title}")
        print(f"상태: {newsletter.status.value.upper()}")
        print(f"생성일: {newsletter.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

        if newsletter.sent_at:
            print(f"발송일: {newsletter.sent_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"수신자: {newsletter.recipient_count}명")

        if newsletter.summary:
            print(f"\n요약:\n{newsletter.summary}")

        print(f"\n콘텐츠:\n")
        print("-"*70)
        # Print HTML content (could be converted to plain text)
        print(newsletter.content[:1000])  # First 1000 chars
        if len(newsletter.content) > 1000:
            print(f"\n... (총 {len(newsletter.content)}자)")
        print("-"*70)

        # Source info
        if newsletter.source_blog_ids:
            print(f"\n출처 블로그: {len(newsletter.source_blog_ids)}개")
        if newsletter.source_projects:
            print(f"출처 프로젝트: {len(newsletter.source_projects)}개")

        print()


async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="View generated newsletters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--id",
        type=int,
        help="Show detail for specific newsletter ID",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of newsletters to show (default: 10)",
    )

    args = parser.parse_args()

    try:
        if args.id:
            await view_newsletter_detail(args.id)
        else:
            await view_newsletters(args.limit)

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
