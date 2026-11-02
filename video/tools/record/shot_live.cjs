// R1 + R2: the start page, typing eygentic.com, choosing 5, pressing Find, then the live board until it finishes.
// This starts ONE real search on the public demo (about $0.40 of model calls).
const { start, BASE } = require('./recorder.cjs');

(async () => {
  const rec = await start('live', process.argv[2]);
  const { page } = rec;
  await page.goto(BASE + '/', { waitUntil: 'networkidle' });
  await page.mouse.move(1500, 860);
  rec.mark('hero');
  await rec.wait(4000);
  const field = page.getByLabel('Your company website');
  await rec.click(field, { dx: 0.3 });
  rec.mark('typing');
  await page.keyboard.type('eygentic.com', { delay: 120 });
  await rec.wait(700);
  await rec.click(page.getByRole('group', { name: 'Companies to find' }).getByText('5', { exact: true }));
  await rec.wait(700);
  const find = page.getByRole('button', { name: 'Find 5 companies' });
  await rec.moveTo(find);
  await rec.wait(400);
  rec.mark('find');
  await rec.click(find);
  await page.mouse.move(1500, 860, { steps: 20 });
  let last = '';
  const t0 = rec.now();
  while (rec.now() - t0 < 600) {
    const status = (await page.getByRole('status').first().innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 120);
    if (status && status !== last) { rec.mark('status: ' + status); last = status; }
    if (status.includes('Done:')) break;
    await rec.wait(1000);
  }
  await rec.wait(3000);
  rec.mark('url ' + page.url());
  await rec.stop();
})();
