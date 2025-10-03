export default function ValuePropositions() {
  const values = [
    {
      icon: '💡',
      bgColor: 'bg-blue-500',
      title: '혁신적 사고',
      description: '최신 기술로 독창적인 솔루션 개발',
    },
    {
      icon: '👥',
      bgColor: 'bg-teal-500',
      title: '협업 중심',
      description: '지식 공유로 더 나은 결과 창출',
    },
    {
      icon: '🚀',
      bgColor: 'bg-orange-500',
      title: '빠른 실행력',
      description: '아이디어를 빠르게 실용화',
    },
  ];

  return (
    <div className="grid md:grid-cols-3 gap-8 mb-20">
      {values.map((value, index) => (
        <div key={index} className="text-center">
          <div className={`w-20 h-20 ${value.bgColor} rounded-full flex items-center justify-center mx-auto mb-4`}>
            <span className="text-4xl">{value.icon}</span>
          </div>
          <h3 className="text-xl font-bold mb-2">{value.title}</h3>
          <p className="text-gray-400 text-sm">{value.description}</p>
        </div>
      ))}
    </div>
  );
}
