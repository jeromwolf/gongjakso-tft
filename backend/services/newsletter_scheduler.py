"""
Newsletter Scheduler

Automated weekly newsletter generation and sending
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from loguru import logger

from core.database import get_async_session
from services.newsletter_generator import generate_weekly_newsletter


class NewsletterScheduler:
    """Automated newsletter scheduler"""

    def __init__(self, auto_send: bool = False):
        """
        Initialize scheduler

        Args:
            auto_send: If True, automatically send after generation
                      If False, save as DRAFT for manual review
        """
        self.scheduler = AsyncIOScheduler(timezone="Asia/Seoul")
        self.auto_send = auto_send
        logger.info(f"NewsletterScheduler initialized (auto_send={auto_send})")

    async def run_newsletter_generation(self):
        """Generate newsletter (scheduled job)"""
        logger.info("=" * 70)
        logger.info("Starting scheduled newsletter generation")
        logger.info(f"Time: {datetime.now()}")
        logger.info(f"Auto-send: {self.auto_send}")
        logger.info("=" * 70)

        try:
            async for db in get_async_session():
                newsletter = await generate_weekly_newsletter(
                    db=db,
                    auto_send=self.auto_send,
                )

                if self.auto_send:
                    logger.info(
                        f"✅ Newsletter generated and sent: {newsletter.title} "
                        f"(ID: {newsletter.id}, Recipients: {newsletter.recipient_count})"
                    )
                else:
                    logger.info(
                        f"✅ Newsletter generated as DRAFT: {newsletter.title} "
                        f"(ID: {newsletter.id})"
                    )
                break  # Exit after first successful generation

        except Exception as e:
            logger.error(f"❌ Newsletter generation failed: {e}", exc_info=True)

        logger.info("=" * 70)

    def start(
        self,
        day_of_week: str = "mon",  # mon, tue, wed, thu, fri, sat, sun
        hour: int = 9,
        minute: int = 0
    ):
        """
        Start scheduler

        Args:
            day_of_week: Day to run (mon, tue, wed, thu, fri, sat, sun)
            hour: Hour to run (0-23)
            minute: Minute to run (0-59)
        """
        # Add weekly job
        trigger = CronTrigger(
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            timezone="Asia/Seoul"
        )

        self.scheduler.add_job(
            self.run_newsletter_generation,
            trigger=trigger,
            id="weekly_newsletter",
            name="Weekly Newsletter Generation",
            replace_existing=True,
        )

        logger.info(
            f"Scheduler started - will run every {day_of_week.upper()} at "
            f"{hour:02d}:{minute:02d} KST"
        )

        # Print next run time
        job = self.scheduler.get_job("weekly_newsletter")
        if job and job.next_run_time:
            logger.info(f"Next run: {job.next_run_time}")

        # Start scheduler
        self.scheduler.start()

    async def run_now(self):
        """Run newsletter generation immediately (for testing)"""
        logger.info("Running newsletter generation immediately (manual trigger)")
        await self.run_newsletter_generation()


def create_newsletter_scheduler(auto_send: bool = False) -> NewsletterScheduler:
    """
    Create newsletter scheduler

    Args:
        auto_send: If True, automatically send after generation

    Returns:
        NewsletterScheduler instance

    Example:
        >>> scheduler = create_newsletter_scheduler(auto_send=True)
        >>> scheduler.start()  # Run every Monday at 9 AM
        >>>
        >>> # Or run immediately for testing
        >>> await scheduler.run_now()
    """
    return NewsletterScheduler(auto_send=auto_send)
