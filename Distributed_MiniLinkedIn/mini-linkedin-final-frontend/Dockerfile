#Distributed_MiniLinkedIn/nginx/Dockerfile

FROM nginx:latest

WORKDIR /var/www/html

COPY ./build .

# Copy the custom nginx.conf file to the container
COPY default.conf /etc/nginx/conf.d/default.conf
# Copy the frontend build files to the container

# Expose port 80 for incoming HTTP traffic
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
