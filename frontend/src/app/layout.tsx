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
  title: "데이터공작소 개발 TFT - Blog & Newsletter",
  description: "데이터공작소 개발 TFT의 블로그와 뉴스레터를 만나보세요. 최신 개발 소식과 기술 인사이트를 공유합니다.",
  keywords: "데이터공작소, 개발, 블로그, 뉴스레터, TFT",
  authors: [{ name: "데이터공작소 TFT" }],
  openGraph: {
    title: "데이터공작소 개발 TFT",
    description: "데이터공작소 개발 TFT의 블로그와 뉴스레터",
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
