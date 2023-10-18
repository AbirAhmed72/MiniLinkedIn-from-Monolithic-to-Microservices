# Use an official Node runtime as a parent image
FROM node:16-slim

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the local source files to the container
COPY . .

# Build the production-ready frontend application
RUN npm run build

# Expose the port your app runs on
EXPOSE 3000

# Set the command to run the application
CMD ["npm", "start"]
