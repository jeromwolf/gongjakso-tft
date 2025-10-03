'use client';

import Link from 'next/link';
import { useAuth } from '@/contexts/auth-context';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const pathname = usePathname();

  // Don't show navbar on login/signup pages
  if (pathname === '/login' || pathname === '/signup') {
    return null;
  }

  return (
    <nav className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            데이터공작소 TFT
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-6">
            <Link
              href="/blog"
              className="text-gray-300 hover:text-white transition flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              블로그
            </Link>
            <Link
              href="/projects"
              className="text-gray-300 hover:text-white transition flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
              </svg>
              프로젝트
            </Link>

            {isAuthenticated ? (
              <>
                {/* User Menu */}
                <div className="flex items-center gap-4">
                  <span className="text-sm text-gray-400">
                    {user?.name}
                  </span>
                  {user?.role === 'admin' && (
                    <Link
                      href="/admin"
                      className="text-sm px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded-full transition"
                    >
                      관리자
                    </Link>
                  )}
                  <button
                    onClick={logout}
                    className="text-sm px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition"
                  >
                    로그아웃
                  </button>
                </div>
              </>
            ) : (
              <>
                {/* Auth Links */}
                <Link
                  href="/login"
                  className="text-gray-300 hover:text-white transition"
                >
                  로그인
                </Link>
                <Link
                  href="/signup"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
                >
                  회원가입
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
