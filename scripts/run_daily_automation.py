#!/usr/bin/env python3
"""
Daily Automation Runner

Runs both blog and newsletter generation daily

Usage:
    # Run immediately (test mode)
    python scripts/run_daily_automation.py --now

    # Run on schedule (daily)
    python scripts/run_daily_automation.py

    # Custom schedule
    python scripts/run_daily_automation.py --blog-hour 9 --newsletter-hour 18
"""
import asyncio
import sys
import argparse
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.blog_scheduler import create_blog_scheduler
from services.newsletter_scheduler import create_newsletter_scheduler
from loguru import logger


# Default settings
DEFAULT_AUTHOR_ID = 1  # Admin user ID for blog posts
DEFAULT_BLOG_HOUR = 9  # 9 AM: Generate daily blog
DEFAULT_NEWSLETTER_HOUR = 18  # 6 PM: Send daily newsletter


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🤖 AI ON Daily Automation 🤖                    ║
║                                                              ║
║         Blog Generation + Newsletter Delivery                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


async def main_async():
    parser = argparse.ArgumentParser(
        description="AI ON Daily Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--now",
        action="store_true",
        help="Run all tasks immediately (for testing)"
    )
    parser.add_argument(
        "--author-id",
        type=int,
        default=DEFAULT_AUTHOR_ID,
        help=f"Blog author user ID (default: {DEFAULT_AUTHOR_ID})"
    )
    parser.add_argument(
        "--blog-hour",
        type=int,
        default=DEFAULT_BLOG_HOUR,
        help=f"Hour to generate blog (0-23, default: {DEFAULT_BLOG_HOUR} AM)"
    )
    parser.add_argument(
        "--newsletter-hour",
        type=int,
        default=DEFAULT_NEWSLETTER_HOUR,
        help=f"Hour to send newsletter (0-23, default: {DEFAULT_NEWSLETTER_HOUR} PM)"
    )
    parser.add_argument(
        "--auto-publish-blog",
        action="store_true",
        help="Auto-publish blog after generation (default: save as DRAFT)"
    )
    parser.add_argument(
        "--auto-send-newsletter",
        action="store_true",
        help="Auto-send newsletter after generation (default: save as DRAFT)"
    )

    args = parser.parse_args()

    print_banner()

    # Create schedulers
    blog_scheduler = create_blog_scheduler(
        author_id=args.author_id,
        auto_publish=args.auto_publish_blog
    )

    newsletter_scheduler = create_newsletter_scheduler(
        auto_send=args.auto_send_newsletter
    )

    if args.now:
        # Run immediately
        print("\n🚀 Starting daily automation (immediate mode)...\n")

        print("📝 Step 1: Generating blog post...")
        await blog_scheduler.run_now()

        print("\n📧 Step 2: Generating newsletter...")
        await newsletter_scheduler.run_now()

        print("\n✅ Daily automation completed!\n")
    else:
        # Run on schedule
        print(f"\n📅 Starting daily automation scheduler...\n")
        print(f"   📝 Blog Generation:")
        print(f"      - Time: {args.blog_hour:02d}:00 KST")
        print(f"      - Mode: {'AUTO-PUBLISH' if args.auto_publish_blog else 'DRAFT'}")
        print(f"\n   📧 Newsletter:")
        print(f"      - Time: {args.newsletter_hour:02d}:00 KST")
        print(f"      - Mode: {'AUTO-SEND' if args.auto_send_newsletter else 'DRAFT'}")
        print()

        # Start blog scheduler
        blog_scheduler.start(hour=args.blog_hour, minute=0)

        # Start newsletter scheduler
        newsletter_scheduler.start(
            day_of_week="*",  # Every day
            hour=args.newsletter_hour,
            minute=0
        )

        print("✅ Schedulers started successfully!\n")
        print("Press Ctrl+C to stop\n")

        # Keep running
        try:
            while True:
                await asyncio.sleep(60)
        except KeyboardInterrupt:
            print("\n\n👋 Schedulers stopped by user\n")


def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\n\n👋 Schedulers stopped by user\n")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
