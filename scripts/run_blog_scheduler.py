#!/usr/bin/env python3
"""
Blog Scheduler Runner

Usage:
    # Run immediately (DRAFT mode)
    python scripts/run_blog_scheduler.py --now

    # Run immediately (auto-publish)
    python scripts/run_blog_scheduler.py --now --auto-publish

    # Run on schedule (daily at 9 AM)
    python scripts/run_blog_scheduler.py

    # Custom schedule
    python scripts/run_blog_scheduler.py --hour 14 --minute 0 --auto-publish
"""
import asyncio
import sys
import argparse
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.blog_scheduler import create_blog_scheduler
from loguru import logger


# Default author ID (should be admin user)
DEFAULT_AUTHOR_ID = 1  # Change this to your admin user ID


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              📝 AI ON Blog Scheduler 📝                      ║
║                                                              ║
║         Automated Daily Blog Generation                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


async def main_async():
    parser = argparse.ArgumentParser(
        description="AI ON Blog Scheduler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--now",
        action="store_true",
        help="Run blog generation immediately (for testing)"
    )
    parser.add_argument(
        "--auto-publish",
        action="store_true",
        help="Auto-publish blog after generation (default: save as DRAFT)"
    )
    parser.add_argument(
        "--author-id",
        type=int,
        default=DEFAULT_AUTHOR_ID,
        help=f"Blog author user ID (default: {DEFAULT_AUTHOR_ID})"
    )
    parser.add_argument(
        "--topic",
        type=str,
        help="Specific topic to write about (optional)"
    )
    parser.add_argument(
        "--hour",
        type=int,
        default=9,
        help="Hour to run scheduler (0-23, default: 9 AM)"
    )
    parser.add_argument(
        "--minute",
        type=int,
        default=0,
        help="Minute to run scheduler (0-59, default: 0)"
    )

    args = parser.parse_args()

    print_banner()

    # Create scheduler
    scheduler = create_blog_scheduler(
        author_id=args.author_id,
        auto_publish=args.auto_publish
    )

    if args.now:
        # Run immediately
        print("\n🚀 Starting blog generation...\n")
        await scheduler.run_now()
        print("\n✅ Blog generation completed!\n")
    else:
        # Run on schedule
        print(f"\n📅 Starting scheduler...")
        print(f"   - Daily at: {args.hour:02d}:{args.minute:02d} KST")
        print(f"   - Author ID: {args.author_id}")
        print(f"   - Mode: {'AUTO-PUBLISH' if args.auto_publish else 'DRAFT'}\n")

        scheduler.start(hour=args.hour, minute=args.minute)

        # Keep running
        try:
            while True:
                await asyncio.sleep(60)
        except KeyboardInterrupt:
            print("\n\n👋 Scheduler stopped by user\n")


def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler stopped by user\n")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
