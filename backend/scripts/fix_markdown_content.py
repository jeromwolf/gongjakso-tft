"""
Fix Markdown Content in Projects

This script removes code block backticks from project content fields
that are wrapped in triple backticks, causing markdown rendering issues.
"""
import asyncio
import httpx
from loguru import logger

# API Configuration
API_BASE_URL = "https://gongjakso-tft.onrender.com"
# API_BASE_URL = "http://localhost:8000"  # Use this for local testing

# Admin credentials
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"


async def login() -> str:
    """Login and get access token"""
    async with httpx.AsyncClient() as client:
        # JSON format
        response = await client.post(
            f"{API_BASE_URL}/api/auth/login",
            json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD,
            },
        )

        if response.status_code != 200:
            logger.error(f"Login failed: {response.text}")
            raise Exception("Failed to login")

        data = response.json()
        token = data["access_token"]
        logger.info(f"✅ Logged in as admin")
        return token


async def get_all_projects(token: str) -> list:
    """Get all projects"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/api/projects?page_size=100",
            headers={"Authorization": f"Bearer {token}"},
        )

        if response.status_code != 200:
            logger.error(f"Failed to get projects: {response.text}")
            raise Exception("Failed to get projects")

        data = response.json()
        projects = data["items"]
        logger.info(f"📦 Found {len(projects)} projects")
        return projects


async def update_project(token: str, project_id: int, content: str) -> None:
    """Update project content"""
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{API_BASE_URL}/api/projects/{project_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"content": content},
        )

        if response.status_code != 200:
            logger.error(f"Failed to update project {project_id}: {response.text}")
            raise Exception(f"Failed to update project {project_id}")

        logger.info(f"✅ Updated project {project_id}")


def fix_markdown_content(content: str) -> str:
    """Remove code block backticks from content"""
    if content.startswith("```") and content.endswith("```"):
        # Remove leading and trailing backticks
        content = content[3:-3].strip()
        logger.info("  - Removed code block backticks")
        return content
    return content


async def get_project_by_id(token: str, project_id: int) -> dict:
    """Get individual project by ID to fetch content"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/api/projects/{project_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        if response.status_code != 200:
            logger.error(f"Failed to get project {project_id}: {response.text}")
            return None

        return response.json()


async def main():
    """Main function"""
    logger.info("🚀 Starting markdown content fix...")

    # Login
    token = await login()

    # Get all projects (without content)
    projects = await get_all_projects(token)

    # Check and fix each project
    fixed_count = 0
    for project in projects:
        project_id = project["id"]
        project_name = project["name"]

        # Get full project data with content
        logger.info(f"📥 Fetching {project_name}...")
        full_project = await get_project_by_id(token, project_id)

        if not full_project:
            logger.warning(f"⚠️  Could not fetch {project_name}")
            continue

        content = full_project.get("content")

        if not content:
            logger.info(f"⏭️  Skipping {project_name} (no content)")
            continue

        # Check if content needs fixing
        if content.startswith("```") and content.endswith("```"):
            logger.info(f"🔧 Fixing {project_name}...")
            fixed_content = fix_markdown_content(content)

            # Update project
            await update_project(token, project_id, fixed_content)
            fixed_count += 1
        else:
            logger.info(f"✅ {project_name} - content is OK")

    logger.info(f"\n🎉 Done! Fixed {fixed_count} project(s)")


if __name__ == "__main__":
    asyncio.run(main())
