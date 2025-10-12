'use client';

import Link from 'next/link';

// 최신 한글 IT 뉴스 (2025년 10월 기준)
const PLACEHOLDER_NEWS = [
  {
    id: 1,
    title: '넷마블 신작 뱀피르, 출시 8시간 만에 앱스토어 1위 달성',
    source: 'ZDNet Korea',
    summary: '넷마블이 출시한 뱀파이어 테마 MMORPG 뱀피르가 애플 앱스토어에서 출시 8시간 만에 1위를 기록했습니다.',
    url: 'https://zdnet.co.kr/',
    publishedAt: '오늘',
  },
  {
    id: 2,
    title: '통신사 해킹 사고로 국회 과기정통위 '보안' 이슈 집중',
    source: '전자신문',
    summary: 'SK텔레콤, KT, LG유플러스 대표가 증인으로 출석한 가운데 최근 통신 해킹 사건으로 보안이 최대 이슈로 부상했습니다.',
    url: 'https://www.etnews.com/',
    publishedAt: '오늘',
  },
  {
    id: 3,
    title: '한국 AI 스타트업 4곳, CB인사이트 글로벌 AI 100 선정',
    source: 'Forbes Korea',
    summary: '업스테이지, 트웰브랩스, 노타AI 등 한국 스타트업 4곳이 역대 최다로 세계 100대 AI 기업에 선정되었습니다.',
    url: 'https://www.forbeskorea.co.kr/',
    publishedAt: '1일 전',
  },
  {
    id: 4,
    title: 'NC소프트, 서브컬처 게임 리밋 제로 브레이커스 공개',
    source: 'ZDNet Korea',
    summary: 'NC소프트가 신규 서브컬처 게임 리밋 제로 브레이커스 티저 사이트를 오픈하고 본격 홍보에 나섰습니다.',
    url: 'https://zdnet.co.kr/',
    publishedAt: '1일 전',
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
