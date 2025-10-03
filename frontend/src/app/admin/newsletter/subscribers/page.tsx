'use client';

import { useEffect } from 'react';
import { useAuth } from '@/contexts/auth-context';
import { useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { newsletterAPI } from '@/lib/api';
import { formatDistanceToNow } from 'date-fns';
import { ko } from 'date-fns/locale';

export default function SubscribersPage() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'admin')) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  const { data, isLoading } = useQuery({
    queryKey: ['newsletter-subscribers'],
    queryFn: () => newsletterAPI.subscribers({ page_size: 1000 }),
    enabled: !!user && user.role === 'admin',
  });

  if (authLoading || !user) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  const activeSubscribers = data?.items?.filter((s: any) => s.is_active) || [];
  const inactiveSubscribers = data?.items?.filter((s: any) => !s.is_active) || [];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/admin/newsletter" className="text-blue-400 hover:text-blue-300 text-sm mb-2 inline-block">
            ← 뉴스레터 관리로
          </Link>
          <h1 className="text-4xl font-bold">👥 구독자 목록</h1>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <p className="text-sm text-gray-400">전체 구독자</p>
            <p className="text-2xl font-bold">{data?.total || 0}</p>
          </div>
          <div className="bg-green-900/20 border border-green-700 rounded-lg p-4">
            <p className="text-sm text-green-400">활성 구독자</p>
            <p className="text-2xl font-bold text-green-400">{activeSubscribers.length}</p>
          </div>
          <div className="bg-red-900/20 border border-red-700 rounded-lg p-4">
            <p className="text-sm text-red-400">구독 취소</p>
            <p className="text-2xl font-bold text-red-400">{inactiveSubscribers.length}</p>
          </div>
        </div>

        {/* Subscriber List */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto"></div>
          </div>
        ) : data && data.items && data.items.length > 0 ? (
          <div className="space-y-6">
            {/* Active Subscribers */}
            {activeSubscribers.length > 0 && (
              <div>
                <h2 className="text-2xl font-bold mb-4 text-green-400">✅ 활성 구독자 ({activeSubscribers.length})</h2>
                <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-gray-900 border-b border-gray-700">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            이메일
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            구독일
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            상태
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-700">
                        {activeSubscribers.map((subscriber: any) => (
                          <tr key={subscriber.id} className="hover:bg-gray-700/50 transition">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center">
                                <div className="flex-shrink-0 h-8 w-8 bg-green-600 rounded-full flex items-center justify-center">
                                  <span className="text-xs font-bold">
                                    {subscriber.email.charAt(0).toUpperCase()}
                                  </span>
                                </div>
                                <div className="ml-3">
                                  <div className="text-sm font-medium">{subscriber.email}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-300">
                                {formatDistanceToNow(new Date(subscriber.created_at), {
                                  addSuffix: true,
                                  locale: ko,
                                })}
                              </div>
                              <div className="text-xs text-gray-500">
                                {new Date(subscriber.created_at).toLocaleDateString('ko-KR')}
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-900 text-green-300">
                                활성
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}

            {/* Inactive Subscribers */}
            {inactiveSubscribers.length > 0 && (
              <div>
                <h2 className="text-2xl font-bold mb-4 text-red-400">❌ 구독 취소 ({inactiveSubscribers.length})</h2>
                <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-gray-900 border-b border-gray-700">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            이메일
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            구독일
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            취소일
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            상태
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-700">
                        {inactiveSubscribers.map((subscriber: any) => (
                          <tr key={subscriber.id} className="hover:bg-gray-700/50 transition opacity-60">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center">
                                <div className="flex-shrink-0 h-8 w-8 bg-red-600 rounded-full flex items-center justify-center">
                                  <span className="text-xs font-bold">
                                    {subscriber.email.charAt(0).toUpperCase()}
                                  </span>
                                </div>
                                <div className="ml-3">
                                  <div className="text-sm font-medium line-through">{subscriber.email}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-400">
                                {formatDistanceToNow(new Date(subscriber.created_at), {
                                  addSuffix: true,
                                  locale: ko,
                                })}
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              {subscriber.unsubscribed_at ? (
                                <div className="text-sm text-gray-400">
                                  {formatDistanceToNow(new Date(subscriber.unsubscribed_at), {
                                    addSuffix: true,
                                    locale: ko,
                                  })}
                                </div>
                              ) : (
                                <span className="text-gray-500 text-sm">-</span>
                              )}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-900 text-red-300">
                                취소
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-400">
            아직 구독자가 없습니다.
          </div>
        )}
      </div>
    </div>
  );
}
