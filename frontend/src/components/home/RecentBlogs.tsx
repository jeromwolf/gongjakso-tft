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
      <section className="mb-24">
        <div className="text-center mb-12">
          <h2 className="text-2xl font-bold mb-3 text-white">Recent Blog</h2>
          <p className="text-gray-400 text-sm">최신 기술 인사이트와 개발 이야기</p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-gray-800/30 border border-gray-700 rounded-xl p-6 animate-pulse">
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
    <section className="mb-24">
      <div className="text-center mb-12">
        <h2 className="text-2xl font-bold mb-2 text-white">Recent Blog</h2>
        <p className="text-gray-400 text-sm">최신 기술 인사이트와 개발 이야기</p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {recentBlogs.map((blog: any) => (
          <Link
            key={blog.id}
            href={`/blog/${blog.slug}`}
            className="group bg-gray-800/30 hover:bg-gray-800/50 border border-gray-700 hover:border-gray-600 rounded-xl p-6 transition-all"
          >
            {/* Tags */}
            {blog.tags && blog.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-3">
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
            <h3 className="text-lg font-bold text-white mb-2 line-clamp-2 group-hover:text-blue-400 transition">
              {blog.title}
            </h3>

            {/* Excerpt */}
            {blog.excerpt && (
              <p className="text-sm text-gray-400 mb-4 line-clamp-2">{blog.excerpt}</p>
            )}

            {/* Meta */}
            <div className="flex items-center gap-3 text-xs text-gray-500">
              <span>{format(new Date(blog.created_at), 'yyyy.MM.dd', { locale: ko })}</span>
              <span>•</span>
              <span>{blog.view_count} views</span>
            </div>
          </Link>
        ))}
      </div>

      <div className="text-center mt-8">
        <Link
          href="/blog"
          className="inline-block px-6 py-3 bg-gray-800/50 hover:bg-gray-800 border border-gray-700 hover:border-gray-600 rounded-lg text-sm font-medium text-white transition"
        >
          모든 블로그 보기 →
        </Link>
      </div>
    </section>
  );
}
