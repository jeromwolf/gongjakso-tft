'use client';

export default function CoffeeSupport() {
  const handleTossDonation = () => {
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    const tossUrl = 'supertoss://send?amount=0&bank=%ED%86%A0%EC%8A%A4%EB%B1%85%ED%81%AC&accountNo=100039997509&origin=qr';
    const accountNumber = '토스뱅크 100039997509';

    if (isMobile) {
      // 모바일: 토스 앱 열기
      window.location.href = tossUrl;
    } else {
      // PC: 계좌번호 복사 및 안내
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(accountNumber).then(() => {
          alert('📋 계좌번호가 복사되었습니다!\n\n' + accountNumber + '\n\n토스 앱이나 은행 앱에서 붙여넣기 해주세요 😊');
        }).catch(() => {
          alert('💝 후원 계좌번호\n\n' + accountNumber + '\n\n토스 앱이나 은행 앱에서 송금해주세요!');
        });
      } else {
        alert('💝 후원 계좌번호\n\n' + accountNumber + '\n\n토스 앱이나 은행 앱에서 송금해주세요!');
      }
    }
  };

  return (
    <section className="mb-24">
      {/* Header with emotional message */}
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold mb-4 text-white">☕ 커피 한 잔의 후원</h2>
        <p className="text-lg text-gray-300 max-w-3xl mx-auto leading-relaxed mb-2">
          우리는 오픈소스와 기술 공유를 통해 더 나은 개발 생태계를 만들어가고 있습니다.
        </p>
        <p className="text-gray-400 max-w-3xl mx-auto">
          Claude Code, GitHub Copilot 등 AI 도구의 정액제 비용을 후원해 주시면,<br />
          더 많은 프로젝트를 개발하고 소스를 공개할 수 있습니다. 💜
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

            {/* Amount options - Larger cards */}
            <div className="space-y-3 mb-6">
              <div className="flex items-center gap-3 p-3 bg-gray-700/30 border border-gray-600 rounded-lg hover:border-gray-500 transition">
                <span className="text-2xl">☕</span>
                <div>
                  <p className="text-white font-medium">₩5,000 커피 한 잔</p>
                  <p className="text-xs text-gray-400">AI 도구 1일 사용료</p>
                </div>
              </div>

              <div className="flex items-center gap-3 p-3 bg-blue-600/20 border-2 border-blue-500 rounded-lg hover:bg-blue-600/30 transition">
                <span className="text-2xl">⭐</span>
                <div>
                  <p className="text-white font-medium">₩20,000 AI 도구 지원</p>
                  <p className="text-xs text-blue-300">추천! 월간 구독료</p>
                </div>
              </div>

              <div className="flex items-center gap-3 p-3 bg-gray-700/30 border border-gray-600 rounded-lg hover:border-gray-500 transition">
                <span className="text-2xl">💝</span>
                <div>
                  <p className="text-white font-medium">자유 금액</p>
                  <p className="text-xs text-gray-400">원하시는 만큼 후원</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right: QR Code + Button */}
          <div className="flex flex-col items-center justify-center">
            <button
              onClick={handleTossDonation}
              className="w-full px-8 py-4 bg-blue-600 hover:bg-blue-700 rounded-xl font-bold transition text-white text-lg mb-6 text-center shadow-lg hover:shadow-xl cursor-pointer"
            >
              💝 토스로 후원하기
            </button>

            <div className="bg-white p-5 rounded-xl shadow-lg">
              <img
                src="/toss-qr.png"
                alt="토스 후원 QR 코드"
                className="w-40 h-40 object-contain"
              />
            </div>
            <p className="text-sm text-gray-400 mt-4">📱 또는 QR 코드를 스캔하세요</p>
          </div>
        </div>
      </div>

      {/* Bottom: Detailed usage section */}
      <div className="mt-8 bg-gray-800/20 border border-gray-700 rounded-xl p-8">
        <h3 className="text-xl font-bold text-white mb-6 text-center">💡 후원금은 이렇게 사용됩니다</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-4xl mb-3">🤖</div>
            <h4 className="text-white font-semibold mb-2">Claude Code, GitHub Copilot 등 AI 개발 도구 구독료</h4>
            <p className="text-sm text-gray-400">최신 AI 도구로 더 빠르고 효율적인 개발</p>
          </div>

          <div className="text-center">
            <div className="text-4xl mb-3">💻</div>
            <h4 className="text-white font-semibold mb-2">더 많은 오픈소스 프로젝트 개발 및 유지보수</h4>
            <p className="text-sm text-gray-400">유용한 도구를 만들어 커뮤니티와 공유</p>
          </div>

          <div className="text-center">
            <div className="text-4xl mb-3">💾</div>
            <h4 className="text-white font-semibold mb-2">서버 호스팅 및 인프라 운영 비용</h4>
            <p className="text-sm text-gray-400">안정적인 서비스 제공</p>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-700 text-center">
          <div className="text-center">
            <div className="text-4xl mb-3">🎓</div>
            <h4 className="text-white font-semibold mb-2">기술 문서화 및 튜토리얼 제작</h4>
            <p className="text-sm text-gray-400">누구나 쉽게 배울 수 있는 콘텐츠 제공</p>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-700 text-center">
          <div className="text-center">
            <div className="text-4xl mb-3">💙</div>
            <h4 className="text-white font-semibold mb-2">커뮤니티와 함께 성장하는 개발 생태계 조성</h4>
            <p className="text-sm text-gray-400">여러분의 후원이 더 나은 세상을 만듭니다</p>
          </div>
        </div>
      </div>
    </section>
  );
}
