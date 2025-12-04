# Use Playwright base with browsers installed
FROM mcr.microsoft.com/playwright:v1.43.0-jammy

# Create app directory and set as workdir
WORKDIR /app

# Copy only package files first (for caching)
COPY ./playwright/package*.json ./

# Install dependencies (production)
RUN npm install --production

# Copy app source from playwright directory into container
COPY ./playwright ./

# Ensure node_modules binaries are available
ENV PATH /app/node_modules/.bin:$PATH

# Expose port (optional; container runtime will map)
EXPOSE 3000

# Default start command
CMD ["node", "server/index.js"]
