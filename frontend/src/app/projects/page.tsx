'use client';

import { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { projectAPI } from '@/lib/api';
import { Project } from '@/lib/types';

const categoryLabels: Record<string, string> = {
  '전체': '전체',
  'AI/ML': 'AI/ML',
  'Finance': '금융',
  'Video': '비디오',
  'DevOps': 'DevOps',
  'Blockchain': '블록체인',
  'Web': '웹',
  'Mobile': '모바일',
};

export default function ProjectsPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('전체');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const { data, isLoading, error } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectAPI.list({ page_size: 100 }),
  });

  // Extract unique categories from projects
  const categories = useMemo(() => {
    if (!data?.items) return ['전체'];
    const uniqueCategories = new Set(
      data.items.map((p: Project) => p.category).filter(Boolean)
    );
    return ['전체', ...Array.from(uniqueCategories)];
  }, [data]);

  // Filter projects by category and search query
  const filteredProjects = useMemo(() => {
    if (!data?.items) return [];

    let filtered = data.items;

    // Filter by category
    if (selectedCategory !== '전체') {
      filtered = filtered.filter((p: Project) => p.category === selectedCategory);
    }

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter((p: Project) => {
        // Search in name, description, and tech stack
        const matchName = p.name.toLowerCase().includes(query);
        const matchDescription = p.description?.toLowerCase().includes(query);
        const matchTechStack = p.tech_stack?.some((tech: string) =>
          tech.toLowerCase().includes(query)
        );
        return matchName || matchDescription || matchTechStack;
      });
    }

    return filtered;
  }, [data, selectedCategory, searchQuery]);

  // Count projects per category
  const categoryCounts = useMemo(() => {
    if (!data?.items) return {};
    const counts: Record<string, number> = { '전체': data.items.length };
    data.items.forEach((p: Project) => {
      if (p.category) {
        counts[p.category] = (counts[p.category] || 0) + 1;
      }
    });
    return counts;
  }, [data]);

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
        <div className="container mx-auto px-4 py-16">
          <div className="bg-red-900/30 border border-red-500 text-red-200 px-6 py-4 rounded-lg">
            오류 발생: 프로젝트 목록을 불러올 수 없습니다.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-6">
            <div className="flex-1">
              <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-green-400 to-blue-500 bg-clip-text text-transparent">
                💻 프로젝트
              </h1>
              <p className="text-xl text-gray-300">
                데이터공작소 TFT가 개발한 혁신적인 솔루션들을 만나보세요
              </p>
            </div>

            {/* Search Box */}
            <div className="md:w-80">
              <div className="relative">
                <input
                  type="text"
                  placeholder="프로젝트 검색 (이름, 설명, 기술)"
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
                  {filteredProjects.length}개 프로젝트 검색됨
                </p>
              )}
            </div>
          </div>
        </header>

        {/* Category Filter */}
        {!isLoading && categories.length > 1 && (
          <div className="mb-8 flex flex-wrap gap-3">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-2 rounded-full font-medium transition-all flex items-center gap-2 ${
                  selectedCategory === category
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/50'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700'
                }`}
              >
                <span>{categoryLabels[category] || category}</span>
                <span className={`text-sm px-2 py-0.5 rounded-full ${
                  selectedCategory === category
                    ? 'bg-blue-700'
                    : 'bg-gray-700'
                }`}>
                  {categoryCounts[category] || 0}
                </span>
              </button>
            ))}
          </div>
        )}

        {isLoading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div
                key={i}
                className="bg-gray-800 rounded-lg border border-gray-700 p-6 animate-pulse"
              >
                <div className="h-6 bg-gray-700 rounded mb-4"></div>
                <div className="h-4 bg-gray-700 rounded mb-2"></div>
                <div className="h-4 bg-gray-700 rounded mb-4"></div>
                <div className="flex gap-2 mb-4">
                  <div className="h-6 bg-gray-700 rounded w-16"></div>
                  <div className="h-6 bg-gray-700 rounded w-16"></div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredProjects.map((project: Project) => (
              <Link
                key={project.id}
                href={`/project/${project.slug}`}
                className="group bg-gray-800 rounded-lg border border-gray-700 hover:border-green-500 transition-all p-6 hover:shadow-xl hover:shadow-green-500/20"
              >
                <div className="flex items-start justify-between mb-3">
                  <h2 className="text-xl font-bold group-hover:text-green-400 transition flex-1">
                    {project.name}
                  </h2>
                  {project.status === 'completed' && (
                    <span className="px-2 py-1 bg-green-900/30 text-green-400 text-xs rounded-full border border-green-500/30">
                      완료
                    </span>
                  )}
                  {project.status === 'in_progress' && (
                    <span className="px-2 py-1 bg-blue-900/30 text-blue-400 text-xs rounded-full border border-blue-500/30">
                      진행중
                    </span>
                  )}
                </div>

                <p className="text-gray-300 mb-4 line-clamp-2">{project.description}</p>

                {project.tech_stack && project.tech_stack.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {project.tech_stack.slice(0, 3).map((tech) => (
                      <span
                        key={tech}
                        className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded"
                      >
                        {tech}
                      </span>
                    ))}
                    {project.tech_stack.length > 3 && (
                      <span className="px-2 py-1 bg-gray-700 text-gray-400 text-xs rounded">
                        +{project.tech_stack.length - 3}
                      </span>
                    )}
                  </div>
                )}

                <div className="flex gap-2 text-sm text-gray-400">
                  {project.github_url && (
                    <div className="flex items-center gap-1">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                      </svg>
                      GitHub
                    </div>
                  )}
                  {project.demo_url && (
                    <div className="flex items-center gap-1">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                      Demo
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}

        {filteredProjects.length === 0 && !isLoading && (
          <div className="text-center py-16 text-gray-400">
            {selectedCategory === '전체'
              ? '아직 등록된 프로젝트가 없습니다.'
              : `"${selectedCategory}" 카테고리에 해당하는 프로젝트가 없습니다.`}
          </div>
        )}
      </div>
    </div>
  );
}
