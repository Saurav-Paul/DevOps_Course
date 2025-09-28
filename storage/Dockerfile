FROM node:20-alpine
WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install --only=prod
COPY server.js .
ENV LOG_PATH=/var/storage/log.txt
EXPOSE 8080
CMD ["node", "server.js"]