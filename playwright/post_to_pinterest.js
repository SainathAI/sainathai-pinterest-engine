const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
    const email = process.env.PINTEREST_EMAIL;
    const password = process.env.PINTEREST_PASSWORD;

    if (!email || !password) {
        console.error("Missing credentials");
        process.exit(1);
    }

    const imagePath = process.argv[2];   // path to image from HF output
    const title = process.argv[3];
    const desc = process.argv[4];

    if (!imagePath || !title || !desc) {
        console.error("Usage: node post_to_pinterest.js <imagePath> <title> <desc>");
        process.exit(1);
    }

    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    // 1. Go to Pinterest login
    await page.goto("https://www.pinterest.com/login/");

    // 2. Fill email + password
    await page.fill('input[type="email"]', email);
    await page.fill('input[type="password"]', password);
    await page.click('button[type="submit"]');
    await page.waitForTimeout(5000);

    // 3. Go to Create Pin page
    await page.goto("https://www.pinterest.com/pin-builder/");
    await page.waitForSelector('input[type="file"]');

    // 4. Upload image
    const inputUpload = await page.$('input[type="file"]');
    await inputUpload.setInputFiles(imagePath);

    // 5. Add title + description
    await page.fill('textarea[data-test-id="pin-builder-title"]', title);
    await page.fill('textarea[data-test-id="pin-builder-description"]', desc);

    // 6. Select first board automatically
    await page.click('[data-test-id="board-dropdown-select-button"]');
    await page.waitForTimeout(1500);
    await page.click('[data-test-id="board-dropdown-item"]:nth-child(1)');

    // 7. Publish
    await page.click('[data-test-id="pin-builder-create-button"]');
    await page.waitForTimeout(4000);

    console.log("Pin Published Successfully!");
    await browser.close();
})();
