'use client';

import { useEffect } from 'react';
import { useAuth } from '@/contexts/auth-context';
import { useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { blogAPI, projectAPI } from '@/lib/api';

export default function AdminDashboard() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();

  // Check if user is admin
  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'admin')) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  // Fetch stats
  const { data: blogs } = useQuery({
    queryKey: ['blogs-admin'],
    queryFn: () => blogAPI.list({ page_size: 100 }),
    enabled: !!user && user.role === 'admin',
  });

  const { data: projects } = useQuery({
    queryKey: ['projects-admin'],
    queryFn: () => projectAPI.list({ page_size: 100 }),
    enabled: !!user && user.role === 'admin',
  });

  if (authLoading || !user) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p>로딩 중...</p>
        </div>
      </div>
    );
  }

  const stats = [
    {
      name: '블로그 포스트',
      value: blogs?.total || 0,
      link: '/admin/blog',
      icon: '📝',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      name: '프로젝트',
      value: projects?.total || 0,
      link: '/admin/projects',
      icon: '🚀',
      color: 'from-green-500 to-emerald-500',
    },
    {
      name: '발행된 블로그',
      value: blogs?.items?.filter((b: any) => b.status === 'published').length || 0,
      link: '/admin/blog',
      icon: '✅',
      color: 'from-purple-500 to-pink-500',
    },
    {
      name: '초안 블로그',
      value: blogs?.items?.filter((b: any) => b.status === 'draft').length || 0,
      link: '/admin/blog',
      icon: '📄',
      color: 'from-yellow-500 to-orange-500',
    },
  ];

  const quickActions = [
    {
      name: '새 블로그 작성',
      link: '/admin/blog/new',
      icon: '✍️',
      description: '새로운 블로그 포스트 작성',
    },
    {
      name: '새 프로젝트 추가',
      link: '/admin/projects/new',
      icon: '➕',
      description: '새로운 프로젝트 추가',
    },
    {
      name: '블로그 관리',
      link: '/admin/blog',
      icon: '📋',
      description: '모든 블로그 보기 및 관리',
    },
    {
      name: '프로젝트 관리',
      link: '/admin/projects',
      icon: '🗂️',
      description: '모든 프로젝트 보기 및 관리',
    },
    {
      name: '뉴스레터 관리',
      link: '/admin/newsletter',
      icon: '📧',
      description: '뉴스레터 작성 및 발송',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">🔐 관리자 대시보드</h1>
          <p className="text-gray-400">안녕하세요, {user.name}님</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {stats.map((stat) => (
            <Link
              key={stat.name}
              href={stat.link}
              className="bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 rounded-xl p-6 hover:border-blue-500 transition group"
            >
              <div className="flex items-center justify-between mb-4">
                <span className="text-4xl">{stat.icon}</span>
                <div className={`text-3xl font-bold bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`}>
                  {stat.value}
                </div>
              </div>
              <h3 className="text-lg font-semibold text-gray-300 group-hover:text-white transition">
                {stat.name}
              </h3>
            </Link>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">빠른 작업</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action) => (
              <Link
                key={action.name}
                href={action.link}
                className="bg-gray-800 border border-gray-700 rounded-lg p-6 hover:border-blue-500 hover:bg-gray-750 transition group"
              >
                <div className="text-3xl mb-3">{action.icon}</div>
                <h3 className="text-lg font-semibold mb-2 group-hover:text-blue-400 transition">
                  {action.name}
                </h3>
                <p className="text-sm text-gray-400">{action.description}</p>
              </Link>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="grid md:grid-cols-2 gap-8">
          {/* Recent Blogs */}
          <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold">최근 블로그</h2>
              <Link
                href="/admin/blog"
                className="text-sm text-blue-400 hover:text-blue-300"
              >
                모두 보기 →
              </Link>
            </div>
            <div className="space-y-4">
              {blogs?.items?.slice(0, 5).map((blog: any) => (
                <Link
                  key={blog.id}
                  href={`/admin/blog/${blog.id}/edit`}
                  className="block p-3 bg-gray-900 rounded-lg hover:bg-gray-750 transition"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-semibold mb-1 line-clamp-1">{blog.title}</h3>
                      <p className="text-xs text-gray-400">
                        {new Date(blog.created_at).toLocaleDateString('ko-KR')}
                      </p>
                    </div>
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        blog.status === 'published'
                          ? 'bg-green-900 text-green-300'
                          : 'bg-yellow-900 text-yellow-300'
                      }`}
                    >
                      {blog.status === 'published' ? '발행' : '초안'}
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          </div>

          {/* Recent Projects */}
          <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold">최근 프로젝트</h2>
              <Link
                href="/admin/projects"
                className="text-sm text-blue-400 hover:text-blue-300"
              >
                모두 보기 →
              </Link>
            </div>
            <div className="space-y-4">
              {projects?.items?.slice(0, 5).map((project: any) => (
                <Link
                  key={project.id}
                  href={`/admin/projects/${project.id}/edit`}
                  className="block p-3 bg-gray-900 rounded-lg hover:bg-gray-750 transition"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-semibold mb-1 line-clamp-1">{project.name}</h3>
                      <p className="text-xs text-gray-400">{project.category}</p>
                    </div>
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        project.status === 'completed'
                          ? 'bg-green-900 text-green-300'
                          : 'bg-blue-900 text-blue-300'
                      }`}
                    >
                      {project.status === 'completed' ? '완료' : '진행중'}
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
