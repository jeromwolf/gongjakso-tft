'use client';

import { useState } from 'react';
import { newsletterAPI } from '@/lib/api';

export default function NewsletterForm() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleSubscribe = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage(null);
    setIsLoading(true);

    try {
      await newsletterAPI.subscribe({ email });
      setMessage({
        type: 'success',
        text: '구독이 완료되었습니다! 곧 첫 번째 뉴스레터를 받아보실 수 있습니다.',
      });
      setEmail('');
    } catch (err: any) {
      setMessage({
        type: 'error',
        text: err.response?.data?.detail || '구독에 실패했습니다. 다시 시도해주세요.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="mb-24">
      <div className="bg-gray-800/30 border border-gray-700 rounded-xl p-10 text-center">
        <h2 className="text-2xl font-bold mb-2 text-white">Newsletter</h2>
        <p className="text-sm text-gray-500 mb-4">뉴스레터 구독</p>
        <p className="text-gray-400 text-sm mb-8">매주 최신 기술 트렌드와 개발 팁을 받아보세요</p>

        <form onSubmit={handleSubscribe} className="max-w-md mx-auto">
          <div className="flex gap-3 mb-4">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              required
              disabled={isLoading}
              className="flex-1 px-4 py-3 rounded-lg bg-gray-900 border border-gray-600 text-white placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {isLoading ? '처리 중...' : '구독'}
            </button>
          </div>
          {message && (
            <div
              className={`text-sm p-3 rounded-lg ${
                message.type === 'success'
                  ? 'bg-green-500/10 text-green-400 border border-green-500/30'
                  : 'bg-red-500/10 text-red-400 border border-red-500/30'
              }`}
            >
              {message.text}
            </div>
          )}
        </form>
      </div>
    </section>
  );
}
