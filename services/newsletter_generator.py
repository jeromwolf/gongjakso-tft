"""
AI Newsletter Generator

Automatically creates newsletter content from:
- Recent blog posts
- Project updates (GitHub API)
- IT news
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from models.blog import Blog
from models.project import Project
from models.newsletter import Newsletter, NewsletterStatus
from core.config import settings
from loguru import logger
import openai


class NewsletterContent:
    """Newsletter content container"""
    def __init__(
        self,
        title: str,
        summary: str,
        html_content: str,
        period_start: datetime,
        period_end: datetime,
        source_blog_ids: List[int],
        source_projects: List[Dict],
    ):
        self.title = title
        self.summary = summary
        self.html_content = html_content
        self.period_start = period_start
        self.period_end = period_end
        self.source_blog_ids = source_blog_ids
        self.source_projects = source_projects


class NewsletterGenerator:
    """AI-powered newsletter generator"""

    def __init__(self, db: AsyncSession):
        self.db = db
        # Set OpenAI API key
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured")
        openai.api_key = settings.OPENAI_API_KEY

    async def collect_weekly_content(
        self,
        days: int = 7
    ) -> Dict:
        """
        Collect content from the past N days

        Returns:
            dict: {
                'blogs': List[Blog],
                'projects': List[Project],
                'period_start': datetime,
                'period_end': datetime
            }
        """
        now = datetime.now(timezone.utc)
        period_start = now - timedelta(days=days)
        period_end = now

        logger.info(f"Collecting content from {period_start} to {period_end}")

        # 1. Recent blogs
        blog_stmt = (
            select(Blog)
            .where(
                and_(
                    Blog.created_at >= period_start,
                    Blog.created_at <= period_end
                )
            )
            .order_by(Blog.created_at.desc())
        )
        blog_result = await self.db.execute(blog_stmt)
        blogs = list(blog_result.scalars().all())

        # 2. Active projects (for GitHub updates)
        project_stmt = select(Project).where(
            Project.github_url.isnot(None)
        )
        project_result = await self.db.execute(project_stmt)
        projects = list(project_result.scalars().all())

        logger.info(f"Collected: {len(blogs)} blogs, {len(projects)} projects")

        return {
            'blogs': blogs,
            'projects': projects,
            'period_start': period_start,
            'period_end': period_end,
        }

    async def generate_newsletter(
        self,
        content_data: Dict,
        style: str = "friendly_technical"
    ) -> NewsletterContent:
        """
        Generate newsletter using AI

        Args:
            content_data: Content collected from collect_weekly_content()
            style: Writing style (friendly_technical, professional, casual)

        Returns:
            NewsletterContent with HTML
        """
        blogs = content_data['blogs']
        projects = content_data['projects']
        period_start = content_data['period_start']
        period_end = content_data['period_end']

        # Prepare content summary for AI
        blog_summaries = [
            f"- {blog.title}: {blog.excerpt or blog.content[:200]}"
            for blog in blogs
        ]

        project_summaries = [
            f"- {proj.name}: {proj.description}"
            for proj in projects[:5]  # Top 5 projects only
        ]

        # AI Prompt
        prompt = f"""
당신은 'AI ON'의 주간 뉴스레터를 작성하는 전문 작가입니다.

# 목표
지난 주 AI ON에서 발행한 콘텐츠를 정리하여 구독자에게 유익하고 흥미로운 뉴스레터를 작성하세요.

# 콘텐츠 기간
{period_start.strftime('%Y-%m-%d')} ~ {period_end.strftime('%Y-%m-%d')}

# 이번 주 블로그 포스트
{chr(10).join(blog_summaries) if blog_summaries else "이번 주 새로운 블로그 포스트가 없습니다."}

# 프로젝트 (최근 활동 중인 프로젝트)
{chr(10).join(project_summaries) if project_summaries else "프로젝트 정보가 없습니다."}

# 작성 가이드라인
1. **제목**: 매력적이고 클릭하고 싶은 제목 (예: "🚀 이번 주 AI ON: FastAPI 성능 최적화 & Next.js 15 신기능")
2. **요약** (50자 이내): 이번 주 핵심 내용 한 줄 요약
3. **본문 구조**:
   - 인사말 (간단하게, 2-3줄)
   - 이번 주 하이라이트 (핵심 내용 요약, 3-4줄)
   - 블로그 포스트 소개 (각 포스트마다 3-4줄 설명)
   - 프로젝트 소개 (간단히 1-2개 프로젝트 언급)
   - 마무리 인사 (다음 주 예고, 피드백 요청 등)
4. **톤**: 친근하지만 전문적, 개발자들이 좋아할 만한 내용
5. **길이**: 읽는 데 3-5분 정도 (800-1200자)

# 출력 형식
JSON 형식으로 출력하세요:
{{
  "title": "뉴스레터 제목",
  "summary": "한 줄 요약 (50자 이내)",
  "html_content": "HTML 형식의 본문"
}}

HTML 작성 시 주의사항:
- 이메일 클라이언트 호환성을 위해 간단한 HTML만 사용
- 제목: <h2>, <h3> 태그 사용
- 단락: <p> 태그 사용
- 강조: <strong>, <em> 태그 사용
- 링크: <a href="https://aion.io.kr/blogs/slug">텍스트</a> 형식
- 리스트: <ul>, <ol>, <li> 사용 가능
- 인라인 스타일 사용 금지 (CSS는 템플릿에서 처리)
"""

        # Call OpenAI GPT-4
        logger.info("Generating newsletter with GPT-4...")

        import json
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{
                "role": "system",
                "content": "당신은 AI ON의 주간 뉴스레터를 작성하는 전문 작가입니다. 친근하지만 전문적인 톤으로 개발자들이 좋아할 만한 콘텐츠를 작성합니다."
            }, {
                "role": "user",
                "content": prompt
            }],
            max_tokens=4000,
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        # Parse response
        ai_response = response.choices[0].message.content

        # Extract JSON from markdown code blocks if present
        if "```json" in ai_response:
            ai_response = ai_response.split("```json")[1].split("```")[0].strip()
        elif "```" in ai_response:
            ai_response = ai_response.split("```")[1].split("```")[0].strip()

        result = json.loads(ai_response)

        logger.info(f"Newsletter generated: {result['title']}")

        return NewsletterContent(
            title=result['title'],
            summary=result['summary'],
            html_content=result['html_content'],
            period_start=period_start,
            period_end=period_end,
            source_blog_ids=[blog.id for blog in blogs],
            source_projects=[{
                'id': proj.id,
                'name': proj.name,
                'github_url': proj.github_url
            } for proj in projects],
        )

    async def create_draft_newsletter(
        self,
        content: NewsletterContent,
        created_by_id: Optional[int] = None
    ) -> Newsletter:
        """
        Save generated newsletter as DRAFT

        Args:
            content: Generated newsletter content
            created_by_id: Admin user ID (optional)

        Returns:
            Newsletter model instance
        """
        newsletter = Newsletter(
            title=content.title,
            summary=content.summary,
            content=content.html_content,
            status=NewsletterStatus.DRAFT,
            period_start=content.period_start,
            period_end=content.period_end,
            source_blog_ids=content.source_blog_ids,
            source_projects=content.source_projects,
            is_auto_generated=True,
            created_by=created_by_id,
        )

        self.db.add(newsletter)
        await self.db.commit()
        await self.db.refresh(newsletter)

        logger.info(f"Draft newsletter created: ID={newsletter.id}")
        return newsletter


async def generate_weekly_newsletter(
    db: AsyncSession,
    auto_send: bool = False,
    created_by_id: Optional[int] = None
) -> Newsletter:
    """
    Generate and optionally send weekly newsletter

    Args:
        db: Database session
        auto_send: If True, send immediately after generation
        created_by_id: Admin user ID

    Returns:
        Newsletter instance
    """
    generator = NewsletterGenerator(db)

    # 1. Collect content
    content_data = await generator.collect_weekly_content(days=7)

    # 2. Generate with AI
    content = await generator.generate_newsletter(content_data)

    # 3. Save as draft
    newsletter = await generator.create_draft_newsletter(
        content=content,
        created_by_id=created_by_id
    )

    # 4. Auto-send if enabled
    if auto_send:
        from services.newsletter_service import send_newsletter_to_all
        sent_count = await send_newsletter_to_all(db, newsletter.id)
        logger.info(f"Newsletter auto-sent to {sent_count} subscribers")

    return newsletter
