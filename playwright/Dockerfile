FROM node:18

WORKDIR /app

COPY server/package.json ./
RUN npm install

COPY server ./server

EXPOSE 3000

CMD ["node", "server/index.js"]
