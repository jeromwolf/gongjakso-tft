import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    // 프로덕션 빌드 시 ESLint 에러 무시 (경고로만 표시)
    ignoreDuringBuilds: true,
  },
  typescript: {
    // 프로덕션 빌드 시 TypeScript 에러 무시
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
