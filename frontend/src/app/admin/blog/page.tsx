'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/auth-context';
import { useRouter } from 'next/navigation';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { blogAPI } from '@/lib/api';

export default function AdminBlogListPage() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const queryClient = useQueryClient();
  const [searchQuery, setSearchQuery] = useState('');

  // Check if user is admin
  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'admin')) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  const { data, isLoading } = useQuery({
    queryKey: ['blogs-admin'],
    queryFn: () => blogAPI.list({ page_size: 100 }),
    enabled: !!user && user.role === 'admin',
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => blogAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['blogs-admin'] });
      alert('블로그가 삭제되었습니다.');
    },
    onError: () => {
      alert('삭제에 실패했습니다.');
    },
  });

  const handleDelete = (id: number, title: string) => {
    if (confirm(`"${title}" 블로그를 삭제하시겠습니까?`)) {
      deleteMutation.mutate(id);
    }
  };

  const filteredBlogs = data?.items?.filter((blog: any) => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return (
      blog.title.toLowerCase().includes(query) ||
      blog.excerpt?.toLowerCase().includes(query) ||
      blog.tags?.some((tag: string) => tag.toLowerCase().includes(query))
    );
  });

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
            <h1 className="text-4xl font-bold">📝 블로그 관리</h1>
          </div>
          <Link
            href="/admin/blog/new"
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition"
          >
            ✍️ 새 블로그 작성
          </Link>
        </div>

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="블로그 검색 (제목, 내용, 태그)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <p className="text-sm text-gray-400">전체</p>
            <p className="text-2xl font-bold">{data?.total || 0}</p>
          </div>
          <div className="bg-green-900/20 border border-green-700 rounded-lg p-4">
            <p className="text-sm text-green-400">발행됨</p>
            <p className="text-2xl font-bold text-green-400">
              {data?.items?.filter((b: any) => b.status === 'published').length || 0}
            </p>
          </div>
          <div className="bg-yellow-900/20 border border-yellow-700 rounded-lg p-4">
            <p className="text-sm text-yellow-400">초안</p>
            <p className="text-2xl font-bold text-yellow-400">
              {data?.items?.filter((b: any) => b.status === 'draft').length || 0}
            </p>
          </div>
        </div>

        {/* Blog List */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          </div>
        ) : filteredBlogs && filteredBlogs.length > 0 ? (
          <div className="space-y-4">
            {filteredBlogs.map((blog: any) => (
              <div
                key={blog.id}
                className="bg-gray-800 border border-gray-700 rounded-lg p-6 hover:border-blue-500 transition"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h2 className="text-xl font-bold">{blog.title}</h2>
                      <span
                        className={`px-3 py-1 text-xs rounded-full ${
                          blog.status === 'published'
                            ? 'bg-green-900 text-green-300'
                            : 'bg-yellow-900 text-yellow-300'
                        }`}
                      >
                        {blog.status === 'published' ? '발행됨' : '초안'}
                      </span>
                    </div>

                    {blog.excerpt && (
                      <p className="text-gray-400 mb-3 line-clamp-2">{blog.excerpt}</p>
                    )}

                    {blog.tags && blog.tags.length > 0 && (
                      <div className="flex flex-wrap gap-2 mb-3">
                        {blog.tags.map((tag: string) => (
                          <span key={tag} className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded">
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}

                    <div className="flex items-center gap-4 text-sm text-gray-400">
                      <span>👁️ {blog.view_count} views</span>
                      <span>•</span>
                      <span>{new Date(blog.created_at).toLocaleDateString('ko-KR')}</span>
                      <span>•</span>
                      <span>✍️ {blog.author}</span>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Link
                      href={`/admin/blog/${blog.id}/edit`}
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition"
                    >
                      수정
                    </Link>
                    <button
                      onClick={() => handleDelete(blog.id, blog.title)}
                      className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm transition"
                      disabled={deleteMutation.isPending}
                    >
                      삭제
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-400">
            {searchQuery ? '검색 결과가 없습니다.' : '아직 블로그가 없습니다.'}
          </div>
        )}
      </div>
    </div>
  );
}
