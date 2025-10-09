'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/auth-context';
import { useRouter } from 'next/navigation';
import { projectAPI } from '@/lib/api';
import Link from 'next/link';

export default function NewProjectPage() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState('');

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('');
  const [status, setStatus] = useState<'completed' | 'in_progress'>('in_progress');
  const [techStack, setTechStack] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [githubUrl2, setGithubUrl2] = useState('');
  const [demoUrl, setDemoUrl] = useState('');

  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'admin')) {
      router.push('/');
    }
  }, [user, authLoading, router]);

  const handleAIGenerate = async () => {
    if (!githubUrl && !demoUrl) {
      setError('GitHub URL 또는 Demo URL을 먼저 입력해주세요.');
      return;
    }

    setAiLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/ai/generate-project-info`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          github_url: githubUrl || undefined,
          demo_url: demoUrl || undefined,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'AI 생성에 실패했습니다.');
      }

      const data = await response.json();

      // 폼 자동 채우기
      setName(data.name);
      setDescription(data.description);
      setContent(data.content);
      setCategory(data.category);
      setTechStack(data.tech_stack.join(', '));

      alert('✨ AI가 프로젝트 정보를 생성했습니다!');
    } catch (err: any) {
      setError(err.message || 'AI 생성에 실패했습니다.');
    } finally {
      setAiLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const techArray = techStack.split(',').map(t => t.trim()).filter(t => t);

      await projectAPI.create({
        name,
        description,
        content: content || undefined,
        category: category || undefined,
        status,
        tech_stack: techArray,
        github_url: githubUrl || undefined,
        github_url_2: githubUrl2 || undefined,
        demo_url: demoUrl || undefined,
      });

      alert('프로젝트가 생성되었습니다!');
      router.push('/admin/projects');
    } catch (err: any) {
      setError(err.response?.data?.detail || '프로젝트 생성에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading) {
    return <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 flex items-center justify-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
    </div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-8 max-w-3xl">
        <Link href="/admin/projects" className="text-green-400 hover:text-green-300 text-sm mb-4 inline-block">
          ← 프로젝트 목록으로
        </Link>

        <h1 className="text-4xl font-bold mb-8">➕ 새 프로젝트 추가</h1>

        {error && (
          <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">프로젝트 이름 *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              placeholder="예: MP4 압축 도구"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">설명 *</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              rows={4}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              placeholder="프로젝트에 대한 설명을 작성하세요"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">상세 콘텐츠 (Markdown)</label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={12}
              placeholder="## 프로젝트 소개&#10;&#10;상세한 설명을 Markdown 형식으로 작성하세요..."
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500 font-mono text-sm"
            />
            <p className="text-xs text-gray-500 mt-1">Markdown 형식으로 작성하면 프로젝트 상세 페이지에 표시됩니다</p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-2">카테고리</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              >
                <option value="">선택</option>
                <option value="AI/ML">AI/ML</option>
                <option value="Finance">Finance</option>
                <option value="Video">Video</option>
                <option value="DevOps">DevOps</option>
                <option value="Blockchain">Blockchain</option>
                <option value="Web">Web</option>
                <option value="Mobile">Mobile</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">상태 *</label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value as 'completed' | 'in_progress')}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              >
                <option value="in_progress">진행중</option>
                <option value="completed">완료</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">기술 스택 (쉼표로 구분)</label>
            <input
              type="text"
              value={techStack}
              onChange={(e) => setTechStack(e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              placeholder="예: Python, FastAPI, PostgreSQL"
            />
            <p className="text-xs text-gray-500 mt-1">쉼표(,)로 구분하여 입력하세요</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">GitHub URL</label>
            <input
              type="url"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              placeholder="https://github.com/..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">GitHub URL #2 (선택)</label>
            <input
              type="url"
              value={githubUrl2}
              onChange={(e) => setGithubUrl2(e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              placeholder="https://github.com/... (관련/서브 리포지토리)"
            />
            <p className="text-xs text-gray-500 mt-1">관련 또는 서브 리포지토리가 있을 경우 입력하세요</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Demo URL</label>
            <input
              type="url"
              value={demoUrl}
              onChange={(e) => setDemoUrl(e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              placeholder="https://..."
            />
          </div>

          {/* AI 자동 생성 버튼 */}
          <div className="bg-blue-900/30 border border-blue-700 rounded-lg p-4">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <h3 className="font-semibold text-blue-400 mb-1 flex items-center gap-2">
                  <span>✨</span> AI로 자동 작성
                </h3>
                <p className="text-sm text-gray-400">
                  GitHub 또는 Demo URL을 입력하면 AI가 프로젝트 이름, 설명, 상세 콘텐츠, 카테고리, 기술 스택을 자동으로 생성합니다.
                </p>
              </div>
              <button
                type="button"
                onClick={handleAIGenerate}
                disabled={aiLoading || (!githubUrl && !demoUrl)}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap flex items-center gap-2"
              >
                {aiLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    생성 중...
                  </>
                ) : (
                  <>
                    <span>✨</span>
                    AI로 작성
                  </>
                )}
              </button>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-semibold transition disabled:opacity-50"
            >
              {isLoading ? '생성 중...' : '프로젝트 생성'}
            </button>
            <Link
              href="/admin/projects"
              className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold transition text-center"
            >
              취소
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
