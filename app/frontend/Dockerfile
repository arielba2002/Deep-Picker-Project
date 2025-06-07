FROM node:18-alpine as builder

WORKDIR /app

# Install dependencies and build
COPY package*.json ./
RUN npm ci
COPY . .

# Build in production mode with correct API URL
ENV VITE_API_URL=/api
RUN npm run build

# Production image
FROM nginx:alpine

# Create nginx directories with proper permissions
RUN mkdir -p /var/cache/nginx /var/run/nginx /var/tmp/nginx && \
    chown -R nginx:nginx /var/cache/nginx /var/run/nginx /var/tmp/nginx && \
    chmod -R 777 /var/cache/nginx /var/run/nginx /var/tmp/nginx && \
    mkdir -p /var/run/nginx && \
    chown -R nginx:nginx /var/run/nginx

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration files
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

# Set proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html

EXPOSE 3000
USER nginx
CMD ["nginx", "-g", "daemon off;"]
