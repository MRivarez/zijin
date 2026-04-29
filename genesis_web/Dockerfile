# 编译Vue代码
FROM node:24-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install --registry=https://registry.npmmirror.com
COPY . .
RUN npm run build

# Nginx部署
FROM nginx:alpine
# 将编译好的dist文件夹覆盖到Nginx默认目录
COPY --from=builder /app/dist /usr/share/nginx/html
# 暴露Nginx默认端口
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]