'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { projectAPI, blogAPI } from '@/lib/api';

export default function Stats() {
  const { data: projects } = useQuery({
    queryKey: ['projects-count'],
    queryFn: () => projectAPI.list({ page_size: 100 }),
  });

  const { data: blogs } = useQuery({
    queryKey: ['blogs-count'],
    queryFn: () => blogAPI.list({ page_size: 100 }),
  });

  // Calculate unique tech stack count from all projects
  const uniqueTechStack = React.useMemo(() => {
    if (!projects?.items) return 0;

    const allTech = new Set<string>();
    projects.items.forEach((project: any) => {
      if (project.tech_stack && Array.isArray(project.tech_stack)) {
        project.tech_stack.forEach((tech: string) => allTech.add(tech));
      }
    });

    return allTech.size;
  }, [projects]);

  const stats = [
    {
      value: projects?.items?.length || 0,
      label: 'Projects',
      suffix: '',
    },
    {
      value: blogs?.items?.filter((b: any) => b.status === 'published').length || 0,
      label: 'Blog Posts',
      suffix: '',
    },
    {
      value: uniqueTechStack > 0 ? uniqueTechStack : 12,
      label: 'Tech Stack',
      suffix: '+',
    },
    {
      value: '100%',
      label: 'Open Source',
      suffix: '',
    },
  ];

  return (
    <section className="mb-24">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <div
            key={index}
            className="bg-gray-800/30 border border-gray-700 rounded-xl p-6 text-center"
          >
            <div className="text-3xl font-bold text-white mb-1">
              {stat.value}{stat.suffix}
            </div>
            <div className="text-sm text-gray-500 uppercase tracking-wider">{stat.label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
