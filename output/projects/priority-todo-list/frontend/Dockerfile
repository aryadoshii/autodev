# Stage 1: Build stage
FROM node:20-alpine AS build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with npm
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the React app with Vite
RUN npm run build

# Stage 2: Production stage
FROM nginx:alpine

# Copy nginx configuration
COPY --from=build /app/nginx.conf /etc/nginx/nginx.conf

# Copy built files from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Remove default nginx index page
RUN rm /usr/share/nginx/html/index.html

# Set permissions for nginx user
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]