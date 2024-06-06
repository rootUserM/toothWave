# Use the official Nginx image from the Docker Hub
FROM nginx:1.26.0

RUN chown -R nginx:nginx /usr/share/nginx/html
RUN chmod -R 755 /usr/share/nginx/html

# Copy the custom Nginx configuration file to the container
COPY conf.d/default.conf /etc/nginx/conf.d/

# Copy website content to the container (optional)
COPY html /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
