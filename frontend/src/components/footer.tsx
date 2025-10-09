import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-gray-900 border-t border-gray-800 text-gray-400">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">데이터공작소 TFT</h3>
            <p className="text-sm leading-relaxed">
              데이터 분석, AI/ML, 풀스택 개발 프로젝트를 공유하는 커뮤니티 플랫폼입니다.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">바로가기</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/blog" className="hover:text-green-400 transition">
                  블로그
                </Link>
              </li>
              <li>
                <Link href="/projects" className="hover:text-green-400 transition">
                  프로젝트
                </Link>
              </li>
              <li>
                <Link href="/admin" className="hover:text-green-400 transition">
                  관리자
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">리소스</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a
                  href="https://gongjakso-tft.onrender.com/api/docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-green-400 transition"
                >
                  API 문서
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/jeromwolf/gongjakso-tft"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-green-400 transition"
                >
                  GitHub Repository
                </a>
              </li>
            </ul>
          </div>

          {/* Social Media */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">소셜 미디어</h3>
            <div className="flex gap-4">
              {/* YouTube */}
              <a
                href="https://www.youtube.com/channel/UCzwPW_BSlr4Art7ckUYK5kw"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-gray-800 hover:bg-red-600 rounded-full flex items-center justify-center transition-colors"
                aria-label="YouTube 채널"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
              </a>

              {/* GitHub */}
              <a
                href="https://github.com/jeromwolf"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-gray-800 hover:bg-gray-700 rounded-full flex items-center justify-center transition-colors"
                aria-label="GitHub"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd"/>
                </svg>
              </a>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
          <p>
            © {new Date().getFullYear()} 데이터공작소 개발 TFT. All rights reserved.
          </p>
          <p className="mt-2 text-xs text-gray-500">
            Built with Next.js, FastAPI, and PostgreSQL
          </p>
        </div>
      </div>
    </footer>
  );
}
