# Use an official Nginx image as the base image
FROM nginx:latest

# Copy the custom nginx.conf file to the container
COPY default.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for incoming HTTP traffic
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
