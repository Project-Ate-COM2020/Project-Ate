FROM node:25.7.0-alpine
WORKDIR /app
COPY package-lock.json package.json ./
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]