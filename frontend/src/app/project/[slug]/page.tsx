'use client';

import { use } from 'react';
import { useQuery } from '@tanstack/react-query';
import { projectAPI } from '@/lib/api';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';

interface ProjectPageProps {
  params: Promise<{
    slug: string;
  }>;
}

export default function ProjectPage({ params }: ProjectPageProps) {
  const { slug } = use(params);

  const { data: project, isLoading, error } = useQuery({
    queryKey: ['project', slug],
    queryFn: () => projectAPI.getBySlug(slug),
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">프로젝트를 불러오는 중...</p>
        </div>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-400 mb-4">오류 발생</h2>
          <p className="text-gray-400 mb-4">프로젝트를 찾을 수 없습니다.</p>
          <Link href="/" className="text-blue-400 hover:text-blue-300">
            ← 홈으로 돌아가기
          </Link>
        </div>
      </div>
    );
  }

  const statusBadgeColors = {
    completed: 'bg-green-600 text-green-100',
    in_progress: 'bg-yellow-600 text-yellow-100',
    active: 'bg-blue-600 text-blue-100',
    archived: 'bg-gray-600 text-gray-100',
  };

  const difficultyColors = {
    Beginner: 'bg-green-500/20 text-green-400 border-green-500',
    Intermediate: 'bg-yellow-500/20 text-yellow-400 border-yellow-500',
    Advanced: 'bg-red-500/20 text-red-400 border-red-500',
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      <div className="container mx-auto px-4 py-16 max-w-5xl">
        {/* Header */}
        <div className="mb-8">
          <Link href="/" className="text-blue-400 hover:text-blue-300 mb-4 inline-block">
            ← 홈으로
          </Link>

          {/* Title and Status */}
          <div className="flex items-start justify-between gap-4 mb-4">
            <h1 className="text-4xl font-bold">{project.name}</h1>
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${statusBadgeColors[project.status]}`}>
              {project.status === 'completed' ? '완료' :
               project.status === 'in_progress' ? '작업중' :
               project.status === 'active' ? '활성' : '보관'}
            </span>
          </div>

          {/* Meta Info */}
          <div className="flex flex-wrap gap-4 text-sm text-gray-400 mb-4">
            {project.category && (
              <span className="flex items-center gap-1">
                <i className="fas fa-folder"></i>
                {project.category}
              </span>
            )}
            {project.difficulty && (
              <span className={`px-2 py-1 border rounded ${difficultyColors[project.difficulty as keyof typeof difficultyColors] || 'bg-gray-500/20 text-gray-400 border-gray-500'}`}>
                {project.difficulty}
              </span>
            )}
            <span className="flex items-center gap-1">
              <i className="fas fa-eye"></i>
              {project.view_count} views
            </span>
          </div>

          {/* Description */}
          {project.description && (
            <p className="text-xl text-gray-300 mb-6">{project.description}</p>
          )}

          {/* Links */}
          <div className="flex flex-wrap gap-3">
            {project.github_url && (
              <a
                href={project.github_url}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg font-medium transition flex items-center gap-2"
              >
                <i className="fab fa-github"></i>
                GitHub
              </a>
            )}
            {project.demo_url && (
              <a
                href={project.demo_url}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition flex items-center gap-2"
              >
                <i className="fas fa-external-link-alt"></i>
                Live Demo
              </a>
            )}
          </div>
        </div>

        {/* Tech Stack */}
        {project.tech_stack && project.tech_stack.length > 0 && (
          <div className="mb-8 p-6 bg-gray-800 rounded-lg border border-gray-700">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <i className="fas fa-code"></i>
              기술 스택
            </h2>
            <div className="flex flex-wrap gap-2">
              {project.tech_stack.map((tech) => (
                <span
                  key={tech}
                  className="px-3 py-1 bg-blue-600/20 text-blue-400 border border-blue-600 rounded-full text-sm"
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Content (Markdown) */}
        {project.content && (
          <div className="prose prose-invert prose-lg max-w-none mb-8">
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <ReactMarkdown
                components={{
                  h1: ({ node, ...props }) => <h1 className="text-3xl font-bold mb-4 text-blue-400" {...props} />,
                  h2: ({ node, ...props }) => <h2 className="text-2xl font-bold mb-3 mt-6 text-blue-300" {...props} />,
                  h3: ({ node, ...props }) => <h3 className="text-xl font-bold mb-2 mt-4" {...props} />,
                  p: ({ node, ...props }) => <p className="mb-4 leading-relaxed text-gray-300" {...props} />,
                  ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-4 space-y-2 text-gray-300" {...props} />,
                  ol: ({ node, ...props }) => <ol className="list-decimal list-inside mb-4 space-y-2 text-gray-300" {...props} />,
                  li: ({ node, ...props }) => <li className="ml-4" {...props} />,
                  code: ({ node, inline, ...props }: any) =>
                    inline ? (
                      <code className="bg-gray-900 px-2 py-1 rounded text-blue-400 font-mono text-sm" {...props} />
                    ) : (
                      <code className="block bg-gray-900 p-4 rounded-lg my-4 overflow-x-auto font-mono text-sm" {...props} />
                    ),
                  pre: ({ node, ...props }) => <pre className="bg-gray-900 rounded-lg overflow-x-auto" {...props} />,
                  a: ({ node, ...props }) => (
                    <a className="text-blue-400 hover:text-blue-300 underline" target="_blank" rel="noopener noreferrer" {...props} />
                  ),
                }}
              >
                {project.content}
              </ReactMarkdown>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-12 pt-6 border-t border-gray-700 text-center">
          <Link href="/" className="text-blue-400 hover:text-blue-300 inline-flex items-center gap-2">
            <i className="fas fa-arrow-left"></i>
            다른 프로젝트 보기
          </Link>
        </div>
      </div>
    </div>
  );
}
