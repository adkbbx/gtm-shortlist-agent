import { defineConfig } from '@playwright/test';
import { resolve } from 'node:path';

const python = process.platform === 'win32' ? '.venv\\Scripts\\python.exe' : '.venv/bin/python';
const environment = { PYTHONPATH: resolve('src') };
export default defineConfig({
  testDir: './tests/ui', timeout: 45000, fullyParallel: false, workers: 1,
  // Shared CI runners are slower than a laptop; give each check more time there.
  expect: { timeout: process.env.CI ? 15000 : 5000 },
  reporter: process.env.CI ? [['github'], ['list']] : 'list',
  use: { baseURL: 'http://127.0.0.1:8015', trace: 'retain-on-failure' },
  projects: [
    { name: 'laptop', use: { viewport: { width: 1366, height: 900 } } },
    { name: 'phone', use: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } },
  ],
  webServer: [
    // The local agent, for tests/ui/agent.spec.ts.
    { command: `${python} scripts/local_test_server.py`, env: environment, url: 'http://127.0.0.1:8015/api/health', reuseExistingServer: false },
    // The public demo, for tests/ui/agent-public.spec.ts.
    { command: `${python} scripts/public_demo_test_server.py`, env: environment, url: 'http://127.0.0.1:8017/api/health', reuseExistingServer: false },
  ],
});
