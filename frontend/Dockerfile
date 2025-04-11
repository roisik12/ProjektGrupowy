# 🔧 Stage 1 - Build React frontend
FROM node:20-alpine AS builder

WORKDIR /app

# ✅ Copy .env.production
COPY .env.production .env

# 📦 Install dependencies
COPY package*.json ./
RUN npm install

# 🧠 Copy application sources
COPY . .

# ⚙️ Build application
RUN npm run build

# 🚀 Stage 2 - Deploy via nginx
FROM nginx:alpine

# 🔁 Copy built files
COPY --from=builder /app/build /usr/share/nginx/html

# 📁 Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]