import Link from 'next/link';

export default function Features() {
  const features = [
    {
      href: '/projects',
      title: 'Projects',
      subtitle: '프로젝트',
      description: '혁신적인 데이터 솔루션',
    },
    {
      href: '/blog',
      title: 'Blog',
      subtitle: '블로그',
      description: '최신 개발 소식과 기술 트렌드',
    },
    {
      href: null,
      title: 'Newsletter',
      subtitle: '뉴스레터',
      description: '매주 엄선된 기술 정보',
    },
  ];

  return (
    <div className="grid md:grid-cols-3 gap-6 mb-24">
      {features.map((feature, index) => {
        const className = `group bg-gray-800/30 hover:bg-gray-800/50 border border-gray-700 hover:border-gray-600 rounded-xl p-8 transition-all ${feature.href ? 'cursor-pointer' : ''}`;

        const content = (
          <>
            <h3 className="text-3xl font-bold mb-2 text-white group-hover:text-blue-400 transition">
              {feature.title}
            </h3>
            <p className="text-sm text-gray-500 mb-4">{feature.subtitle}</p>
            <p className="text-gray-400 text-sm">{feature.description}</p>
          </>
        );

        return feature.href ? (
          <Link key={index} href={feature.href} className={className}>
            {content}
          </Link>
        ) : (
          <div key={index} className={className}>
            {content}
          </div>
        );
      })}
    </div>
  );
}
