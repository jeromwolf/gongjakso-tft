'use client';

import Link from 'next/link';

// 임시 뉴스 데이터 (나중에 API 연동)
const PLACEHOLDER_NEWS = [
  {
    id: 1,
    title: 'OpenAI Launches GPT-5 with Advanced Reasoning',
    source: 'TechCrunch',
    summary: 'OpenAI announces GPT-5 with significantly improved reasoning and problem-solving capabilities.',
    url: '#',
    publishedAt: '2시간 전',
  },
  {
    id: 2,
    title: 'Google Gemini Enterprise Expands AI Workplace Tools',
    source: 'The Verge',
    summary: 'Google ramps up its AI in the workplace ambitions with new Gemini Enterprise features.',
    url: '#',
    publishedAt: '4시간 전',
  },
  {
    id: 3,
    title: 'Meta Releases Llama 3.5 Open Source Model',
    source: 'TechCrunch',
    summary: 'Meta continues its open-source AI push with the release of Llama 3.5, competing with GPT-4.',
    url: '#',
    publishedAt: '6시간 전',
  },
  {
    id: 4,
    title: 'Tesla AI Day Reveals New Autopilot Features',
    source: 'The Verge',
    summary: 'Tesla showcases next-generation AI capabilities at annual AI Day event.',
    url: '#',
    publishedAt: '8시간 전',
  },
];

export default function NewsSection() {
  return (
    <section>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white">📰 IT 뉴스</h2>
          <p className="text-sm text-gray-400 mt-1">최신 기술 뉴스</p>
        </div>
        <Link
          href="/news"
          className="text-sm text-blue-400 hover:text-blue-300 transition flex items-center gap-1"
        >
          전체보기
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>

      <div className="space-y-4">
        {PLACEHOLDER_NEWS.map((news) => (
          <article
            key={news.id}
            className="bg-gray-800/30 border border-gray-700 rounded-lg p-4 hover:border-gray-600 transition group"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1">
                <h3 className="font-semibold text-white group-hover:text-blue-400 transition mb-2">
                  <a href={news.url} className="hover:underline">
                    {news.title}
                  </a>
                </h3>
                <p className="text-sm text-gray-400 mb-3">{news.summary}</p>
                <div className="flex items-center gap-3 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                      <path
                        fillRule="evenodd"
                        d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z"
                        clipRule="evenodd"
                      />
                    </svg>
                    {news.source}
                  </span>
                  <span>•</span>
                  <span className="flex items-center gap-1">
                    <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                        clipRule="evenodd"
                      />
                    </svg>
                    {news.publishedAt}
                  </span>
                </div>
              </div>
            </div>
          </article>
        ))}
      </div>

      <div className="mt-6 text-center">
        <p className="text-xs text-gray-500">
          💡 뉴스는 IT News Flux에서 자동으로 선택됩니다
        </p>
      </div>
    </section>
  );
}
