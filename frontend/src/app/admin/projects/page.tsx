'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/auth-context';
import { useRouter } from 'next/navigation';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { projectAPI } from '@/lib/api';

export default function AdminProjectsListPage() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const queryClient = useQueryClient();
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'admin')) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  const { data, isLoading } = useQuery({
    queryKey: ['projects-admin'],
    queryFn: () => projectAPI.list({ page_size: 100 }),
    enabled: !!user && user.role === 'admin',
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => projectAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects-admin'] });
      alert('프로젝트가 삭제되었습니다.');
    },
    onError: () => {
      alert('삭제에 실패했습니다.');
    },
  });

  const handleDelete = (id: number, name: string) => {
    if (confirm(`"${name}" 프로젝트를 삭제하시겠습니까?`)) {
      deleteMutation.mutate(id);
    }
  };

  const filteredProjects = data?.items?.filter((project: any) => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return (
      project.name.toLowerCase().includes(query) ||
      project.description?.toLowerCase().includes(query) ||
      project.tech_stack?.some((tech: string) => tech.toLowerCase().includes(query))
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
            <h1 className="text-4xl font-bold">🚀 프로젝트 관리</h1>
          </div>
          <Link
            href="/admin/projects/new"
            className="px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-semibold transition"
          >
            ➕ 새 프로젝트 추가
          </Link>
        </div>

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="프로젝트 검색 (이름, 설명, 기술)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-green-500"
          />
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <p className="text-sm text-gray-400">전체</p>
            <p className="text-2xl font-bold">{data?.total || 0}</p>
          </div>
          <div className="bg-green-900/20 border border-green-700 rounded-lg p-4">
            <p className="text-sm text-green-400">완료</p>
            <p className="text-2xl font-bold text-green-400">
              {data?.items?.filter((p: any) => p.status === 'completed').length || 0}
            </p>
          </div>
          <div className="bg-blue-900/20 border border-blue-700 rounded-lg p-4">
            <p className="text-sm text-blue-400">진행중</p>
            <p className="text-2xl font-bold text-blue-400">
              {data?.items?.filter((p: any) => p.status === 'in_progress').length || 0}
            </p>
          </div>
        </div>

        {/* Project List */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto"></div>
          </div>
        ) : filteredProjects && filteredProjects.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredProjects.map((project: any) => (
              <div
                key={project.id}
                className="bg-gray-800 border border-gray-700 rounded-lg p-6 hover:border-green-500 transition"
              >
                <div className="flex items-start justify-between mb-3">
                  <h2 className="text-xl font-bold flex-1">{project.name}</h2>
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

                <p className="text-gray-400 text-sm mb-4 line-clamp-3">{project.description}</p>

                {project.category && (
                  <p className="text-xs text-gray-500 mb-3">카테고리: {project.category}</p>
                )}

                {project.tech_stack && project.tech_stack.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-4">
                    {project.tech_stack.slice(0, 4).map((tech: string) => (
                      <span key={tech} className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded">
                        {tech}
                      </span>
                    ))}
                    {project.tech_stack.length > 4 && (
                      <span className="px-2 py-1 bg-gray-700 text-gray-400 text-xs rounded">
                        +{project.tech_stack.length - 4}
                      </span>
                    )}
                  </div>
                )}

                <div className="flex gap-2">
                  <Link
                    href={`/admin/projects/${project.id}/edit`}
                    className="flex-1 text-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition"
                  >
                    수정
                  </Link>
                  <button
                    onClick={() => handleDelete(project.id, project.name)}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm transition"
                    disabled={deleteMutation.isPending}
                  >
                    삭제
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-400">
            {searchQuery ? '검색 결과가 없습니다.' : '아직 프로젝트가 없습니다.'}
          </div>
        )}
      </div>
    </div>
  );
}
