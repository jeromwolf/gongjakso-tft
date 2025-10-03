'use client';

import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { projectAPI } from '@/lib/api';

export default function FeaturedProjects() {
  const { data, isLoading } = useQuery({
    queryKey: ['featured-projects'],
    queryFn: () => projectAPI.list({ page_size: 100 }),
  });

  if (isLoading) {
    return null;
  }

  // Get completed projects or first 3
  const featuredProjects = data?.items
    ?.filter((p: any) => p.status === 'completed')
    .slice(0, 3) || data?.items?.slice(0, 3) || [];

  if (featuredProjects.length === 0) {
    return null;
  }

  return (
    <section className="mb-24">
      <div className="text-center mb-12">
        <h2 className="text-2xl font-bold mb-2 text-white">Featured Projects</h2>
        <p className="text-gray-400 text-sm">데이터공작소 TFT의 대표 솔루션들</p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {featuredProjects.map((project: any) => (
          <Link
            key={project.id}
            href={`/project/${project.slug}`}
            className="group bg-gray-800/30 hover:bg-gray-800/50 border border-gray-700 hover:border-gray-600 rounded-xl p-6 transition-all"
          >
            {/* Category & Status */}
            <div className="flex items-center gap-2 mb-3">
              {project.category && (
                <span className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded">
                  {project.category}
                </span>
              )}
              {project.status === 'completed' && (
                <span className="px-2 py-1 bg-green-500/10 text-green-400 text-xs rounded border border-green-500/20">
                  완료
                </span>
              )}
            </div>

            {/* Title */}
            <h3 className="text-lg font-bold text-white mb-2 group-hover:text-blue-400 transition">
              {project.name}
            </h3>

            {/* Description */}
            <p className="text-sm text-gray-400 mb-4 line-clamp-2">{project.description}</p>

            {/* Tech Stack */}
            {project.tech_stack && project.tech_stack.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {project.tech_stack.slice(0, 3).map((tech: string) => (
                  <span
                    key={tech}
                    className="px-2 py-1 bg-blue-500/10 text-blue-400 text-xs rounded"
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
          </Link>
        ))}
      </div>

      <div className="text-center mt-8">
        <Link
          href="/projects"
          className="inline-block px-6 py-3 bg-gray-800/50 hover:bg-gray-800 border border-gray-700 hover:border-gray-600 rounded-lg text-sm font-medium text-white transition"
        >
          모든 프로젝트 보기 →
        </Link>
      </div>
    </section>
  );
}
