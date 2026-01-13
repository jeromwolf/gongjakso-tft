'use client';

export interface DonationConfig {
  accountNumber: string;
  bankName: string;
  tossDeepLink?: string; // Optional: Toss deep link (if available)
}

export interface DonationButtonProps {
  config: DonationConfig;
  label?: string;
  className?: string;
}

/**
 * 재사용 가능한 후원 버튼 컴포넌트
 *
 * @example
 * ```tsx
 * <DonationButton
 *   config={{
 *     accountNumber: '100039997509',
 *     bankName: '토스뱅크',
 *     tossDeepLink: 'supertoss://send?amount=0&bank=%ED%86%A0%EC%8A%A4%EB%B1%85%ED%81%AC&accountNo=100039997509&origin=qr'
 *   }}
 * />
 * ```
 */
export default function DonationButton({
  config,
  label = '💝 토스로 후원하기',
  className = ''
}: DonationButtonProps) {
  const handleDonation = () => {
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    const displayAccount = `${config.bankName} ${config.accountNumber}`;

    if (isMobile && config.tossDeepLink) {
      // 모바일: 토스 앱 열기
      window.location.href = config.tossDeepLink;
    } else {
      // PC: 계좌번호 복사 및 안내
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(displayAccount).then(() => {
          alert(`📋 계좌번호가 복사되었습니다!\n\n${displayAccount}\n\n토스 앱이나 은행 앱에서 붙여넣기 해주세요 😊`);
        }).catch(() => {
          alert(`💝 후원 계좌번호\n\n${displayAccount}\n\n토스 앱이나 은행 앱에서 송금해주세요!`);
        });
      } else {
        alert(`💝 후원 계좌번호\n\n${displayAccount}\n\n토스 앱이나 은행 앱에서 송금해주세요!`);
      }
    }
  };

  return (
    <button
      onClick={handleDonation}
      className={`px-8 py-4 bg-blue-600 hover:bg-blue-700 rounded-xl font-bold transition text-white text-lg shadow-lg hover:shadow-xl cursor-pointer ${className}`}
    >
      {label}
    </button>
  );
}
