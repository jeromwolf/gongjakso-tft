'use client';

import { useEffect } from 'react';
import { useAuth } from '@/contexts/auth-context';
import { useRouter, useParams } from 'next/navigation';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { newsletterAPI } from '@/lib/api';
import { formatDistanceToNow } from 'date-fns';
import { ko } from 'date-fns/locale';

export default function NewsletterDetailPage() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const params = useParams();
  const queryClient = useQueryClient();
  const newsletterId = Number(params.id);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'admin')) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  const { data: newsletter, isLoading } = useQuery({
    queryKey: ['newsletter', newsletterId],
    queryFn: () => newsletterAPI.getById(newsletterId),
    enabled: !!user && user.role === 'admin' && !!newsletterId,
  });

  const sendMutation = useMutation({
    mutationFn: (id: number) => newsletterAPI.send(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['newsletter', newsletterId] });
      queryClient.invalidateQueries({ queryKey: ['newsletters-admin'] });
      alert('뉴스레터가 발송되었습니다!');
    },
    onError: (error: any) => {
      alert(error.response?.data?.detail || '발송에 실패했습니다.');
    },
  });

  const handleSend = () => {
    if (confirm(`"${newsletter?.title}" 뉴스레터를 모든 구독자에게 발송하시겠습니까?`)) {
      sendMutation.mutate(newsletterId);
    }
  };

  if (authLoading || !user) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!newsletter) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="bg-red-900/30 border border-red-500 text-red-200 px-6 py-4 rounded-lg">
            뉴스레터를 찾을 수 없습니다.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-8 max-w-5xl">
        {/* Header */}
        <div className="mb-8">
          <Link href="/admin/newsletter" className="text-blue-400 hover:text-blue-300 text-sm mb-2 inline-block">
            ← 뉴스레터 목록으로
          </Link>
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-4xl font-bold">{newsletter.title}</h1>
                <span
                  className={`px-3 py-1 text-sm rounded-full ${
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
              <div className="flex items-center gap-4 text-sm text-gray-400">
                <span>생성일: {new Date(newsletter.created_at).toLocaleString('ko-KR')}</span>
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
              </div>
            </div>

            {newsletter.status === 'draft' && (
              <button
                onClick={handleSend}
                className="px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-semibold transition"
                disabled={sendMutation.isPending}
              >
                {sendMutation.isPending ? '발송 중...' : '📧 발송하기'}
              </button>
            )}
          </div>
        </div>

        {/* Stats */}
        {newsletter.status === 'sent' && (
          <div className="bg-green-900/20 border border-green-700 rounded-lg p-6 mb-8">
            <div className="flex items-center gap-6">
              <div>
                <p className="text-sm text-green-400 mb-1">발송 수</p>
                <p className="text-3xl font-bold text-green-300">{newsletter.sent_count || 0}</p>
              </div>
              <div className="h-12 w-px bg-green-700"></div>
              <div>
                <p className="text-sm text-green-400 mb-1">발송 완료</p>
                <p className="text-lg text-green-300">
                  {newsletter.sent_at
                    ? new Date(newsletter.sent_at).toLocaleDateString('ko-KR', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })
                    : '-'}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Content Preview */}
        <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
          <div className="bg-gray-900 px-6 py-4 border-b border-gray-700">
            <h2 className="text-xl font-bold">📄 내용 미리보기</h2>
          </div>
          <div className="p-8">
            {/* HTML Content Preview */}
            <div
              className="prose prose-invert max-w-none"
              dangerouslySetInnerHTML={{ __html: newsletter.content }}
            />
          </div>
        </div>

        {/* HTML Source */}
        <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden mt-6">
          <div className="bg-gray-900 px-6 py-4 border-b border-gray-700">
            <h2 className="text-xl font-bold">💻 HTML 소스</h2>
          </div>
          <div className="p-6">
            <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
              <code className="text-sm text-gray-300 font-mono">{newsletter.content}</code>
            </pre>
          </div>
        </div>

        {/* Actions */}
        <div className="mt-8 flex gap-4">
          <Link
            href="/admin/newsletter"
            className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold transition"
          >
            목록으로
          </Link>
        </div>
      </div>
    </div>
  );
}
