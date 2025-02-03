# Stage 1: Build the React app
FROM node:18-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:alpine

# Install gettext
RUN apk add --no-cache gettext

# Copy the build output to Nginx's default public directory
COPY --from=build /app/build /usr/share/nginx/html

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 80
EXPOSE 80

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]