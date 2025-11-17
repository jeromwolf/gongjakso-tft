#!/usr/bin/env python3
"""
Newsletter Scheduler Runner

Automated weekly newsletter generation

Usage:
    # Run scheduler (every Monday at 9 AM)
    python scripts/run_newsletter_scheduler.py

    # Run immediately (for testing)
    python scripts/run_newsletter_scheduler.py --now

    # Auto-send after generation
    python scripts/run_newsletter_scheduler.py --auto-send

    # Custom schedule (every Friday at 10:30 AM)
    python scripts/run_newsletter_scheduler.py --day fri --hour 10 --minute 30
"""
import argparse
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.newsletter_scheduler import create_newsletter_scheduler
from loguru import logger


def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              📧 AI ON Newsletter Scheduler 📧                ║
    ║                                                              ║
    ║         Automated Weekly Newsletter Generation              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


async def main_async():
    """Run scheduler (async)"""
    parser = argparse.ArgumentParser(
        description="AI ON Newsletter Scheduler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--now",
        action="store_true",
        help="Run immediately (skip scheduler)",
    )
    parser.add_argument(
        "--auto-send",
        action="store_true",
        help="Auto-send after generation (no manual review)",
    )
    parser.add_argument(
        "--day",
        type=str,
        default="mon",
        choices=["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
        help="Day of week to run (default: mon)",
    )
    parser.add_argument(
        "--hour",
        type=int,
        default=9,
        help="Hour to run (0-23, default: 9)",
    )
    parser.add_argument(
        "--minute",
        type=int,
        default=0,
        help="Minute to run (0-59, default: 0)",
    )

    args = parser.parse_args()

    try:
        print_banner()

        # Create scheduler
        scheduler = create_newsletter_scheduler(auto_send=args.auto_send)

        # Run immediately or schedule
        if args.now:
            logger.info("Running newsletter generation immediately...")
            print("\n🚀 Starting newsletter generation...\n")
            await scheduler.run_now()
            print("\n✅ Newsletter generation completed!\n")

        else:
            logger.info("Starting scheduler...")
            print(f"\n📅 Scheduler Configuration:")
            print(f"   Day: Every {args.day.upper()}")
            print(f"   Time: {args.hour:02d}:{args.minute:02d} KST")
            print(f"   Auto-send: {'Yes' if args.auto_send else 'No (DRAFT mode)'}")

            if not args.auto_send:
                print(f"\n⚠️  DRAFT mode: Newsletters will be saved for manual review")
                print(f"   Admin must manually send via API or dashboard")

            print(f"\n🕐 Next run: Every {args.day.upper()} at {args.hour:02d}:{args.minute:02d} KST")
            print(f"\n✨ Scheduler started! Press Ctrl+C to stop.\n")

            scheduler.start(
                day_of_week=args.day,
                hour=args.hour,
                minute=args.minute
            )

            # Keep running
            while True:
                await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n\n👋 Scheduler stopped by user")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Scheduler failed: {e}", exc_info=True)
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)


def main():
    """Entry point"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
