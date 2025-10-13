'use client';

import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { blogAPI } from '@/lib/api';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';

export default function RecentBlogs() {
  const { data, isLoading } = useQuery({
    queryKey: ['recent-blogs'],
    queryFn: () => blogAPI.list({ page_size: 3 }),
  });

  if (isLoading) {
    return (
      <section>
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">✍️ 블로그</h2>
          <p className="text-sm text-gray-400 mt-1">최신 기술 인사이트</p>
        </div>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-gray-800/30 border border-gray-700 rounded-lg p-4 animate-pulse">
              <div className="h-4 bg-gray-700 rounded mb-3"></div>
              <div className="h-3 bg-gray-700 rounded mb-2"></div>
              <div className="h-3 bg-gray-700 rounded w-2/3"></div>
            </div>
          ))}
        </div>
      </section>
    );
  }

  const recentBlogs = data?.items?.filter((blog: any) => blog.status === 'published').slice(0, 3) || [];

  if (recentBlogs.length === 0) {
    return null;
  }

  return (
    <section>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white">✍️ 블로그</h2>
          <p className="text-sm text-gray-400 mt-1">최신 기술 인사이트</p>
        </div>
        <Link
          href="/blog"
          className="text-sm text-blue-400 hover:text-blue-300 transition flex items-center gap-1"
        >
          전체보기
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>

      <div className="space-y-4">
        {recentBlogs.map((blog: any) => (
          <Link
            key={blog.id}
            href={`/blog/${blog.slug}`}
            className="group block bg-gray-800/30 hover:bg-gray-800/50 border border-gray-700 hover:border-gray-600 rounded-lg p-4 transition-all"
          >
            {/* Tags */}
            {blog.tags && blog.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-2">
                {blog.tags.slice(0, 2).map((tag: string) => (
                  <span
                    key={tag}
                    className="px-2 py-1 bg-blue-500/10 text-blue-400 text-xs rounded border border-blue-500/20"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            )}

            {/* Title */}
            <h3 className="font-semibold text-white mb-2 line-clamp-2 group-hover:text-blue-400 transition">
              {blog.title}
            </h3>

            {/* Excerpt */}
            {blog.excerpt && (
              <p className="text-sm text-gray-400 mb-3 line-clamp-2">{blog.excerpt}</p>
            )}

            {/* Meta */}
            <div className="flex items-center gap-3 text-xs text-gray-500">
              <span className="flex items-center gap-1">
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                    clipRule="evenodd"
                  />
                </svg>
                {format(new Date(blog.created_at), 'yyyy.MM.dd', { locale: ko })}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                  <path
                    fillRule="evenodd"
                    d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                    clipRule="evenodd"
                  />
                </svg>
                {blog.view_count}
              </span>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
