'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/auth-context';
import { useRouter } from 'next/navigation';
import { blogAPI, aiAPI } from '@/lib/api';
import ReactMarkdown from 'react-markdown';
import Link from 'next/link';

export default function NewBlogPage() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'edit' | 'preview'>('edit');

  // Form state
  const [title, setTitle] = useState('');
  const [excerpt, setExcerpt] = useState('');
  const [content, setContent] = useState('');
  const [tags, setTags] = useState('');
  const [status, setStatus] = useState<'draft' | 'published'>('draft');

  // AI state
  const [showAIPanel, setShowAIPanel] = useState(false);
  const [aiTopic, setAiTopic] = useState('');
  const [aiStyle, setAiStyle] = useState<'technical' | 'casual' | 'tutorial'>('technical');
  const [aiLength, setAiLength] = useState<'short' | 'medium' | 'long'>('medium');
  const [isGenerating, setIsGenerating] = useState(false);
  const [imageUrl, setImageUrl] = useState('');
  const [imageAlt, setImageAlt] = useState('');

  // Check if user is admin
  useEffect(() => {
    if (!authLoading && (!user || user.role !== 'admin')) {
      router.push('/');
    }
  }, [user, authLoading, router]);

  // AI 기능: 전체 블로그 생성
  const handleGenerateBlog = async () => {
    if (!aiTopic.trim()) {
      setError('주제를 입력해주세요.');
      return;
    }

    setIsGenerating(true);
    setError('');

    try {
      const result = await aiAPI.generateBlog({
        topic: aiTopic,
        style: aiStyle,
        length: aiLength,
        save_as_draft: false,
      });

      setTitle(result.title);
      setExcerpt(result.excerpt);
      setContent(result.content);
      setTags(result.tags.join(', '));
      setShowAIPanel(false);
      alert('AI가 블로그를 생성했습니다! 내용을 확인하고 수정해주세요.');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'AI 생성에 실패했습니다.');
    } finally {
      setIsGenerating(false);
    }
  };

  // AI 기능: 제목만 생성
  const handleGenerateTitle = async () => {
    const topic = aiTopic || content.substring(0, 100);
    if (!topic.trim()) {
      setError('내용 또는 주제를 먼저 입력해주세요.');
      return;
    }

    setIsGenerating(true);
    try {
      const result = await aiAPI.preview(topic, aiStyle);
      setTitle(result.title || '');
    } catch (err: any) {
      setError('제목 생성에 실패했습니다.');
    } finally {
      setIsGenerating(false);
    }
  };

  // 요약 자동 생성 (내용 기반)
  const handleGenerateExcerpt = () => {
    if (!content.trim()) {
      setError('내용을 먼저 작성해주세요.');
      return;
    }
    // 첫 150자 추출 또는 첫 단락
    const firstParagraph = content.split('\n\n')[0];
    const excerpt = firstParagraph.substring(0, 150).trim() + (firstParagraph.length > 150 ? '...' : '');
    setExcerpt(excerpt);
  };

  // 이미지 마크다운 삽입
  const handleInsertImage = () => {
    if (!imageUrl.trim()) return;
    const imageMarkdown = `![${imageAlt || '이미지'}](${imageUrl})\n\n`;
    setContent(content + imageMarkdown);
    setImageUrl('');
    setImageAlt('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const tagArray = tags
        .split(',')
        .map((tag) => tag.trim())
        .filter((tag) => tag.length > 0);

      const blog = await blogAPI.create({
        title,
        excerpt: excerpt || undefined,
        content,
        tags: tagArray.length > 0 ? tagArray : undefined,
        status,
      });

      router.push(`/blog/${blog.slug}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || '블로그 생성에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white flex items-center justify-center pt-16">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user || user.role !== 'admin') {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <Link href="/blog" className="text-blue-400 hover:text-blue-300 mb-4 inline-block">
            ← 블로그 목록
          </Link>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold">새 블로그 작성</h1>
              <p className="text-gray-400 mt-2">Markdown 형식으로 블로그를 작성하세요</p>
            </div>
            <button
              type="button"
              onClick={() => setShowAIPanel(!showAIPanel)}
              className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-medium transition flex items-center gap-2"
            >
              <i className="fas fa-magic"></i>
              {showAIPanel ? 'AI 패널 닫기' : '🤖 AI로 작성'}
            </button>
          </div>
        </div>

        {/* AI Generation Panel */}
        {showAIPanel && (
          <div className="mb-8 bg-gradient-to-r from-purple-900/30 to-blue-900/30 border border-purple-500/50 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <i className="fas fa-robot text-purple-400"></i>
              AI 블로그 생성
            </h2>
            <p className="text-gray-300 mb-6">
              주제를 입력하면 AI가 전체 블로그를 작성해드립니다.
            </p>

            <div className="space-y-4">
              {/* Topic Input */}
              <div>
                <label className="block text-sm font-medium mb-2">주제 *</label>
                <input
                  type="text"
                  value={aiTopic}
                  onChange={(e) => setAiTopic(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  placeholder="예: FastAPI로 RESTful API 만들기"
                />
              </div>

              {/* Style & Length */}
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">스타일</label>
                  <select
                    value={aiStyle}
                    onChange={(e) => setAiStyle(e.target.value as any)}
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  >
                    <option value="technical">기술적 (Technical)</option>
                    <option value="casual">편안한 (Casual)</option>
                    <option value="tutorial">튜토리얼 (Tutorial)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">길이</label>
                  <select
                    value={aiLength}
                    onChange={(e) => setAiLength(e.target.value as any)}
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  >
                    <option value="short">짧게 (Short)</option>
                    <option value="medium">보통 (Medium)</option>
                    <option value="long">길게 (Long)</option>
                  </select>
                </div>
              </div>

              {/* Generate Button */}
              <button
                type="button"
                onClick={handleGenerateBlog}
                disabled={isGenerating || !aiTopic.trim()}
                className="w-full px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg font-medium transition flex items-center justify-center gap-2"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    AI가 작성 중...
                  </>
                ) : (
                  <>
                    <i className="fas fa-magic"></i>
                    전체 블로그 생성
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label htmlFor="title" className="block text-sm font-medium">
                제목 *
              </label>
              <button
                type="button"
                onClick={handleGenerateTitle}
                disabled={isGenerating}
                className="px-3 py-1 bg-purple-600/20 hover:bg-purple-600/40 border border-purple-500 rounded text-sm transition flex items-center gap-1"
              >
                <i className="fas fa-magic text-xs"></i>
                AI 제안
              </button>
            </div>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              placeholder="블로그 제목을 입력하세요"
            />
          </div>

          {/* Excerpt */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label htmlFor="excerpt" className="block text-sm font-medium">
                요약 (선택)
              </label>
              <button
                type="button"
                onClick={handleGenerateExcerpt}
                disabled={!content.trim()}
                className="px-3 py-1 bg-purple-600/20 hover:bg-purple-600/40 border border-purple-500 rounded text-sm transition flex items-center gap-1 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <i className="fas fa-wand-magic-sparkles text-xs"></i>
                자동 생성
              </button>
            </div>
            <input
              id="excerpt"
              type="text"
              value={excerpt}
              onChange={(e) => setExcerpt(e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              placeholder="블로그 요약을 입력하세요"
            />
          </div>

          {/* Tags */}
          <div>
            <label htmlFor="tags" className="block text-sm font-medium mb-2">
              태그 (선택)
            </label>
            <input
              id="tags"
              type="text"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              placeholder="쉼표로 구분하여 입력 (예: React, TypeScript, Next.js)"
            />
            {tags && (
              <div className="flex flex-wrap gap-2 mt-2">
                {tags.split(',').map((tag, index) => {
                  const trimmedTag = tag.trim();
                  return trimmedTag ? (
                    <span
                      key={index}
                      className="px-2 py-1 bg-blue-600/20 text-blue-400 border border-blue-600 rounded text-sm"
                    >
                      #{trimmedTag}
                    </span>
                  ) : null;
                })}
              </div>
            )}
          </div>

          {/* Status */}
          <div>
            <label className="block text-sm font-medium mb-2">상태</label>
            <div className="flex gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  name="status"
                  value="draft"
                  checked={status === 'draft'}
                  onChange={(e) => setStatus(e.target.value as 'draft')}
                  className="w-4 h-4 text-blue-600"
                />
                <span>초안</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  name="status"
                  value="published"
                  checked={status === 'published'}
                  onChange={(e) => setStatus(e.target.value as 'published')}
                  className="w-4 h-4 text-blue-600"
                />
                <span>발행</span>
              </label>
            </div>
          </div>

          {/* Image Insertion Helper */}
          <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-4">
            <h3 className="text-sm font-medium mb-3 flex items-center gap-2">
              <i className="fas fa-image text-blue-400"></i>
              이미지 삽입 도우미
            </h3>
            <div className="grid md:grid-cols-3 gap-3">
              <input
                type="text"
                value={imageUrl}
                onChange={(e) => setImageUrl(e.target.value)}
                className="md:col-span-2 px-3 py-2 bg-gray-800 border border-gray-700 rounded text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                placeholder="이미지 URL (https://...)"
              />
              <input
                type="text"
                value={imageAlt}
                onChange={(e) => setImageAlt(e.target.value)}
                className="px-3 py-2 bg-gray-800 border border-gray-700 rounded text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                placeholder="설명 (선택)"
              />
            </div>
            <button
              type="button"
              onClick={handleInsertImage}
              disabled={!imageUrl.trim()}
              className="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded text-sm transition flex items-center gap-2"
            >
              <i className="fas fa-plus"></i>
              본문에 이미지 삽입
            </button>
            <p className="text-xs text-gray-500 mt-2">
              💡 Tip: 무료 이미지는 <a href="https://unsplash.com" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">Unsplash</a>에서 찾을 수 있습니다
            </p>
          </div>

          {/* Content - Tab Navigation */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-sm font-medium">
                내용 * (Markdown)
              </label>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => setActiveTab('edit')}
                  className={`px-4 py-2 rounded-lg transition ${
                    activeTab === 'edit'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}
                >
                  편집
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('preview')}
                  className={`px-4 py-2 rounded-lg transition ${
                    activeTab === 'preview'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}
                >
                  미리보기
                </button>
              </div>
            </div>

            {/* Edit Tab */}
            {activeTab === 'edit' && (
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                required
                rows={20}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition font-mono text-sm"
                placeholder="Markdown 형식으로 내용을 작성하세요..."
              />
            )}

            {/* Preview Tab */}
            {activeTab === 'preview' && (
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 min-h-[500px]">
                {content ? (
                  <div className="prose prose-invert prose-lg max-w-none">
                    <ReactMarkdown
                      components={{
                        h1: ({ node, ...props }) => <h1 className="text-3xl font-bold mb-4 text-blue-400" {...props} />,
                        h2: ({ node, ...props }) => <h2 className="text-2xl font-bold mb-3 text-blue-300" {...props} />,
                        h3: ({ node, ...props }) => <h3 className="text-xl font-bold mb-2 text-blue-200" {...props} />,
                        p: ({ node, ...props }) => <p className="mb-4 leading-relaxed text-gray-300" {...props} />,
                        ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-4 space-y-2 text-gray-300" {...props} />,
                        ol: ({ node, ...props }) => <ol className="list-decimal list-inside mb-4 space-y-2 text-gray-300" {...props} />,
                        li: ({ node, ...props }) => <li className="ml-4" {...props} />,
                        blockquote: ({ node, ...props }) => (
                          <blockquote className="border-l-4 border-blue-500 pl-4 py-2 my-4 italic text-gray-400" {...props} />
                        ),
                        code: ({ node, inline, ...props }: any) =>
                          inline ? (
                            <code className="bg-gray-900 px-2 py-1 rounded text-blue-400 font-mono text-sm" {...props} />
                          ) : (
                            <code className="block bg-gray-900 p-4 rounded-lg my-4 overflow-x-auto font-mono text-sm" {...props} />
                          ),
                        pre: ({ node, ...props }) => <pre className="bg-gray-900 rounded-lg overflow-x-auto" {...props} />,
                        a: ({ node, ...props }) => (
                          <a className="text-blue-400 hover:text-blue-300 underline" {...props} />
                        ),
                      }}
                    >
                      {content}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <p className="text-gray-500 text-center">내용이 없습니다. 편집 탭에서 내용을 작성하세요.</p>
                )}
              </div>
            )}
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-500/10 border border-red-500 text-red-400 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* Submit Button */}
          <div className="flex gap-4">
            <button
              type="submit"
              disabled={isLoading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg font-medium transition flex items-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  저장 중...
                </>
              ) : (
                <>
                  <i className="fas fa-save"></i>
                  {status === 'published' ? '발행하기' : '초안 저장'}
                </>
              )}
            </button>
            <Link
              href="/blog"
              className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-medium transition"
            >
              취소
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
