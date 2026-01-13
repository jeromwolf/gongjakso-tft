'use client';

import DonationButton, { DonationConfig } from './DonationButton';
import Image from 'next/image';

export interface DonationAmount {
  emoji: string;
  amount: number;
  label: string;
  description: string;
  highlight?: boolean;
}

export interface DonationUsage {
  emoji: string;
  title: string;
  description: string;
}

export interface DonationSectionProps {
  config: DonationConfig;
  title?: string;
  subtitle?: string;
  description?: string;
  amounts?: DonationAmount[];
  qrCodeUrl?: string;
  usages?: DonationUsage[];
  className?: string;
}

/**
 * 재사용 가능한 후원 섹션 컴포넌트 (전체 UI)
 *
 * @example
 * ```tsx
 * <DonationSection
 *   config={{
 *     accountNumber: '100039997509',
 *     bankName: '토스뱅크',
 *     tossDeepLink: 'supertoss://send?...'
 *   }}
 *   title="☕ 커피 한 잔의 후원"
 *   qrCodeUrl="/toss-qr.png"
 * />
 * ```
 */
export default function DonationSection({
  config,
  title = '☕ 커피 한 잔의 후원',
  subtitle = '우리는 오픈소스와 기술 공유를 통해 더 나은 개발 생태계를 만들어가고 있습니다.',
  description = 'Claude Code, GitHub Copilot 등 AI 도구의 정액제 비용을 후원해 주시면,\n더 많은 프로젝트를 개발하고 소스를 공개할 수 있습니다. 💜',
  amounts = [
    {
      emoji: '☕',
      amount: 5000,
      label: '₩5,000 커피 한 잔',
      description: 'AI 도구 1일 사용료',
    },
    {
      emoji: '⭐',
      amount: 20000,
      label: '₩20,000 AI 도구 지원',
      description: '추천! 월간 구독료',
      highlight: true,
    },
    {
      emoji: '💝',
      amount: 0,
      label: '자유 금액',
      description: '원하시는 만큼 후원',
    },
  ],
  qrCodeUrl,
  usages = [
    {
      emoji: '🤖',
      title: 'Claude Code, GitHub Copilot 등 AI 개발 도구 구독료',
      description: '최신 AI 도구로 더 빠르고 효율적인 개발',
    },
    {
      emoji: '💻',
      title: '더 많은 오픈소스 프로젝트 개발 및 유지보수',
      description: '유용한 도구를 만들어 커뮤니티와 공유',
    },
    {
      emoji: '💾',
      title: '서버 호스팅 및 인프라 운영 비용',
      description: '안정적인 서비스 제공',
    },
    {
      emoji: '🎓',
      title: '기술 문서화 및 튜토리얼 제작',
      description: '누구나 쉽게 배울 수 있는 콘텐츠 제공',
    },
  ],
  className = '',
}: DonationSectionProps) {
  return (
    <section className={`mb-24 ${className}`}>
      {/* Header with emotional message */}
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold mb-4 text-white">{title}</h2>
        <p className="text-lg text-gray-300 max-w-3xl mx-auto leading-relaxed mb-2">
          {subtitle}
        </p>
        <p className="text-gray-400 max-w-3xl mx-auto whitespace-pre-line">
          {description}
        </p>
      </div>

      <div className="bg-gray-800/30 border border-gray-700 rounded-xl p-8 md:p-10">
        <div className="grid md:grid-cols-2 gap-10">
          {/* Left: Warm message + Amount options */}
          <div>
            <h3 className="text-xl font-bold text-white mb-4">☕ 따뜻한 마음을 담아</h3>
            <p className="text-gray-400 mb-6 leading-relaxed">
              여러분의 후원은 더 나은 오픈소스 프로젝트를 만드는 데 사용됩니다.<br />
              원하시는 금액으로 자유롭게 후원해주세요.
            </p>

            {/* Amount options */}
            <div className="space-y-3 mb-6">
              {amounts.map((amount, index) => (
                <div
                  key={index}
                  className={`flex items-center gap-3 p-3 rounded-lg transition ${
                    amount.highlight
                      ? 'bg-blue-600/20 border-2 border-blue-500 hover:bg-blue-600/30'
                      : 'bg-gray-700/30 border border-gray-600 hover:border-gray-500'
                  }`}
                >
                  <span className="text-2xl">{amount.emoji}</span>
                  <div>
                    <p className="text-white font-medium">{amount.label}</p>
                    <p className={`text-xs ${amount.highlight ? 'text-blue-300' : 'text-gray-400'}`}>
                      {amount.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right: QR Code + Button */}
          <div className="flex flex-col items-center justify-center">
            <DonationButton
              config={config}
              className="w-full mb-6 text-center"
            />

            {qrCodeUrl && (
              <>
                <div className="bg-white p-5 rounded-xl shadow-lg">
                  <Image
                    src={qrCodeUrl}
                    alt="토스 후원 QR 코드"
                    width={160}
                    height={160}
                    className="object-contain"
                  />
                </div>
                <p className="text-sm text-gray-400 mt-4">📱 또는 QR 코드를 스캔하세요</p>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Bottom: Detailed usage section */}
      {usages.length > 0 && (
        <div className="mt-8 bg-gray-800/20 border border-gray-700 rounded-xl p-8">
          <h3 className="text-xl font-bold text-white mb-6 text-center">
            💡 후원금은 이렇게 사용됩니다
          </h3>
          <div className="grid md:grid-cols-3 gap-6">
            {usages.slice(0, 3).map((usage, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl mb-3">{usage.emoji}</div>
                <h4 className="text-white font-semibold mb-2">{usage.title}</h4>
                <p className="text-sm text-gray-400">{usage.description}</p>
              </div>
            ))}
          </div>

          {/* Additional usages (if more than 3) */}
          {usages.slice(3).map((usage, index) => (
            <div key={index + 3} className="mt-8 pt-6 border-t border-gray-700 text-center">
              <div className="text-center">
                <div className="text-4xl mb-3">{usage.emoji}</div>
                <h4 className="text-white font-semibold mb-2">{usage.title}</h4>
                <p className="text-sm text-gray-400">{usage.description}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
