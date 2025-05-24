FROM node:18-alpine

WORKDIR /app

# 1) install dependencies
COPY package*.json ./
RUN npm ci

# 2) copy your app
COPY . .

# 3) ensure any user can write into /app (and subdirs like node_modules/.vite-temp)
RUN chmod -R a+rwX /app

EXPOSE 3000

# 4) start Vite in host-bind mode
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
