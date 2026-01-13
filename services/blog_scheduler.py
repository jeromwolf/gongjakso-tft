"""
Blog Scheduler

Automated daily blog generation
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from loguru import logger

from core.database import AsyncSessionLocal
from services.blog_generator import generate_daily_blog


class BlogScheduler:
    """Automated blog scheduler"""

    def __init__(self, author_id: int, auto_publish: bool = False):
        """
        Initialize scheduler

        Args:
            author_id: Admin user ID (blog author)
            auto_publish: If True, automatically publish after generation
                         If False, save as DRAFT for manual review
        """
        self.scheduler = AsyncIOScheduler(timezone="Asia/Seoul")
        self.author_id = author_id
        self.auto_publish = auto_publish
        logger.info(f"BlogScheduler initialized (author_id={author_id}, auto_publish={auto_publish})")

    async def run_blog_generation(self):
        """Generate blog (scheduled job)"""
        logger.info("=" * 70)
        logger.info("Starting scheduled blog generation")
        logger.info(f"Time: {datetime.now()}")
        logger.info(f"Auto-publish: {self.auto_publish}")
        logger.info("=" * 70)

        try:
            async with AsyncSessionLocal() as db:
                blog = await generate_daily_blog(
                    db=db,
                    author_id=self.author_id,
                    auto_publish=self.auto_publish,
                )

                if self.auto_publish:
                    logger.info(
                        f"✅ Blog generated and published: {blog.title} "
                        f"(ID: {blog.id}, Slug: {blog.slug})"
                    )
                else:
                    logger.info(
                        f"✅ Blog generated as DRAFT: {blog.title} "
                        f"(ID: {blog.id}, Slug: {blog.slug})"
                    )

        except Exception as e:
            logger.error(f"❌ Blog generation failed: {e}", exc_info=True)

        logger.info("=" * 70)

    def start(
        self,
        hour: int = 9,
        minute: int = 0
    ):
        """
        Start scheduler

        Args:
            hour: Hour to run (0-23, default 9 AM)
            minute: Minute to run (0-59, default 0)
        """
        # Add daily job
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
            timezone="Asia/Seoul"
        )

        self.scheduler.add_job(
            self.run_blog_generation,
            trigger=trigger,
            id="daily_blog",
            name="Daily Blog Generation",
            replace_existing=True,
        )

        logger.info(
            f"Scheduler started - will run daily at {hour:02d}:{minute:02d} KST"
        )

        # Print next run time
        job = self.scheduler.get_job("daily_blog")
        if job and job.next_run_time:
            logger.info(f"Next run: {job.next_run_time}")

        # Start scheduler
        self.scheduler.start()

    async def run_now(self):
        """Run blog generation immediately (for testing)"""
        logger.info("Running blog generation immediately (manual trigger)")
        await self.run_blog_generation()


def create_blog_scheduler(author_id: int, auto_publish: bool = False) -> BlogScheduler:
    """
    Create blog scheduler

    Args:
        author_id: Admin user ID (blog author)
        auto_publish: If True, automatically publish after generation

    Returns:
        BlogScheduler instance

    Example:
        >>> scheduler = create_blog_scheduler(author_id=1, auto_publish=True)
        >>> scheduler.start()  # Run daily at 9 AM
        >>>
        >>> # Or run immediately for testing
        >>> await scheduler.run_now()
    """
    return BlogScheduler(author_id=author_id, auto_publish=auto_publish)
