'use client';

import Link from 'next/link';
import HeroSection from '@/components/home/HeroSection';
import Stats from '@/components/home/Stats';
import RecentBlogs from '@/components/home/RecentBlogs';
import FeaturedProjects from '@/components/home/FeaturedProjects';
import UseCases from '@/components/home/UseCases';
import NewsletterForm from '@/components/home/NewsletterForm';
import CoffeeSupport from '@/components/home/CoffeeSupport';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <HeroSection />

        {/* Stats */}
        <Stats />

        {/* Featured Projects */}
        <FeaturedProjects />

        {/* Recent Blogs */}
        <RecentBlogs />

        {/* Use Cases */}
        <UseCases />

        {/* Newsletter Form */}
        <NewsletterForm />

        {/* Coffee Support */}
        <CoffeeSupport />

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-400">
          <p>© 2025 데이터공작소 개발 TFT. All rights reserved.</p>
          <div className="mt-4 flex gap-4 justify-center">
            <Link href="/blog" className="hover:text-white transition">
              블로그
            </Link>
            <Link
              href="https://github.com/jeromwolf/gongjakso-tft"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition"
            >
              GitHub
            </Link>
            <Link href="mailto:contact@gongjakso-tft.com" className="hover:text-white transition">
              Contact
            </Link>
          </div>
        </footer>
      </div>
    </div>
  );
}
