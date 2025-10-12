import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { QueryProvider } from "@/providers/query-provider";
import { AuthProvider } from "@/contexts/auth-context";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "AI ON - AI 기술 스터디 × 바이브코딩 프로젝트",
  description: "AI ON에서 AI 기술 스터디와 바이브코딩 프로젝트를 만나보세요. 최신 AI 개발 소식과 기술 인사이트를 공유합니다.",
  keywords: "AI ON, AI, 인공지능, 바이브코딩, 기술 스터디, 블로그, 프로젝트",
  authors: [{ name: "AI ON" }],
  openGraph: {
    title: "AI ON - AI 기술 스터디 × 바이브코딩 프로젝트",
    description: "AI ON의 블로그와 프로젝트 쇼케이스",
    type: "website",
    locale: "ko_KR",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className={`${inter.variable} antialiased`}>
        <QueryProvider>
          <AuthProvider>
            <Navbar />
            {children}
            <Footer />
          </AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
