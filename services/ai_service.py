"""
AI Service using OpenAI API
"""
from typing import Optional, List, Dict, Any
from openai import AsyncOpenAI
from core.config import settings
from loguru import logger


# Initialize OpenAI client
if settings.OPENAI_API_KEY:
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
else:
    client = None
    logger.warning("OPENAI_API_KEY is not configured. AI features will be disabled.")


async def generate_blog_content(
    topic: str,
    style: str = "technical",
    length: str = "medium",
    project_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, str]:
    """
    Generate blog content using OpenAI API

    Args:
        topic: Blog topic or title
        style: Writing style (technical, casual, tutorial, etc.)
        length: Content length (short, medium, long)
        project_data: Optional project data to include

    Returns:
        Dict with title, excerpt, content, and tags
    """
    if not client:
        raise ValueError("OPENAI_API_KEY is not configured")

    # Build prompt based on parameters
    prompt = _build_blog_prompt(topic, style, length, project_data)

    try:
        logger.info(f"Generating blog content for topic: {topic}")

        response = await client.chat.completions.create(
            model="gpt-4o",
            max_tokens=4000,
            temperature=0.7,
            messages=[
                {
                    "role": "system",
                    "content": "당신은 데이터공작소 개발 TFT의 전문 기술 블로그 작성자입니다. 한국어로 고품질의 기술 블로그를 작성합니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract content from response
        content = response.choices[0].message.content

        # Parse structured response
        parsed = _parse_blog_response(content)

        logger.info(f"Successfully generated blog content: {parsed['title']}")
        return parsed

    except Exception as e:
        logger.error(f"Failed to generate blog content: {str(e)}")
        raise


async def generate_newsletter_content(
    period_days: int = 7,
    blog_posts: Optional[List[Dict[str, Any]]] = None,
    projects: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, str]:
    """
    Generate newsletter content using OpenAI API

    Args:
        period_days: Period in days (7 for weekly, 30 for monthly)
        blog_posts: Recent blog posts
        projects: Recent project updates

    Returns:
        Dict with title and content (HTML)
    """
    if not client:
        raise ValueError("OPENAI_API_KEY is not configured")

    # Build prompt with context
    prompt = _build_newsletter_prompt(period_days, blog_posts, projects)

    try:
        logger.info(f"Generating newsletter content (period: {period_days} days)")

        response = await client.chat.completions.create(
            model="gpt-4o",
            max_tokens=3000,
            temperature=0.7,
            messages=[
                {
                    "role": "system",
                    "content": "당신은 데이터공작소 개발 TFT의 뉴스레터 작성자입니다. 한국어로 친근하고 매력적인 뉴스레터를 작성합니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract content from response
        content = response.choices[0].message.content

        # Parse structured response
        parsed = _parse_newsletter_response(content)

        logger.info(f"Successfully generated newsletter: {parsed['title']}")
        return parsed

    except Exception as e:
        logger.error(f"Failed to generate newsletter content: {str(e)}")
        raise


def _build_blog_prompt(
    topic: str,
    style: str,
    length: str,
    project_data: Optional[Dict[str, Any]] = None,
) -> str:
    """Build prompt for blog generation"""

    length_guide = {
        "short": "500-800 words",
        "medium": "1000-1500 words",
        "long": "2000-3000 words",
    }

    style_guide = {
        "technical": "기술적이고 심도 있는 분석",
        "casual": "편안하고 친근한 어조",
        "tutorial": "단계별 설명과 예제 중심",
        "news": "뉴스 보도 형식",
    }

    prompt = f"""데이터공작소 개발 TFT를 위한 블로그 글을 작성해주세요.

**주제**: {topic}

**스타일**: {style_guide.get(style, "전문적이고 정보를 제공하는")}
**길이**: {length_guide.get(length, "1000-1500 words")}

**요구사항**:
1. 한국어로 작성
2. 기술 블로그 독자를 대상으로 함
3. Markdown 형식으로 작성
4. 실용적인 예제와 인사이트 포함
5. SEO 친화적인 제목과 요약

"""

    if project_data:
        prompt += f"""
**프로젝트 정보**:
- 프로젝트명: {project_data.get('name')}
- 설명: {project_data.get('description')}
- 기술 스택: {', '.join(project_data.get('tech_stack', []))}
- GitHub: {project_data.get('github_url')}

위 프로젝트와 관련된 내용을 포함해주세요.
"""

    prompt += """
**응답 형식** (다음 형식을 정확히 따라주세요):

TITLE: [블로그 제목]

EXCERPT: [2-3문장의 요약]

TAGS: [태그1, 태그2, 태그3] (쉼표로 구분)

CONTENT:
[여기에 Markdown 형식의 본문 작성]

---

위 형식을 정확히 지켜서 작성해주세요."""

    return prompt


def _build_newsletter_prompt(
    period_days: int,
    blog_posts: Optional[List[Dict[str, Any]]],
    projects: Optional[List[Dict[str, Any]]],
) -> str:
    """Build prompt for newsletter generation"""

    period_text = "주간" if period_days == 7 else "월간"

    prompt = f"""데이터공작소 개발 TFT의 {period_text} 뉴스레터를 작성해주세요.

**기간**: 최근 {period_days}일

**포함 내용**:
1. 최근 블로그 포스트 요약
2. 프로젝트 업데이트
3. 개발 팀 소식
4. 다음 주 예고

"""

    if blog_posts:
        prompt += "\n**최근 블로그 포스트**:\n"
        for post in blog_posts[:5]:
            prompt += f"- {post.get('title')}: {post.get('excerpt', '')}\n"

    if projects:
        prompt += "\n**프로젝트 업데이트**:\n"
        for project in projects[:5]:
            prompt += f"- {project.get('name')}: {project.get('description', '')}\n"

    prompt += """
**요구사항**:
1. 한국어로 작성
2. 친근하고 읽기 쉬운 어조
3. HTML 형식으로 작성 (이메일 전송용)
4. 각 섹션을 명확히 구분
5. 독자의 관심을 끌 수 있는 매력적인 제목

**응답 형식** (다음 형식을 정확히 따라주세요):

TITLE: [뉴스레터 제목]

CONTENT:
[여기에 HTML 형식의 본문 작성]

---

HTML은 간단한 태그만 사용하세요 (h2, h3, p, ul, li, a, strong, em).
위 형식을 정확히 지켜서 작성해주세요."""

    return prompt


def _parse_blog_response(content: str) -> Dict[str, str]:
    """Parse Claude's blog response into structured data"""

    lines = content.split('\n')

    title = ""
    excerpt = ""
    tags = []
    blog_content = []

    current_section = None

    for line in lines:
        line = line.strip()

        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
            current_section = "title"
        elif line.startswith("EXCERPT:"):
            excerpt = line.replace("EXCERPT:", "").strip()
            current_section = "excerpt"
        elif line.startswith("TAGS:"):
            tags_str = line.replace("TAGS:", "").strip()
            tags = [tag.strip() for tag in tags_str.split(',')]
            current_section = "tags"
        elif line.startswith("CONTENT:"):
            current_section = "content"
        elif current_section == "content" and line:
            blog_content.append(line)

    # Join content lines
    content_text = '\n'.join(blog_content).strip()

    # Remove any trailing --- markers
    content_text = content_text.replace('---', '').strip()

    return {
        "title": title or "생성된 블로그 제목",
        "excerpt": excerpt or "",
        "content": content_text,
        "tags": tags,
    }


def _parse_newsletter_response(content: str) -> Dict[str, str]:
    """Parse Claude's newsletter response into structured data"""

    lines = content.split('\n')

    title = ""
    newsletter_content = []

    current_section = None

    for line in lines:
        line_stripped = line.strip()

        if line_stripped.startswith("TITLE:"):
            title = line_stripped.replace("TITLE:", "").strip()
            current_section = "title"
        elif line_stripped.startswith("CONTENT:"):
            current_section = "content"
        elif current_section == "content" and line:
            newsletter_content.append(line)

    # Join content lines
    content_text = '\n'.join(newsletter_content).strip()

    # Remove any trailing --- markers
    content_text = content_text.replace('---', '').strip()

    return {
        "title": title or "데이터공작소 TFT 뉴스레터",
        "content": content_text,
    }
