"""
Email Service using Resend API
"""
import resend
from typing import List, Optional
from core.config import settings
from loguru import logger


# Configure Resend API
if settings.RESEND_API_KEY:
    resend.api_key = settings.RESEND_API_KEY


async def send_email(
    to: List[str],
    subject: str,
    html_content: str,
    from_email: Optional[str] = None,
) -> bool:
    """
    Send an email using Resend API

    Args:
        to: List of recipient email addresses
        subject: Email subject
        html_content: HTML content of the email
        from_email: Sender email (default from settings)

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY is not configured. Simulating email send (dev mode).")
        logger.info(f"[DEV MODE] Would send email to {len(to)} recipients: {subject}")
        return True  # Simulate success in dev mode

    try:
        from_address = from_email or settings.FROM_EMAIL

        params = {
            "from": from_address,
            "to": to,
            "subject": subject,
            "html": html_content,
        }

        logger.info(f"Sending email to {len(to)} recipients: {subject}")
        response = resend.Emails.send(params)
        logger.info(f"Email sent successfully. Response: {response}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False


async def send_newsletter(
    to: List[str],
    title: str,
    content: str,
) -> bool:
    """
    Send newsletter to subscribers

    Args:
        to: List of subscriber emails
        title: Newsletter title
        content: Newsletter content (Markdown or HTML)

    Returns:
        bool: True if newsletter was sent successfully, False otherwise
    """
    # Convert markdown content to HTML template
    html_content = newsletter_template(title, content)

    subject = f"📧 {title} - 데이터공작소 TFT Newsletter"

    return await send_email(
        to=to,
        subject=subject,
        html_content=html_content,
    )


def newsletter_template(title: str, content: str) -> str:
    """
    Generate HTML template for newsletter

    Args:
        title: Newsletter title
        content: Newsletter content (HTML or plain text)

    Returns:
        str: HTML template
    """
    # Simple HTML template
    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2563eb;
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            font-size: 16px;
            color: #444;
        }}
        .content h2 {{
            color: #1e40af;
            margin-top: 25px;
            margin-bottom: 15px;
        }}
        .content p {{
            margin-bottom: 15px;
        }}
        .content a {{
            color: #2563eb;
            text-decoration: none;
        }}
        .content a:hover {{
            text-decoration: underline;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            font-size: 14px;
            color: #666;
        }}
        .footer a {{
            color: #2563eb;
            text-decoration: none;
        }}
        .unsubscribe {{
            margin-top: 15px;
            font-size: 12px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📧 {title}</h1>
            <p style="color: #666; margin: 10px 0 0 0;">데이터공작소 개발 TFT Newsletter</p>
        </div>
        <div class="content">
            {content}
        </div>
        <div class="footer">
            <p>© 2025 데이터공작소 개발 TFT. All rights reserved.</p>
            <p>
                <a href="https://gongjakso-tft.up.railway.app">웹사이트 방문</a> |
                <a href="https://github.com/jeromwolf/gongjakso-tft">GitHub</a>
            </p>
            <p class="unsubscribe">
                이 뉴스레터를 더 이상 받고 싶지 않으시다면
                <a href="{{{{unsubscribe_url}}}}">구독 취소</a>를 클릭하세요.
            </p>
        </div>
    </div>
</body>
</html>
    """
    return html


async def send_subscription_confirmation(
    to: str,
    confirmation_token: str,
) -> bool:
    """
    Send subscription confirmation email

    Args:
        to: Subscriber email
        confirmation_token: Confirmation token

    Returns:
        bool: True if email was sent successfully
    """
    confirmation_url = f"{settings.FRONTEND_URL}/newsletter/confirm/{confirmation_token}"

    html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>구독 확인</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #f8f9fa; padding: 30px; border-radius: 8px;">
        <h1 style="color: #2563eb;">구독 확인</h1>
        <p>데이터공작소 TFT 뉴스레터 구독을 환영합니다!</p>
        <p>아래 버튼을 클릭하여 구독을 확인해주세요:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{confirmation_url}"
               style="display: inline-block; padding: 12px 30px; background-color: #2563eb; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">
                구독 확인하기
            </a>
        </div>
        <p style="color: #666; font-size: 14px;">
            또는 다음 링크를 복사하여 브라우저에 붙여넣으세요:<br>
            <a href="{confirmation_url}">{confirmation_url}</a>
        </p>
        <p style="color: #999; font-size: 12px; margin-top: 30px;">
            본인이 구독 신청을 하지 않았다면 이 이메일을 무시하셔도 됩니다.
        </p>
    </div>
</body>
</html>
    """

    return await send_email(
        to=[to],
        subject="🎉 데이터공작소 TFT 뉴스레터 구독 확인",
        html_content=html_content,
    )
