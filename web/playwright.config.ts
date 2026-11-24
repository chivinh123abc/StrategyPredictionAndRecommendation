import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  timeout: 180_000,
  expect: { timeout: 30_000 },
  workers: 1,
  reporter: [['list']],
  outputDir: '../reports/ui_lane_revision/playwright-results',
  use: { baseURL: process.env.DRAFT_UI_URL || 'http://127.0.0.1:8000', actionTimeout: 30_000, channel: 'msedge', headless: true, viewport: { width: 1512, height: 1100 }, locale: 'vi-VN' },
})
