'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { blogAPI } from '@/lib/api';
import { formatDistanceToNow } from 'date-fns';
import { ko } from 'date-fns/locale';

export default function BlogListPage() {
  const [searchQuery, setSearchQuery] = React.useState<string>('');
  const [selectedTag, setSelectedTag] = React.useState<string>('전체');

  const { data, isLoading, error } = useQuery({
    queryKey: ['blogs'],
    queryFn: () => blogAPI.list({ page: 1, page_size: 100 }),
  });

  // Extract unique tags
  const allTags = React.useMemo(() => {
    if (!data?.items) return ['전체'];
    const tags = new Set<string>();
    data.items.forEach((blog: any) => {
      if (blog.tags && Array.isArray(blog.tags)) {
        blog.tags.forEach((tag: string) => tags.add(tag));
      }
    });
    return ['전체', ...Array.from(tags)];
  }, [data]);

  // Filter blogs by search and tag
  const filteredBlogs = React.useMemo(() => {
    if (!data?.items) return [];

    let filtered = data.items.filter((blog: any) => blog.status === 'published');

    // Filter by tag
    if (selectedTag !== '전체') {
      filtered = filtered.filter((blog: any) =>
        blog.tags?.includes(selectedTag)
      );
    }

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter((blog: any) => {
        const matchTitle = blog.title.toLowerCase().includes(query);
        const matchExcerpt = blog.excerpt?.toLowerCase().includes(query);
        const matchTags = blog.tags?.some((tag: string) =>
          tag.toLowerCase().includes(query)
        );
        return matchTitle || matchExcerpt || matchTags;
      });
    }

    return filtered;
  }, [data, selectedTag, searchQuery]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">블로그 목록을 불러오는 중...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-400 mb-4">오류 발생</h2>
          <p className="text-gray-400">블로그 목록을 불러올 수 없습니다.</p>
          <p className="text-sm text-gray-500 mt-2">{(error as Error).message}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <header className="mb-8">
          <Link href="/" className="text-blue-400 hover:text-blue-300 mb-4 inline-block">
            ← 홈으로
          </Link>

          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-6">
            <div className="flex-1">
              <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                📝 블로그
              </h1>
              <p className="text-xl text-gray-300">
                데이터공작소 TFT의 기술 블로그입니다
              </p>
            </div>

            {/* Search Box */}
            <div className="md:w-80">
              <div className="relative">
                <input
                  type="text"
                  placeholder="블로그 검색 (제목, 내용, 태그)"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-4 py-3 pl-12 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                />
                <svg
                  className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery('')}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-white"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}
              </div>
              {searchQuery && (
                <p className="text-sm text-gray-400 mt-2">
                  {filteredBlogs.length}개 포스트 검색됨
                </p>
              )}
            </div>
          </div>

          {/* Tag Filter */}
          {!isLoading && allTags.length > 1 && (
            <div className="flex flex-wrap gap-2">
              {allTags.map((tag) => (
                <button
                  key={tag}
                  onClick={() => setSelectedTag(tag)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                    selectedTag === tag
                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/50'
                      : 'bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700'
                  }`}
                >
                  {tag === '전체' ? '전체' : `#${tag}`}
                </button>
              ))}
            </div>
          )}
        </header>

        {/* Blog List */}
        {filteredBlogs.length > 0 ? (
          <div className="space-y-6">
            {filteredBlogs.map((blog) => (
              <Link
                key={blog.id}
                href={`/blog/${blog.slug}`}
                className="block bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-blue-500 transition group"
              >
                <div className="flex items-start justify-between mb-3">
                  <h2 className="text-2xl font-bold group-hover:text-blue-400 transition">
                    {blog.title}
                  </h2>
                  {blog.status === 'draft' && (
                    <span className="px-3 py-1 bg-yellow-600 text-yellow-100 text-xs rounded-full">
                      초안
                    </span>
                  )}
                </div>

                {blog.excerpt && (
                  <p className="text-gray-300 mb-4 line-clamp-2">{blog.excerpt}</p>
                )}

                {blog.tags && blog.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {blog.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-3 py-1 bg-gray-700 text-gray-300 text-sm rounded-full"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                )}

                <div className="flex items-center gap-4 text-sm text-gray-400">
                  <span>✍️ {blog.author}</span>
                  <span>•</span>
                  <span>
                    👁️ {blog.view_count} views
                  </span>
                  <span>•</span>
                  <span>
                    {formatDistanceToNow(new Date(blog.created_at), {
                      addSuffix: true,
                      locale: ko,
                    })}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        ) : !isLoading ? (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">
              {searchQuery || selectedTag !== '전체'
                ? '검색 결과가 없습니다.'
                : '아직 작성된 블로그가 없습니다.'}
            </p>
          </div>
        ) : null}

        {/* Pagination */}
        {data && data.total_pages > 1 && (
          <div className="mt-12 flex justify-center gap-2">
            {Array.from({ length: data.total_pages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                className={`px-4 py-2 rounded ${
                  page === data.page
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {page}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
