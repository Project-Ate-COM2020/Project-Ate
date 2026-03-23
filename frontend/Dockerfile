FROM node:25.7.0-alpine AS Build
WORKDIR /app
COPY package-lock.json package.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine AS Production
COPY --from=Build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
