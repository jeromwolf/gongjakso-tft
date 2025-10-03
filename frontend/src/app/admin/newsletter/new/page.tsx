'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/auth-context';
import { useRouter } from 'next/navigation';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { newsletterAPI } from '@/lib/api';
import Link from 'next/link';

export default function NewNewsletterPage() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const queryClient = useQueryClient();
  const [error, setError] = useState('');

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'admin')) {
      router.push('/');
    }
  }, [user, authLoading, router]);

  const createMutation = useMutation({
    mutationFn: (data: { title: string; content: string }) => newsletterAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['newsletters-admin'] });
      alert('뉴스레터가 생성되었습니다!');
      router.push('/admin/newsletter');
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || '뉴스레터 생성에 실패했습니다.');
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    createMutation.mutate({ title, content });
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <Link href="/admin/newsletter" className="text-blue-400 hover:text-blue-300 text-sm mb-4 inline-block">
          ← 뉴스레터 목록으로
        </Link>

        <h1 className="text-4xl font-bold mb-8">✍️ 새 뉴스레터 작성</h1>

        {error && (
          <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">제목 *</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              placeholder="예: 월간 뉴스레터 - 2025년 10월 특별호"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">내용 * (HTML)</label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              required
              rows={20}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500 font-mono text-sm"
              placeholder="HTML 형식으로 뉴스레터 내용을 작성하세요..."
            />
            <p className="text-xs text-gray-500 mt-2">
              💡 Tip: HTML 형식으로 작성하세요. 기본 태그 (h2, h3, p, ul, li, a, strong, em)를 사용할 수 있습니다.
            </p>
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={createMutation.isPending}
              className="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-semibold transition disabled:opacity-50"
            >
              {createMutation.isPending ? '생성 중...' : '초안으로 저장'}
            </button>
            <Link
              href="/admin/newsletter"
              className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold transition text-center"
            >
              취소
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
