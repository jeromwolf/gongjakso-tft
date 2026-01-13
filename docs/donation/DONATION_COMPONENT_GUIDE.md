# 🎁 재사용 가능한 후원 컴포넌트 가이드

## 📦 컴포넌트 구성

```
frontend/src/components/donation/
├── DonationButton.tsx      # 간단한 후원 버튼
├── DonationSection.tsx     # 전체 후원 섹션 (추천)
└── index.ts                # Export 파일
```

---

## 🚀 다른 프로젝트에서 사용하기

### 1️⃣ 파일 복사

```bash
# donation 컴포넌트 폴더 복사
cp -r frontend/src/components/donation <your-project>/src/components/

# QR 코드 이미지 복사 (선택사항)
cp frontend/public/toss-qr.png <your-project>/public/
```

### 2️⃣ 간단한 사용법 (버튼만)

```tsx
import { DonationButton } from '@/components/donation';

export default function MyPage() {
  return (
    <DonationButton
      config={{
        accountNumber: '100039997509',
        bankName: '토스뱅크',
        tossDeepLink: 'supertoss://send?amount=0&bank=%ED%86%A0%EC%8A%A4%EB%B1%85%ED%81%AC&accountNo=100039997509&origin=qr'
      }}
      label="💝 후원하기"
    />
  );
}
```

### 3️⃣ 전체 섹션 사용 (추천)

```tsx
import { DonationSection } from '@/components/donation';

export default function HomePage() {
  return (
    <DonationSection
      config={{
        accountNumber: '100039997509',
        bankName: '토스뱅크',
        tossDeepLink: 'supertoss://send?amount=0&bank=%ED%86%A0%EC%8A%A4%EB%B1%85%ED%81%AC&accountNo=100039997509&origin=qr'
      }}
      title="☕ 커피 한 잔의 후원"
      qrCodeUrl="/toss-qr.png"
    />
  );
}
```

---

## 🎨 커스터마이징

### 후원 금액 옵션 변경

```tsx
<DonationSection
  config={{...}}
  amounts={[
    {
      emoji: '☕',
      amount: 3000,
      label: '₩3,000 커피 한 잔',
      description: '감사합니다!',
    },
    {
      emoji: '🍕',
      amount: 10000,
      label: '₩10,000 피자 한 판',
      description: '든든한 지원',
      highlight: true, // 파란색 강조
    },
    {
      emoji: '💝',
      amount: 0,
      label: '자유 금액',
      description: '원하시는 만큼',
    },
  ]}
/>
```

### 후원금 사용처 변경

```tsx
<DonationSection
  config={{...}}
  usages={[
    {
      emoji: '🖥️',
      title: '서버 운영 비용',
      description: 'AWS, Vercel 등 호스팅 비용',
    },
    {
      emoji: '📚',
      title: '교육 콘텐츠 제작',
      description: '무료 강의 영상 제작',
    },
    {
      emoji: '🌱',
      title: '오픈소스 기여',
      description: '커뮤니티 발전에 기여',
    },
  ]}
/>
```

### 제목 및 설명 변경

```tsx
<DonationSection
  config={{...}}
  title="🎉 프로젝트 후원하기"
  subtitle="여러분의 후원이 프로젝트를 살립니다!"
  description="후원금은 서버 비용과 개발에 사용됩니다."
/>
```

---

## 🔧 Props 레퍼런스

### DonationButton Props

| Prop | 타입 | 필수 | 설명 |
|------|------|------|------|
| `config` | `DonationConfig` | ✅ | 계좌 정보 |
| `label` | `string` | ❌ | 버튼 텍스트 (기본값: '💝 토스로 후원하기') |
| `className` | `string` | ❌ | 추가 CSS 클래스 |

### DonationConfig 타입

```typescript
interface DonationConfig {
  accountNumber: string;    // 계좌번호 (예: '100039997509')
  bankName: string;         // 은행명 (예: '토스뱅크')
  tossDeepLink?: string;    // 토스 딥링크 (선택사항)
}
```

### DonationSection Props

| Prop | 타입 | 필수 | 설명 |
|------|------|------|------|
| `config` | `DonationConfig` | ✅ | 계좌 정보 |
| `title` | `string` | ❌ | 섹션 제목 |
| `subtitle` | `string` | ❌ | 부제목 |
| `description` | `string` | ❌ | 설명 텍스트 |
| `amounts` | `DonationAmount[]` | ❌ | 후원 금액 옵션 |
| `qrCodeUrl` | `string` | ❌ | QR 코드 이미지 경로 |
| `usages` | `DonationUsage[]` | ❌ | 후원금 사용처 |
| `className` | `string` | ❌ | 추가 CSS 클래스 |

---

## 🎯 사용 예시

### 예시 1: 미니멀 버튼

```tsx
import { DonationButton } from '@/components/donation';

export default function Sidebar() {
  return (
    <aside>
      <DonationButton
        config={{
          accountNumber: '1002-123-456789',
          bankName: '우리은행',
        }}
        label="후원하기"
        className="w-full"
      />
    </aside>
  );
}
```

### 예시 2: QR 코드 없이 사용

```tsx
import { DonationSection } from '@/components/donation';

export default function DonatePage() {
  return (
    <DonationSection
      config={{
        accountNumber: '100039997509',
        bankName: '토스뱅크',
      }}
      // qrCodeUrl을 제공하지 않으면 QR 코드 섹션이 표시되지 않음
    />
  );
}
```

### 예시 3: 완전 커스텀

```tsx
import { DonationSection } from '@/components/donation';

export default function SupportPage() {
  return (
    <DonationSection
      config={{
        accountNumber: '100039997509',
        bankName: '토스뱅크',
        tossDeepLink: 'supertoss://send?amount=5000&bank=토스뱅크&accountNo=100039997509',
      }}
      title="🎸 뮤지션 후원하기"
      subtitle="음악 활동을 응원해주세요!"
      description="후원금은 새로운 곡 제작과 공연에 사용됩니다."
      amounts={[
        {
          emoji: '🎵',
          amount: 5000,
          label: '₩5,000 한 곡',
          description: '새로운 싱글 제작',
        },
        {
          emoji: '🎤',
          amount: 20000,
          label: '₩20,000 공연 지원',
          description: '라이브 공연 준비',
          highlight: true,
        },
        {
          emoji: '💿',
          amount: 50000,
          label: '₩50,000 앨범 제작',
          description: '정규 앨범 제작 후원',
        },
      ]}
      qrCodeUrl="/support-qr.png"
      usages={[
        {
          emoji: '🎹',
          title: '악기 및 장비 구입',
          description: '더 좋은 음악을 위한 투자',
        },
        {
          emoji: '🎬',
          title: '뮤직비디오 제작',
          description: '고품질 비주얼 콘텐츠',
        },
        {
          emoji: '🎪',
          title: '공연 및 투어',
          description: '팬 여러분과 만나는 시간',
        },
      ]}
    />
  );
}
```

---

## 🛠️ 토스 딥링크 생성 방법

### 토스 송금 URL 형식

```
supertoss://send?amount=0&bank=<은행명>&accountNo=<계좌번호>&origin=qr
```

### 예시

```typescript
const tossDeepLink = encodeURI('supertoss://send?amount=0&bank=토스뱅크&accountNo=100039997509&origin=qr');
// 결과: supertoss://send?amount=0&bank=%ED%86%A0%EC%8A%A4%EB%B1%85%ED%81%AC&accountNo=100039997509&origin=qr
```

### QR 코드 생성

1. https://www.qr-code-generator.com/ 접속
2. URL 타입 선택
3. 토스 딥링크 입력
4. QR 코드 다운로드

---

## 📱 동작 방식

### 모바일 환경
- 토스 딥링크 실행 → 토스 앱 자동 실행
- 계좌번호/금액 자동 입력

### PC 환경
- 계좌번호 자동 복사
- Alert로 안내 메시지 표시
- 사용자가 은행 앱에서 직접 송금

---

## 🎨 스타일 커스터마이징

### Tailwind CSS 클래스 변경

```tsx
<DonationSection
  config={{...}}
  className="my-custom-styles"
/>
```

### 버튼 색상 변경

```tsx
<DonationButton
  config={{...}}
  className="bg-green-600 hover:bg-green-700"
/>
```

---

## 📋 체크리스트

다른 프로젝트에 적용하기 전 확인사항:

- [ ] `donation` 폴더 복사 완료
- [ ] 계좌번호 및 은행명 변경
- [ ] QR 코드 이미지 복사 (선택)
- [ ] 제목/설명 텍스트 커스터마이징
- [ ] 후원 금액 옵션 변경
- [ ] 후원금 사용처 변경
- [ ] 모바일/PC 환경에서 테스트

---

## 💡 팁

1. **QR 코드 없이 사용 가능** - `qrCodeUrl` prop을 생략하면 QR 섹션이 표시되지 않음
2. **금액 자동 입력** - 토스 딥링크에 `amount=5000` 추가하면 금액 미리 입력
3. **다국어 지원** - 텍스트를 props로 받기 때문에 다국어 쉽게 적용 가능
4. **반응형 디자인** - 모바일/PC 환경에서 모두 최적화됨

---

## 🆘 문제 해결

### 토스 앱이 안 열려요
- 모바일에서 토스 앱 설치 확인
- 토스 딥링크 형식 확인 (URL 인코딩)

### QR 코드가 안 보여요
- `qrCodeUrl` 경로 확인 (`/public/` 폴더)
- Next.js Image 최적화 설정 확인

### 계좌번호 복사가 안 돼요
- HTTPS 환경에서만 `navigator.clipboard` 작동
- Alert 메시지로 폴백 처리됨

---

## 📄 라이선스

이 컴포넌트는 자유롭게 사용 가능합니다.
출처 표시는 선택사항이지만 감사합니다! 😊

**Created by**: AI ON (https://gongjakso-tft-frontend.onrender.com)
