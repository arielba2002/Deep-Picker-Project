FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Use nginx to serve the built app
FROM nginx:alpine

# Copy built app to nginx
COPY --from=0 /app/dist /usr/share/nginx/html

# Copy nginx configurations
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx-main.conf /etc/nginx/nginx.conf

# Create directories with proper permissions for OpenShift non-root users
RUN mkdir -p /tmp/nginx-cache /tmp/nginx-client-temp /tmp/nginx-proxy-temp /tmp/nginx-fastcgi-temp /tmp/nginx-uwsgi-temp /tmp/nginx-scgi-temp && \
    mkdir -p /var/log/nginx /var/run && \
    chmod -R 777 /tmp/nginx-* /var/log/nginx /var/run /usr/share/nginx/html && \
    chmod 644 /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Switch to non-root user (OpenShift will override this with the correct user ID)  
USER 1001

# Expose port
EXPOSE 3000

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 