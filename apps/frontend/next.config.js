/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  poweredByHeader: false,
  compress: true,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://sorry_api:8083/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
