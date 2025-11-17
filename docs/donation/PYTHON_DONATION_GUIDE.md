# 🐍 Python 후원 기능 구현 가이드

## 📦 개요

Python 웹 프레임워크(FastAPI, Flask, Django)에서 토스 후원 기능을 구현하는 가이드입니다.

---

## 🎯 구현 방식

1. **프론트엔드** - HTML/JS로 후원 페이지 렌더링
2. **백엔드** - Python으로 템플릿 제공 및 API 엔드포인트
3. **토스 연동** - 딥링크 or QR 코드 사용

---

## 1️⃣ FastAPI 구현 (추천)

### 📁 프로젝트 구조

```
your-project/
├── main.py                 # FastAPI 앱
├── templates/
│   └── donation.html       # 후원 페이지
├── static/
│   ├── css/
│   │   └── donation.css
│   ├── js/
│   │   └── donation.js
│   └── images/
│       └── toss-qr.png
└── config.py               # 설정 파일
```

### 📄 `config.py` - 설정 파일

```python
"""
후원 설정 파일
"""
from pydantic_settings import BaseSettings

class DonationConfig(BaseSettings):
    """후원 설정"""

    # 계좌 정보
    ACCOUNT_NUMBER: str = "100039997509"
    BANK_NAME: str = "토스뱅크"

    # 토스 딥링크 (선택사항)
    TOSS_DEEP_LINK: str = "supertoss://send?amount=0&bank=%ED%86%A0%EC%8A%A4%EB%B1%85%ED%81%AC&accountNo=100039997509&origin=qr"

    # 후원 금액 옵션
    DONATION_AMOUNTS: list[dict] = [
        {
            "emoji": "☕",
            "amount": 5000,
            "label": "₩5,000 커피 한 잔",
            "description": "AI 도구 1일 사용료",
            "highlight": False
        },
        {
            "emoji": "⭐",
            "amount": 20000,
            "label": "₩20,000 AI 도구 지원",
            "description": "추천! 월간 구독료",
            "highlight": True
        },
        {
            "emoji": "💝",
            "amount": 0,
            "label": "자유 금액",
            "description": "원하시는 만큼 후원",
            "highlight": False
        }
    ]

    # 후원금 사용처
    DONATION_USAGES: list[dict] = [
        {
            "emoji": "🤖",
            "title": "AI 개발 도구 구독료",
            "description": "Claude Code, GitHub Copilot 등"
        },
        {
            "emoji": "💻",
            "title": "오픈소스 프로젝트 개발",
            "description": "유용한 도구를 만들어 공유"
        },
        {
            "emoji": "💾",
            "title": "서버 호스팅 비용",
            "description": "안정적인 서비스 제공"
        },
        {
            "emoji": "🎓",
            "title": "기술 문서화 및 튜토리얼",
            "description": "누구나 쉽게 배울 수 있는 콘텐츠"
        }
    ]

    class Config:
        env_file = ".env"

donation_config = DonationConfig()
```

### 📄 `main.py` - FastAPI 앱

```python
"""
FastAPI 후원 페이지 예제
"""
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import logging

from config import donation_config

# FastAPI 앱 초기화
app = FastAPI(title="후원 시스템")

# 정적 파일 & 템플릿
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 로거 설정
logger = logging.getLogger(__name__)


# === 후원 페이지 ===

@app.get("/donation")
async def donation_page(request: Request):
    """
    후원 페이지 렌더링
    """
    return templates.TemplateResponse(
        "donation.html",
        {
            "request": request,
            "account_number": donation_config.ACCOUNT_NUMBER,
            "bank_name": donation_config.BANK_NAME,
            "toss_deep_link": donation_config.TOSS_DEEP_LINK,
            "amounts": donation_config.DONATION_AMOUNTS,
            "usages": donation_config.DONATION_USAGES,
            "qr_code_url": "/static/images/toss-qr.png"
        }
    )


# === API 엔드포인트 (선택사항) ===

class DonationLog(BaseModel):
    """후원 로그 (실제 결제는 토스에서 처리)"""
    amount: int
    message: str = ""
    donor_name: str = "익명"

@app.post("/api/donation/log")
async def log_donation(log: DonationLog):
    """
    후원 의도 로깅 (실제 결제 전)
    실제 결제는 토스 앱에서 이루어지므로, 여기서는 로그만 기록
    """
    logger.info(f"후원 의도: {log.donor_name} - ₩{log.amount:,}")

    # TODO: 데이터베이스에 로그 저장
    # donation_log = DonationLogModel(
    #     amount=log.amount,
    #     message=log.message,
    #     donor_name=log.donor_name,
    #     created_at=datetime.now()
    # )
    # await db.save(donation_log)

    return {
        "success": True,
        "message": "후원 감사합니다!",
        "amount": log.amount
    }


@app.get("/api/donation/config")
async def get_donation_config():
    """
    후원 설정 정보 반환 (프론트엔드에서 사용)
    """
    return {
        "account_number": donation_config.ACCOUNT_NUMBER,
        "bank_name": donation_config.BANK_NAME,
        "toss_deep_link": donation_config.TOSS_DEEP_LINK,
        "amounts": donation_config.DONATION_AMOUNTS,
        "usages": donation_config.DONATION_USAGES
    }


# === 메인 실행 ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

### 📄 `templates/donation.html` - 후원 페이지

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>☕ 커피 한 잔의 후원</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }
    </style>
</head>
<body>
    <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-12 text-white">
            <h1 class="text-4xl font-bold mb-4">☕ 커피 한 잔의 후원</h1>
            <p class="text-lg mb-2">우리는 오픈소스와 기술 공유를 통해 더 나은 개발 생태계를 만들어가고 있습니다.</p>
            <p class="text-sm opacity-80">
                Claude Code, GitHub Copilot 등 AI 도구의 정액제 비용을 후원해 주시면,<br>
                더 많은 프로젝트를 개발하고 소스를 공개할 수 있습니다. 💜
            </p>
        </div>

        <!-- Main Section -->
        <div class="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-8 mb-8">
            <div class="grid md:grid-cols-2 gap-8">
                <!-- Left: Amount Options -->
                <div>
                    <h2 class="text-2xl font-bold text-white mb-4">☕ 따뜻한 마음을 담아</h2>
                    <p class="text-white/80 mb-6">
                        여러분의 후원은 더 나은 오픈소스 프로젝트를 만드는 데 사용됩니다.<br>
                        원하시는 금액으로 자유롭게 후원해주세요.
                    </p>

                    <!-- Amount Cards -->
                    <div class="space-y-3 mb-6">
                        {% for amount in amounts %}
                        <div class="flex items-center gap-3 p-3 rounded-lg {% if amount.highlight %}bg-blue-500/30 border-2 border-blue-400{% else %}bg-white/10 border border-white/20{% endif %} hover:bg-white/20 transition">
                            <span class="text-2xl">{{ amount.emoji }}</span>
                            <div>
                                <p class="text-white font-medium">{{ amount.label }}</p>
                                <p class="text-sm {% if amount.highlight %}text-blue-200{% else %}text-white/60{% endif %}">
                                    {{ amount.description }}
                                </p>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <!-- Right: Donation Button + QR -->
                <div class="flex flex-col items-center justify-center">
                    <button
                        onclick="handleDonation()"
                        class="w-full px-8 py-4 bg-blue-600 hover:bg-blue-700 rounded-xl font-bold transition text-white text-lg mb-6 shadow-lg hover:shadow-xl cursor-pointer"
                    >
                        💝 토스로 후원하기
                    </button>

                    <div class="bg-white p-5 rounded-xl shadow-lg">
                        <img src="{{ qr_code_url }}" alt="토스 QR 코드" class="w-40 h-40 object-contain">
                    </div>
                    <p class="text-sm text-white/60 mt-4">📱 또는 QR 코드를 스캔하세요</p>
                </div>
            </div>
        </div>

        <!-- Usage Section -->
        <div class="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-8">
            <h2 class="text-2xl font-bold text-white mb-6 text-center">💡 후원금은 이렇게 사용됩니다</h2>
            <div class="grid md:grid-cols-2 gap-6">
                {% for usage in usages %}
                <div class="text-center text-white">
                    <div class="text-4xl mb-3">{{ usage.emoji }}</div>
                    <h3 class="font-semibold mb-2">{{ usage.title }}</h3>
                    <p class="text-sm text-white/70">{{ usage.description }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <script>
        // 후원 설정
        const config = {
            accountNumber: "{{ account_number }}",
            bankName: "{{ bank_name }}",
            tossDeepLink: "{{ toss_deep_link }}"
        };

        function handleDonation() {
            const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
            const accountInfo = `${config.bankName} ${config.accountNumber}`;

            if (isMobile && config.tossDeepLink) {
                // 모바일: 토스 앱 열기
                window.location.href = config.tossDeepLink;
            } else {
                // PC: 계좌번호 복사
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(accountInfo).then(() => {
                        alert(`📋 계좌번호가 복사되었습니다!\n\n${accountInfo}\n\n토스 앱이나 은행 앱에서 붙여넣기 해주세요 😊`);
                    }).catch(() => {
                        alert(`💝 후원 계좌번호\n\n${accountInfo}\n\n토스 앱이나 은행 앱에서 송금해주세요!`);
                    });
                } else {
                    alert(`💝 후원 계좌번호\n\n${accountInfo}\n\n토스 앱이나 은행 앱에서 송금해주세요!`);
                }
            }
        }
    </script>
</body>
</html>
```

### 📦 설치 및 실행

```bash
# 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install fastapi uvicorn jinja2 python-multipart pydantic-settings

# 서버 실행
uvicorn main:app --reload

# 브라우저에서 접속
# http://localhost:8000/donation
```

---

## 2️⃣ Flask 구현

### 📄 `app.py` - Flask 앱

```python
"""
Flask 후원 페이지 예제
"""
from flask import Flask, render_template, jsonify, request
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# 로거 설정
logger = logging.getLogger(__name__)

# 후원 설정
DONATION_CONFIG = {
    "account_number": "100039997509",
    "bank_name": "토스뱅크",
    "toss_deep_link": "supertoss://send?amount=0&bank=%ED%86%A0%EC%8A%A4%EB%B1%85%ED%81%AC&accountNo=100039997509&origin=qr",
    "amounts": [
        {
            "emoji": "☕",
            "amount": 5000,
            "label": "₩5,000 커피 한 잔",
            "description": "AI 도구 1일 사용료",
            "highlight": False
        },
        {
            "emoji": "⭐",
            "amount": 20000,
            "label": "₩20,000 AI 도구 지원",
            "description": "추천! 월간 구독료",
            "highlight": True
        },
        {
            "emoji": "💝",
            "amount": 0,
            "label": "자유 금액",
            "description": "원하시는 만큼 후원",
            "highlight": False
        }
    ],
    "usages": [
        {
            "emoji": "🤖",
            "title": "AI 개발 도구 구독료",
            "description": "Claude Code, GitHub Copilot 등"
        },
        {
            "emoji": "💻",
            "title": "오픈소스 프로젝트 개발",
            "description": "유용한 도구를 만들어 공유"
        },
        {
            "emoji": "💾",
            "title": "서버 호스팅 비용",
            "description": "안정적인 서비스 제공"
        },
        {
            "emoji": "🎓",
            "title": "기술 문서화 및 튜토리얼",
            "description": "누구나 쉽게 배울 수 있는 콘텐츠"
        }
    ]
}


@app.route('/donation')
def donation_page():
    """후원 페이지 렌더링"""
    return render_template(
        'donation.html',
        account_number=DONATION_CONFIG['account_number'],
        bank_name=DONATION_CONFIG['bank_name'],
        toss_deep_link=DONATION_CONFIG['toss_deep_link'],
        amounts=DONATION_CONFIG['amounts'],
        usages=DONATION_CONFIG['usages'],
        qr_code_url='/static/images/toss-qr.png'
    )


@app.route('/api/donation/config')
def get_donation_config():
    """후원 설정 API"""
    return jsonify(DONATION_CONFIG)


@app.route('/api/donation/log', methods=['POST'])
def log_donation():
    """후원 의도 로깅"""
    data = request.get_json()
    amount = data.get('amount', 0)
    donor_name = data.get('donor_name', '익명')
    message = data.get('message', '')

    logger.info(f"후원 의도: {donor_name} - ₩{amount:,}")

    # TODO: 데이터베이스에 저장

    return jsonify({
        'success': True,
        'message': '후원 감사합니다!',
        'amount': amount
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
```

### 📦 Flask 설치 및 실행

```bash
# 의존성 설치
pip install flask

# 서버 실행
python app.py

# 접속: http://localhost:8000/donation
```

---

## 3️⃣ Django 구현

### 📁 프로젝트 구조

```
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   └── urls.py
└── donation/
    ├── views.py
    ├── urls.py
    ├── templates/
    │   └── donation/
    │       └── index.html
    └── static/
        └── donation/
            └── images/
                └── toss-qr.png
```

### 📄 `donation/views.py`

```python
"""
Django 후원 뷰
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import logging

logger = logging.getLogger(__name__)

# 후원 설정
DONATION_CONFIG = {
    "account_number": "100039997509",
    "bank_name": "토스뱅크",
    "toss_deep_link": "supertoss://send?amount=0&bank=%ED%86%A0%EC%8A%A4%EB%B1%85%ED%81%AC&accountNo=100039997509&origin=qr",
    "amounts": [
        {
            "emoji": "☕",
            "amount": 5000,
            "label": "₩5,000 커피 한 잔",
            "description": "AI 도구 1일 사용료",
            "highlight": False
        },
        {
            "emoji": "⭐",
            "amount": 20000,
            "label": "₩20,000 AI 도구 지원",
            "description": "추천! 월간 구독료",
            "highlight": True
        },
        {
            "emoji": "💝",
            "amount": 0,
            "label": "자유 금액",
            "description": "원하시는 만큼 후원",
            "highlight": False
        }
    ],
    "usages": [
        {
            "emoji": "🤖",
            "title": "AI 개발 도구 구독료",
            "description": "Claude Code, GitHub Copilot 등"
        },
        {
            "emoji": "💻",
            "title": "오픈소스 프로젝트 개발",
            "description": "유용한 도구를 만들어 공유"
        },
        {
            "emoji": "💾",
            "title": "서버 호스팅 비용",
            "description": "안정적인 서비스 제공"
        },
        {
            "emoji": "🎓",
            "title": "기술 문서화 및 튜토리얼",
            "description": "누구나 쉽게 배울 수 있는 콘텐츠"
        }
    ]
}


def donation_page(request):
    """후원 페이지"""
    context = {
        'account_number': DONATION_CONFIG['account_number'],
        'bank_name': DONATION_CONFIG['bank_name'],
        'toss_deep_link': DONATION_CONFIG['toss_deep_link'],
        'amounts': DONATION_CONFIG['amounts'],
        'usages': DONATION_CONFIG['usages'],
        'qr_code_url': '/static/donation/images/toss-qr.png'
    }
    return render(request, 'donation/index.html', context)


@require_http_methods(["GET"])
def donation_config_api(request):
    """후원 설정 API"""
    return JsonResponse(DONATION_CONFIG)


@require_http_methods(["POST"])
def donation_log_api(request):
    """후원 의도 로깅 API"""
    try:
        data = json.loads(request.body)
        amount = data.get('amount', 0)
        donor_name = data.get('donor_name', '익명')
        message = data.get('message', '')

        logger.info(f"후원 의도: {donor_name} - ₩{amount:,}")

        # TODO: 데이터베이스에 저장

        return JsonResponse({
            'success': True,
            'message': '후원 감사합니다!',
            'amount': amount
        })
    except Exception as e:
        logger.error(f"후원 로그 에러: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': '오류가 발생했습니다.'
        }, status=400)
```

### 📄 `donation/urls.py`

```python
"""
Django 후원 URL 설정
"""
from django.urls import path
from . import views

app_name = 'donation'

urlpatterns = [
    path('', views.donation_page, name='index'),
    path('api/config/', views.donation_config_api, name='config'),
    path('api/log/', views.donation_log_api, name='log'),
]
```

### 📄 `myproject/urls.py` - 메인 URL 설정

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('donation/', include('donation.urls')),
]
```

### 📦 Django 실행

```bash
# Django 설치
pip install django

# 프로젝트 생성 (이미 있으면 생략)
django-admin startproject myproject

# 앱 생성
python manage.py startapp donation

# 마이그레이션
python manage.py migrate

# 서버 실행
python manage.py runserver

# 접속: http://localhost:8000/donation/
```

---

## 4️⃣ 데이터베이스 모델 (선택사항)

### FastAPI + SQLAlchemy

```python
"""
후원 로그 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class DonationLog(Base):
    """후원 의도 로그 (실제 결제는 토스에서 처리)"""
    __tablename__ = "donation_logs"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    donor_name = Column(String(100), default="익명")
    message = Column(Text, nullable=True)

    # 실제 결제 여부는 토스에서 확인 필요
    status = Column(String(20), default="pending")  # pending, completed, cancelled

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<DonationLog(id={self.id}, amount={self.amount}, donor={self.donor_name})>"
```

### Django Model

```python
"""
Django 후원 로그 모델
"""
from django.db import models

class DonationLog(models.Model):
    """후원 의도 로그"""

    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('completed', '완료'),
        ('cancelled', '취소'),
    ]

    amount = models.IntegerField(verbose_name="금액")
    donor_name = models.CharField(max_length=100, default="익명", verbose_name="후원자")
    message = models.TextField(blank=True, null=True, verbose_name="메시지")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="상태")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class Meta:
        db_table = 'donation_logs'
        ordering = ['-created_at']
        verbose_name = '후원 로그'
        verbose_name_plural = '후원 로그'

    def __str__(self):
        return f"{self.donor_name} - ₩{self.amount:,}"
```

---

## 5️⃣ 토스 페이먼츠 API 연동 (고급)

실제 결제를 받으려면 토스 페이먼츠 API를 사용해야 합니다.

### 📦 설치

```bash
pip install requests
```

### 📄 토스 페이먼츠 결제 요청

```python
"""
토스 페이먼츠 API 연동
"""
import requests
import base64
from typing import Optional

class TossPayments:
    """토스 페이먼츠 API 클래스"""

    def __init__(self, secret_key: str, client_key: str):
        self.secret_key = secret_key
        self.client_key = client_key
        self.base_url = "https://api.tosspayments.com/v1"

        # Basic Auth 헤더 생성
        encoded = base64.b64encode(f"{secret_key}:".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json"
        }

    def create_payment(
        self,
        amount: int,
        order_id: str,
        order_name: str,
        customer_name: str = "익명",
        success_url: str = None,
        fail_url: str = None
    ) -> dict:
        """
        결제 요청 생성

        Args:
            amount: 결제 금액
            order_id: 주문 ID (고유값)
            order_name: 주문명
            customer_name: 고객명
            success_url: 성공 시 리다이렉트 URL
            fail_url: 실패 시 리다이렉트 URL

        Returns:
            결제 정보 딕셔너리
        """
        url = f"{self.base_url}/payments"

        data = {
            "amount": amount,
            "orderId": order_id,
            "orderName": order_name,
            "customerName": customer_name,
            "successUrl": success_url or "http://localhost:8000/donation/success",
            "failUrl": fail_url or "http://localhost:8000/donation/fail"
        }

        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def confirm_payment(self, payment_key: str, order_id: str, amount: int) -> dict:
        """
        결제 승인

        Args:
            payment_key: 결제 키
            order_id: 주문 ID
            amount: 결제 금액

        Returns:
            결제 승인 결과
        """
        url = f"{self.base_url}/payments/confirm"

        data = {
            "paymentKey": payment_key,
            "orderId": order_id,
            "amount": amount
        }

        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def get_payment(self, payment_key: str) -> dict:
        """결제 정보 조회"""
        url = f"{self.base_url}/payments/{payment_key}"
        response = requests.get(url, headers=self.headers)
        return response.json()


# === 사용 예시 ===

# 토스 페이먼츠 초기화
toss = TossPayments(
    secret_key="test_sk_...",  # 토스 개발자 센터에서 발급
    client_key="test_ck_..."
)

# 결제 요청
payment = toss.create_payment(
    amount=5000,
    order_id="ORDER_20250129_001",
    order_name="커피 한 잔 후원",
    customer_name="홍길동"
)
```

### FastAPI 결제 엔드포인트

```python
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

app = FastAPI()

# 토스 페이먼츠 초기화
toss = TossPayments(
    secret_key="test_sk_...",
    client_key="test_ck_..."
)

class PaymentRequest(BaseModel):
    amount: int
    order_name: str
    customer_name: str = "익명"

@app.post("/api/donation/payment")
async def create_payment(req: PaymentRequest):
    """결제 요청 생성"""
    import uuid
    order_id = f"ORDER_{uuid.uuid4().hex[:12]}"

    try:
        payment = toss.create_payment(
            amount=req.amount,
            order_id=order_id,
            order_name=req.order_name,
            customer_name=req.customer_name
        )
        return payment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/donation/success")
async def payment_success(request: Request):
    """결제 성공 콜백"""
    payment_key = request.query_params.get("paymentKey")
    order_id = request.query_params.get("orderId")
    amount = int(request.query_params.get("amount"))

    # 결제 승인
    result = toss.confirm_payment(payment_key, order_id, amount)

    # TODO: 데이터베이스에 저장

    return {"message": "후원 감사합니다!", "result": result}
```

---

## 6️⃣ 환경변수 설정

### `.env` 파일

```bash
# 후원 계좌 정보
ACCOUNT_NUMBER=100039997509
BANK_NAME=토스뱅크
TOSS_DEEP_LINK=supertoss://send?amount=0&bank=%ED%86%A0%EC%8A%A4%EB%B1%85%ED%81%AC&accountNo=100039997509&origin=qr

# 토스 페이먼츠 API (선택사항)
TOSS_SECRET_KEY=test_sk_...
TOSS_CLIENT_KEY=test_ck_...
```

### Python에서 읽기

```python
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_NUMBER = os.getenv("ACCOUNT_NUMBER")
BANK_NAME = os.getenv("BANK_NAME")
TOSS_DEEP_LINK = os.getenv("TOSS_DEEP_LINK")
```

---

## 📋 체크리스트

- [ ] Python 프레임워크 선택 (FastAPI/Flask/Django)
- [ ] 계좌번호 및 은행명 설정
- [ ] 토스 딥링크 생성
- [ ] QR 코드 이미지 준비
- [ ] HTML 템플릿 작성
- [ ] 후원 금액 옵션 커스터마이징
- [ ] 후원금 사용처 설명 작성
- [ ] (선택) 데이터베이스 모델 생성
- [ ] (선택) 토스 페이먼츠 API 연동
- [ ] 모바일/PC 환경에서 테스트

---

## 🚀 빠른 시작 (FastAPI)

```bash
# 1. 프로젝트 생성
mkdir my-donation-app
cd my-donation-app

# 2. 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 3. 의존성 설치
pip install fastapi uvicorn jinja2 python-dotenv

# 4. 파일 생성
# - main.py (위의 FastAPI 코드 복사)
# - config.py (설정 파일)
# - templates/donation.html (HTML 템플릿)
# - static/images/toss-qr.png (QR 코드 이미지)

# 5. 서버 실행
uvicorn main:app --reload

# 6. 브라우저 접속
# http://localhost:8000/donation
```

---

## 💡 참고 링크

- **토스 페이먼츠 개발자 센터**: https://docs.tosspayments.com/
- **토스 딥링크 가이드**: https://toss.im/deep-link
- **FastAPI 공식 문서**: https://fastapi.tiangolo.com/
- **Flask 공식 문서**: https://flask.palletsprojects.com/
- **Django 공식 문서**: https://www.djangoproject.com/

---

**작성자**: AI ON
**마지막 업데이트**: 2025-10-29
