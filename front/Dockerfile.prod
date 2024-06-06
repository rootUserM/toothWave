# Stage 1: Build Vue.js app
FROM node:16-alpine as build-stage

# Set working directory
WORKDIR /app

# Copy package.json and yarn.lock files
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install

# Copy all files
COPY . .

# Build the Vue.js app
RUN yarn build

# Stage 2: Serve Vue.js app with Nginx
FROM nginx:1.26.0

# Set ownership and permissions for the HTML directory
RUN chown -R nginx:nginx /usr/share/nginx/html
RUN chmod -R 755 /usr/share/nginx/html

# Copy built Vue.js app from build-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration file to the container
COPY nginx/default.conf /etc/nginx/conf.d/

# Expose port 80
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
