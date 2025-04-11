const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  const isDevelopment = process.env.NODE_ENV === 'development';

  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8001',
      changeOrigin: true,
      pathRewrite: {
        '^/api': ''
      },
      onProxyReq: (proxyReq, req, res) => {
        // In development, allow all hosts
        if (isDevelopment) {
          if (req.headers.authorization) {
            proxyReq.setHeader('Authorization', req.headers.authorization);
          }
          return;
        }

        // In production, restrict to localhost
        const allowedHosts = ['localhost', '127.0.0.1'];
        const host = req.hostname;

        if (!allowedHosts.includes(host)) {
          res.writeHead(403, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Access denied' }));
          return;
        }

        if (req.headers.authorization) {
          proxyReq.setHeader('Authorization', req.headers.authorization);
        }
      }
    })
  );
};