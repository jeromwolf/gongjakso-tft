'use client';

import Image from 'next/image';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { useEffect, useState } from 'react';
import { activityAPI } from '@/lib/api';
import type { ActivityListItem } from '@/lib/types';

export default function ActivityPage() {
  const [activities, setActivities] = useState<ActivityListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadActivities();
  }, []);

  const loadActivities = async () => {
    try {
      setLoading(true);
      const response = await activityAPI.list({ page: 1, page_size: 50 });
      setActivities(response.items);
    } catch (err: any) {
      console.error('Failed to load activities:', err);
      setError(err.response?.data?.detail || 'Failed to load activities');
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-16">
        {/* 헤더 */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold mb-4">📸 활동</h1>
          <p className="text-gray-400 text-lg">AI ON 팀의 스터디, 세미나, 프로젝트 활동을 기록합니다</p>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-20">
            <div className="text-gray-400">Loading activities...</div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-6 text-center">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {/* 활동 타임라인 */}
        {!loading && !error && activities.length > 0 && (
          <div className="space-y-8">
            {activities.map((activity, index) => (
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
                      {format(new Date(activity.activity_date), 'yyyy년 MM월 dd일', { locale: ko })}
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

                  {/* 메타 정보 */}
                  <div className="flex items-center gap-6 text-sm text-gray-500 pt-4">
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
        )}

        {/* Empty State */}
        {!loading && !error && activities.length === 0 && (
          <div className="mt-12 text-center">
            <div className="inline-block bg-gray-800/30 border border-gray-700 rounded-lg p-8">
              <p className="text-gray-400 mb-2">✨ 활동이 아직 등록되지 않았습니다</p>
              <p className="text-sm text-gray-500">스터디, 세미나, 프로젝트 활동을 계속 기록해나갈 예정입니다</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
