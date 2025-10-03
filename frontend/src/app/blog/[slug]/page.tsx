'use client';

import { use } from 'react';
import { useQuery } from '@tanstack/react-query';
import { blogAPI } from '@/lib/api';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';

interface BlogPageProps {
  params: Promise<{
    slug: string;
  }>;
}

export default function BlogPage({ params }: BlogPageProps) {
  const { slug } = use(params);

  const { data: blog, isLoading, error } = useQuery({
    queryKey: ['blog', slug],
    queryFn: () => blogAPI.getBySlug(slug),
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center pt-16">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">블로그를 불러오는 중...</p>
        </div>
      </div>
    );
  }

  if (error || !blog) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center pt-16">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-400 mb-4">오류 발생</h2>
          <p className="text-gray-400 mb-4">블로그 글을 찾을 수 없습니다.</p>
          <Link href="/blog" className="text-blue-400 hover:text-blue-300">
            ← 블로그 목록으로
          </Link>
        </div>
      </div>
    );
  }

  const statusBadgeColors = {
    published: 'bg-green-600 text-green-100',
    draft: 'bg-yellow-600 text-yellow-100',
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        {/* Header */}
        <div className="mb-8">
          <Link href="/blog" className="text-blue-400 hover:text-blue-300 mb-4 inline-block">
            ← 블로그 목록
          </Link>

          {/* Title and Status */}
          <div className="flex items-start justify-between gap-4 mb-4">
            <h1 className="text-4xl font-bold leading-tight">{blog.title}</h1>
            <span className={`px-3 py-1 rounded-full text-sm font-semibold whitespace-nowrap ${statusBadgeColors[blog.status]}`}>
              {blog.status === 'published' ? '발행됨' : '초안'}
            </span>
          </div>

          {/* Meta Info */}
          <div className="flex flex-wrap gap-4 text-sm text-gray-400 mb-4">
            {blog.author && (
              <span className="flex items-center gap-1">
                <i className="fas fa-user"></i>
                {blog.author.name}
              </span>
            )}
            <span className="flex items-center gap-1">
              <i className="fas fa-calendar"></i>
              {format(new Date(blog.created_at), 'yyyy년 M월 d일', { locale: ko })}
            </span>
            {blog.updated_at !== blog.created_at && (
              <span className="flex items-center gap-1">
                <i className="fas fa-edit"></i>
                수정: {format(new Date(blog.updated_at), 'yyyy년 M월 d일', { locale: ko })}
              </span>
            )}
            <span className="flex items-center gap-1">
              <i className="fas fa-eye"></i>
              {blog.view_count} views
            </span>
          </div>

          {/* Excerpt */}
          {blog.excerpt && (
            <p className="text-xl text-gray-300 mb-6 border-l-4 border-blue-500 pl-4 italic">
              {blog.excerpt}
            </p>
          )}

          {/* Tags */}
          {blog.tags && blog.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-6">
              {blog.tags.map((tag) => (
                <span
                  key={tag}
                  className="px-3 py-1 bg-blue-600/20 text-blue-400 border border-blue-600 rounded-full text-sm"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Content (Markdown) */}
        {blog.content && (
          <div className="prose prose-invert prose-lg max-w-none mb-8">
            <div className="bg-gray-800 rounded-lg p-8 border border-gray-700">
              <ReactMarkdown
                components={{
                  h1: ({ node, ...props }) => <h1 className="text-3xl font-bold mb-4 mt-8 text-blue-400" {...props} />,
                  h2: ({ node, ...props }) => <h2 className="text-2xl font-bold mb-3 mt-6 text-blue-300" {...props} />,
                  h3: ({ node, ...props }) => <h3 className="text-xl font-bold mb-2 mt-4 text-blue-200" {...props} />,
                  h4: ({ node, ...props }) => <h4 className="text-lg font-bold mb-2 mt-3" {...props} />,
                  p: ({ node, ...props }) => <p className="mb-4 leading-relaxed text-gray-300" {...props} />,
                  ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-4 space-y-2 text-gray-300" {...props} />,
                  ol: ({ node, ...props }) => <ol className="list-decimal list-inside mb-4 space-y-2 text-gray-300" {...props} />,
                  li: ({ node, ...props }) => <li className="ml-4" {...props} />,
                  blockquote: ({ node, ...props }) => (
                    <blockquote className="border-l-4 border-blue-500 pl-4 py-2 my-4 italic text-gray-400 bg-gray-900/50 rounded-r" {...props} />
                  ),
                  code: ({ node, inline, ...props }: any) =>
                    inline ? (
                      <code className="bg-gray-900 px-2 py-1 rounded text-blue-400 font-mono text-sm" {...props} />
                    ) : (
                      <code className="block bg-gray-900 p-4 rounded-lg my-4 overflow-x-auto font-mono text-sm" {...props} />
                    ),
                  pre: ({ node, ...props }) => <pre className="bg-gray-900 rounded-lg overflow-x-auto my-4" {...props} />,
                  a: ({ node, ...props }) => (
                    <a className="text-blue-400 hover:text-blue-300 underline" target="_blank" rel="noopener noreferrer" {...props} />
                  ),
                  img: ({ node, ...props }) => (
                    <img className="rounded-lg my-6 max-w-full h-auto" {...props} />
                  ),
                  hr: ({ node, ...props }) => <hr className="my-8 border-gray-700" {...props} />,
                  table: ({ node, ...props }) => (
                    <div className="overflow-x-auto my-4">
                      <table className="min-w-full border border-gray-700" {...props} />
                    </div>
                  ),
                  thead: ({ node, ...props }) => <thead className="bg-gray-900" {...props} />,
                  tbody: ({ node, ...props }) => <tbody className="divide-y divide-gray-700" {...props} />,
                  tr: ({ node, ...props }) => <tr className="border-b border-gray-700" {...props} />,
                  th: ({ node, ...props }) => <th className="px-4 py-2 text-left font-semibold" {...props} />,
                  td: ({ node, ...props }) => <td className="px-4 py-2" {...props} />,
                }}
              >
                {blog.content}
              </ReactMarkdown>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-12 pt-6 border-t border-gray-700">
          <div className="flex items-center justify-between">
            <Link href="/blog" className="text-blue-400 hover:text-blue-300 inline-flex items-center gap-2">
              <i className="fas fa-arrow-left"></i>
              블로그 목록으로
            </Link>

            {/* Author info */}
            {blog.author && (
              <div className="text-right">
                <p className="text-sm text-gray-400">작성자</p>
                <p className="text-white font-medium">{blog.author.name}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
