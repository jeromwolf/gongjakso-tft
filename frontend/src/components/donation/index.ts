/**
 * 재사용 가능한 후원 컴포넌트
 *
 * 다른 프로젝트에서 사용하는 방법:
 * 1. donation 폴더 전체 복사
 * 2. public/toss-qr.png 복사 (선택사항)
 * 3. 컴포넌트 import 후 사용
 */

export { default as DonationButton } from './DonationButton';
export { default as DonationSection } from './DonationSection';

export type { DonationConfig } from './DonationButton';
export type { DonationAmount, DonationUsage, DonationSectionProps } from './DonationSection';
