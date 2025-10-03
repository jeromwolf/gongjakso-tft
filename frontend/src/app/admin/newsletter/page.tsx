'use client';

import { useEffect } from 'react';
import { useAuth } from '@/contexts/auth-context';
import { useRouter } from 'next/navigation';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { newsletterAPI } from '@/lib/api';
import { formatDistanceToNow } from 'date-fns';
import { ko } from 'date-fns/locale';

export default function AdminNewsletterListPage() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const queryClient = useQueryClient();

  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'admin')) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  const { data, isLoading } = useQuery({
    queryKey: ['newsletters-admin'],
    queryFn: () => newsletterAPI.list({ page_size: 100 }),
    enabled: !!user && user.role === 'admin',
  });

  const sendMutation = useMutation({
    mutationFn: (id: number) => newsletterAPI.send(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['newsletters-admin'] });
      alert('뉴스레터가 발송되었습니다!');
    },
    onError: (error: any) => {
      alert(error.response?.data?.detail || '발송에 실패했습니다.');
    },
  });

  const handleSend = (id: number, title: string) => {
    if (confirm(`"${title}" 뉴스레터를 모든 구독자에게 발송하시겠습니까?`)) {
      sendMutation.mutate(id);
    }
  };

  if (authLoading || !user) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <Link href="/admin" className="text-blue-400 hover:text-blue-300 text-sm mb-2 inline-block">
              ← 대시보드로
            </Link>
            <h1 className="text-4xl font-bold">📧 뉴스레터 관리</h1>
          </div>
          <div className="flex gap-3">
            <Link
              href="/admin/newsletter/subscribers"
              className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold transition"
            >
              👥 구독자 목록
            </Link>
            <Link
              href="/admin/newsletter/new"
              className="px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-semibold transition"
            >
              ✍️ 새 뉴스레터 작성
            </Link>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <p className="text-sm text-gray-400">전체</p>
            <p className="text-2xl font-bold">{data?.total || 0}</p>
          </div>
          <div className="bg-green-900/20 border border-green-700 rounded-lg p-4">
            <p className="text-sm text-green-400">발송됨</p>
            <p className="text-2xl font-bold text-green-400">
              {data?.items?.filter((n: any) => n.status === 'sent').length || 0}
            </p>
          </div>
          <div className="bg-yellow-900/20 border border-yellow-700 rounded-lg p-4">
            <p className="text-sm text-yellow-400">초안</p>
            <p className="text-2xl font-bold text-yellow-400">
              {data?.items?.filter((n: any) => n.status === 'draft').length || 0}
            </p>
          </div>
        </div>

        {/* Newsletter List */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto"></div>
          </div>
        ) : data && data.items && data.items.length > 0 ? (
          <div className="space-y-4">
            {data.items.map((newsletter: any) => (
              <div
                key={newsletter.id}
                className="bg-gray-800 border border-gray-700 rounded-lg p-6 hover:border-green-500 transition"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h2 className="text-xl font-bold">{newsletter.title}</h2>
                      <span
                        className={`px-3 py-1 text-xs rounded-full ${
                          newsletter.status === 'sent'
                            ? 'bg-green-900 text-green-300'
                            : newsletter.status === 'scheduled'
                            ? 'bg-blue-900 text-blue-300'
                            : 'bg-yellow-900 text-yellow-300'
                        }`}
                      >
                        {newsletter.status === 'sent' ? '발송됨' : newsletter.status === 'scheduled' ? '예약됨' : '초안'}
                      </span>
                    </div>

                    <div className="flex items-center gap-4 text-sm text-gray-400 mb-3">
                      <span>📧 {newsletter.sent_count || 0}명 발송</span>
                      {newsletter.sent_at && (
                        <>
                          <span>•</span>
                          <span>
                            발송일: {formatDistanceToNow(new Date(newsletter.sent_at), {
                              addSuffix: true,
                              locale: ko,
                            })}
                          </span>
                        </>
                      )}
                      <span>•</span>
                      <span>
                        생성일: {formatDistanceToNow(new Date(newsletter.created_at), {
                          addSuffix: true,
                          locale: ko,
                        })}
                      </span>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Link
                      href={`/admin/newsletter/${newsletter.id}`}
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition"
                    >
                      보기
                    </Link>
                    {newsletter.status === 'draft' && (
                      <button
                        onClick={() => handleSend(newsletter.id, newsletter.title)}
                        className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg text-sm transition"
                        disabled={sendMutation.isPending}
                      >
                        {sendMutation.isPending ? '발송 중...' : '발송'}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-400">
            아직 뉴스레터가 없습니다.
          </div>
        )}
      </div>
    </div>
  );
}
