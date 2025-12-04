# Use official Playwright image with dependencies
FROM mcr.microsoft.com/playwright:v1.43.0-jammy

WORKDIR /app

# Copy package.json (for npm install)
COPY package.json package-lock.json* ./

RUN npm install

# Copy the rest of the project files
COPY . .

# Disable Chromium sandbox (important for hosting platforms)
ENV PLAYWRIGHT_CHROMIUM_NO_SANDBOX=true

# Expose no port because this is a worker script
CMD ["node", "render_canva.js"]
