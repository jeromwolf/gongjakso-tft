'use client';

import Image from 'next/image';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';

// 활동 데이터 (샘플)
const ACTIVITIES = [
  {
    id: 1,
    title: 'AI ON 팀 킥오프 미팅',
    date: new Date('2025-10-13'),
    type: 'meeting',
    description: `AI ON 프로젝트의 첫 번째 팀 미팅을 진행했습니다.

프로젝트 목표와 방향성을 논의하고, 각 팀원의 역할을 분담했습니다. AI 기술 스터디와 바이브코딩 프로젝트를 결합한 새로운 플랫폼 구축을 위한 첫 걸음을 내딛었습니다.

주요 논의 사항:
- AI ON 브랜딩 및 컨셉 정립
- 홈페이지 구조 및 기능 기획
- IT News Flux 연동 계획
- 블로그 및 프로젝트 콘텐츠 전략`,
    images: ['/team-meeting-1.jpg'],
    participants: 7,
    location: '서울',
  },
];

export default function ActivityPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-16">
        {/* 헤더 */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold mb-4">📸 활동</h1>
          <p className="text-gray-400 text-lg">AI ON 팀의 스터디, 세미나, 프로젝트 활동을 기록합니다</p>
        </div>

        {/* 활동 타임라인 */}
        <div className="space-y-8">
          {ACTIVITIES.map((activity, index) => (
            <article
              key={activity.id}
              className="bg-gray-800/30 border border-gray-700 rounded-xl overflow-hidden hover:border-gray-600 transition"
            >
              {/* 이미지 갤러리 */}
              {activity.images && activity.images.length > 0 && (
                <div className="relative w-full h-[400px] bg-gray-800">
                  <Image
                    src={activity.images[0]}
                    alt={activity.title}
                    fill
                    className="object-cover"
                    priority={index === 0}
                  />
                </div>
              )}

              {/* 활동 정보 */}
              <div className="p-8">
                {/* 날짜 & 타입 */}
                <div className="flex items-center gap-4 mb-4">
                  <span className="flex items-center gap-2 text-sm text-blue-400">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                        clipRule="evenodd"
                      />
                    </svg>
                    {format(activity.date, 'yyyy년 MM월 dd일', { locale: ko })}
                  </span>
                  <span className="px-3 py-1 bg-purple-500/10 text-purple-400 text-xs rounded-full border border-purple-500/20">
                    {activity.type === 'meeting'
                      ? '🤝 미팅'
                      : activity.type === 'seminar'
                      ? '📚 세미나'
                      : activity.type === 'study'
                      ? '💡 스터디'
                      : '🎯 프로젝트'}
                  </span>
                </div>

                {/* 제목 */}
                <h2 className="text-2xl font-bold text-white mb-4">{activity.title}</h2>

                {/* 설명 */}
                <div className="text-gray-400 text-sm leading-relaxed mb-6 whitespace-pre-line">
                  {activity.description}
                </div>

                {/* 메타 정보 */}
                <div className="flex items-center gap-6 text-sm text-gray-500 pt-4 border-t border-gray-700">
                  {activity.participants && (
                    <span className="flex items-center gap-2">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
                      </svg>
                      {activity.participants}명 참여
                    </span>
                  )}
                  {activity.location && (
                    <span className="flex items-center gap-2">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fillRule="evenodd"
                          d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                          clipRule="evenodd"
                        />
                      </svg>
                      {activity.location}
                    </span>
                  )}
                </div>
              </div>
            </article>
          ))}
        </div>

        {/* 더 많은 활동 예정 */}
        <div className="mt-12 text-center">
          <div className="inline-block bg-gray-800/30 border border-gray-700 rounded-lg p-8">
            <p className="text-gray-400 mb-2">✨ 더 많은 활동이 곧 추가됩니다</p>
            <p className="text-sm text-gray-500">스터디, 세미나, 프로젝트 활동을 계속 기록해나갈 예정입니다</p>
          </div>
        </div>
      </div>
    </div>
  );
}
