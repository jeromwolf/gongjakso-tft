"""
AI Blog Generator

Automatically creates blog posts using AI
"""
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.blog import Blog, BlogStatus
from models.user import User
from core.config import settings
from loguru import logger
import openai
import json
import re


class BlogContent:
    """Blog content container"""
    def __init__(
        self,
        title: str,
        slug: str,
        content: str,
        excerpt: str,
        tags: List[str],
    ):
        self.title = title
        self.slug = slug
        self.content = content
        self.excerpt = excerpt
        self.tags = tags


class BlogGenerator:
    """AI-powered blog generator"""

    def __init__(self, db: AsyncSession):
        self.db = db
        # Set OpenAI API key
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured")
        openai.api_key = settings.OPENAI_API_KEY

    async def generate_blog_post(
        self,
        topic: Optional[str] = None,
        style: str = "technical"
    ) -> BlogContent:
        """
        Generate blog post using AI

        Args:
            topic: Optional specific topic to write about
            style: Writing style (technical, tutorial, tips, etc.)

        Returns:
            BlogContent with markdown content
        """
        # AI Prompt for blog generation
        if topic:
            prompt = f"""
당신은 'AI ON' 블로그의 전문 기술 작가입니다.

# 주제
{topic}

# 작성 가이드라인
1. **대상 독자**: 개발자, AI 엔지니어, 기술 스타트업
2. **톤**: 전문적이지만 친근하고 이해하기 쉬운
3. **길이**: 1500-2000자 (읽는 시간 5-7분)
4. **구조**:
   - 도입부 (왜 이 주제가 중요한가?)
   - 본문 (핵심 내용, 예제 코드, 실전 팁)
   - 결론 (요약 및 다음 단계)
5. **형식**: Markdown으로 작성
   - 제목: h2 (##), h3 (###) 사용
   - 코드: ```언어명 블록 사용
   - 강조: **굵게**, *기울임*
   - 리스트: -, * 사용

# 출력 형식
JSON 형식으로 출력하세요:
{{
  "title": "블로그 제목 (40자 이내, SEO 최적화)",
  "excerpt": "한 줄 요약 (100자 이내)",
  "content": "Markdown 형식의 본문",
  "tags": ["태그1", "태그2", "태그3", "태그4", "태그5"],
  "slug": "url-friendly-slug"
}}

태그는 다음 중에서 선택하거나 관련된 새 태그 생성:
- AI, Machine Learning, Deep Learning
- Python, JavaScript, TypeScript, FastAPI, Next.js
- Backend, Frontend, Fullstack
- DevOps, Cloud, AWS, Azure
- Tutorial, Tips, Best Practices
"""
        else:
            # Auto-generate trending topic
            prompt = """
당신은 'AI ON' 블로그의 전문 기술 작가입니다.

# 목표
개발자들이 관심 있어할 만한 최신 AI/개발 트렌드 주제로 블로그 포스트를 작성하세요.

# 추천 주제 (이 중 하나 선택 또는 유사한 주제):
1. AI 에이전트 개발 실전 팁
2. FastAPI + PostgreSQL 성능 최적화
3. Next.js 15의 새로운 기능
4. LangChain/LlamaIndex 활용법
5. TypeScript 고급 패턴
6. 실시간 데이터 처리 with WebSocket
7. GitHub Actions CI/CD 구축
8. Docker 컨테이너 최적화
9. 프롬프트 엔지니어링 베스트 프랙티스
10. 비동기 프로그래밍 패턴

# 작성 가이드라인
1. **대상 독자**: 개발자, AI 엔지니어
2. **톤**: 전문적이지만 친근함
3. **길이**: 1500-2000자
4. **구조**:
   - 도입부 (문제 제기)
   - 본문 (해결책, 예제)
   - 결론 (요약, 다음 단계)
5. **형식**: Markdown

# 출력 형식
JSON 형식으로 출력하세요:
{{
  "title": "블로그 제목 (40자 이내)",
  "excerpt": "한 줄 요약 (100자 이내)",
  "content": "Markdown 형식의 본문",
  "tags": ["태그1", "태그2", "태그3", "태그4", "태그5"],
  "slug": "url-friendly-slug"
}}
"""

        # Call OpenAI GPT-4
        logger.info("Generating blog post with GPT-4...")

        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{
                "role": "system",
                "content": "당신은 AI ON의 기술 블로그 전문 작가입니다. 개발자들이 좋아할 만한 고품질 기술 콘텐츠를 작성합니다."
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

        logger.info(f"Blog generated: {result['title']}")

        # Generate slug if not provided
        if 'slug' not in result or not result['slug']:
            result['slug'] = self._generate_slug(result['title'])

        return BlogContent(
            title=result['title'],
            slug=result['slug'],
            content=result['content'],
            excerpt=result['excerpt'],
            tags=result['tags'],
        )

    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        # Remove special characters and convert to lowercase
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        # Replace spaces with hyphens
        slug = re.sub(r'[-\s]+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        return slug[:200]  # Limit length

    async def create_draft_blog(
        self,
        content: BlogContent,
        author_id: int
    ) -> Blog:
        """
        Save generated blog as DRAFT

        Args:
            content: Generated blog content
            author_id: Admin user ID

        Returns:
            Blog model instance
        """
        # Check if slug already exists
        existing = await self.db.execute(
            select(Blog).where(Blog.slug == content.slug)
        )
        if existing.scalar_one_or_none():
            # Append timestamp to make unique
            content.slug = f"{content.slug}-{int(datetime.now().timestamp())}"

        blog = Blog(
            title=content.title,
            slug=content.slug,
            content=content.content,
            excerpt=content.excerpt,
            tags=",".join(content.tags),
            author_id=author_id,
            status=BlogStatus.DRAFT,
        )

        self.db.add(blog)
        await self.db.commit()
        await self.db.refresh(blog)

        logger.info(f"Draft blog created: ID={blog.id}, Slug={blog.slug}")
        return blog


async def generate_daily_blog(
    db: AsyncSession,
    author_id: int,
    topic: Optional[str] = None,
    auto_publish: bool = False
) -> Blog:
    """
    Generate and optionally publish daily blog

    Args:
        db: Database session
        author_id: Admin user ID (blog author)
        topic: Optional specific topic
        auto_publish: If True, publish immediately

    Returns:
        Blog instance
    """
    generator = BlogGenerator(db)

    # Generate with AI
    content = await generator.generate_blog_post(topic=topic)

    # Save as draft
    blog = await generator.create_draft_blog(
        content=content,
        author_id=author_id
    )

    # Auto-publish if enabled
    if auto_publish:
        blog.status = BlogStatus.PUBLISHED
        blog.published_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(blog)
        logger.info(f"Blog auto-published: ID={blog.id}")

    return blog
