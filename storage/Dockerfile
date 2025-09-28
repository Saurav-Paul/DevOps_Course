FROM node:20-alpine
WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install --only=prod

COPY src ./src

ENV LOG_PATH=/var/storage/log.txt
EXPOSE 8080
CMD ["node", "src/server.js"]
