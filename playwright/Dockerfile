# Use official Playwright image with dependencies
FROM mcr.microsoft.com/playwright:v1.43.0-jammy

WORKDIR /app

# Copy the package.json inside the playwright folder
COPY playwright/package.json ./

RUN npm install

# Copy the rest of the playwright folder
COPY playwright/. .

# Disable Chromium sandbox
ENV PLAYWRIGHT_CHROMIUM_NO_SANDBOX=true

CMD ["node", "render_canva.js"]
