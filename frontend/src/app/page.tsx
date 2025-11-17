'use client';

import HeroSection from '@/components/home/HeroSection';
import Stats from '@/components/home/Stats';
import RecentBlogs from '@/components/home/RecentBlogs';
import FeaturedProjects from '@/components/home/FeaturedProjects';
import NewsletterForm from '@/components/home/NewsletterForm';
import NewsSection from '@/components/home/NewsSection';
import DonationSection from '@/components/donation/DonationSection';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white pt-16">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <HeroSection />

        {/* Newsletter Form - 상단으로 이동 */}
        <NewsletterForm />

        {/* 2단 레이아웃: 뉴스(왼쪽) + 블로그(오른쪽) */}
        <section className="mb-24">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-white mb-2">주간 뉴스와 활동</h2>
            <p className="text-gray-400">매주 업데이트되는 최신 IT 뉴스와 블로그 콘텐츠</p>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* 왼쪽: 뉴스 */}
            <NewsSection />

            {/* 오른쪽: 블로그 */}
            <RecentBlogs />
          </div>
        </section>

        {/* Stats */}
        <Stats />

        {/* Donation Section */}
        <DonationSection
          config={{
            accountNumber: '100039997509',
            bankName: '토스뱅크',
            tossDeepLink: 'supertoss://send?bank=%ED%86%A0%EC%8A%A4%EB%B1%85%ED%81%AC&accountNo=100039997509&origin=qr'
          }}
        />

        {/* Featured Projects - 하단으로 이동 */}
        <FeaturedProjects />
      </div>
    </div>
  );
}
