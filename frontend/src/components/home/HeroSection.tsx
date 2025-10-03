export default function HeroSection() {
  return (
    <header className="text-center mb-24">
      {/* Main Title */}
      <div className="mb-8">
        <h1 className="text-5xl md:text-7xl font-bold mb-4 text-white leading-tight">
          혁신적인 솔루션을<br />
          창조합니다
        </h1>
        <div className="w-24 h-1 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto rounded-full"></div>
      </div>

      {/* Subtitle */}
      <p className="text-xl md:text-2xl text-gray-300 font-medium mb-6 max-w-4xl mx-auto leading-relaxed">
        데이터공작소 개발 TFT가 만든 최첨단 도구와 플랫폼으로<br className="hidden md:block" />
        여러분의 작업을 더욱 효율적으로 만들어보세요
      </p>

      {/* Description */}
      <p className="text-base text-gray-400 max-w-2xl mx-auto">
        혁신적인 기술과 창의적인 아이디어로 실용적인 솔루션을 만들어가는 개발팀
      </p>
    </header>
  );
}
