FROM node:20-alpine
WORKDIR /app

COPY package.json ./
RUN npm install --only=prod

COPY src ./src

ENV VSTORAGE_PATH=/data/vstorage
ENV STORAGE_URL=http://storage:8080

EXPOSE 8081
CMD ["node", "src/server.js"]
