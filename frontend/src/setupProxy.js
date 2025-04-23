const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  const isDevelopment = process.env.NODE_ENV === 'development';

  // Proxy for API requests (keep your existing configuration)
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8001',
      changeOrigin: true,
      pathRewrite: { '^/api': '' }
    })
  );

  // Add this specific proxy for Swagger UI
  app.use(
    ['/docs', '/openapi.json', '/swagger-ui*'],
    createProxyMiddleware({
      target: 'http://localhost:8001',
      changeOrigin: true,
      // Important: Don't rewrite the path for Swagger assets
      pathRewrite: (path) => path
    })
  );
};
