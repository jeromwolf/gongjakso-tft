export default function UseCases() {
  const useCases = [
    {
      title: 'Development',
      subtitle: '개발 생산성',
      description: 'AI 도구와 자동화로 반복 작업 최소화',
    },
    {
      title: 'Analysis',
      subtitle: '데이터 분석',
      description: '실시간 데이터 기반 의사결정',
    },
    {
      title: 'Trading',
      subtitle: '투자 전략',
      description: '백테스팅으로 리스크 검증',
    },
    {
      title: 'Content',
      subtitle: '콘텐츠 제작',
      description: '비디오 편집 자동화',
    },
  ];

  return (
    <section className="mb-24">
      <div className="text-center mb-12">
        <h2 className="text-2xl font-bold mb-3 text-white">Use Cases</h2>
        <p className="text-gray-400 text-sm">실제 프로젝트 활용 예시</p>
      </div>
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
        {useCases.map((useCase, index) => (
          <div
            key={index}
            className="bg-gray-800/30 hover:bg-gray-800/50 border border-gray-700 hover:border-gray-600 p-6 rounded-xl transition-all"
          >
            <h3 className="text-lg font-bold mb-1 text-white">{useCase.title}</h3>
            <p className="text-xs text-gray-500 mb-3">{useCase.subtitle}</p>
            <p className="text-gray-400 text-xs leading-relaxed">{useCase.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
