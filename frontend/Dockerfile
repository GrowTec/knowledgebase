FROM node:16-alpine

WORKDIR /app

# copy files and install dependencies
COPY . ./
RUN npm install

# Change working directory so relative imports work
WORKDIR /app/src/routes
RUN npm run build

# Change to the new "build" directory
WORKDIR /app/build

EXPOSE 3000

CMD ["node", "index.js"]