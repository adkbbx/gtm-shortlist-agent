// R6: one real search for eygentic.com on the live demo, then "Draft outreach" on its first Shortlisted company: the
// subject, email and LinkedIn note, checked by Muse Spark Open. Starts ONE real search (about $0.55 with the draft).
const { start, BASE } = require('./recorder.cjs');

(async () => {
  const rec = await start('email', process.argv[2]);
  const { page } = rec;
  await page.goto(BASE + '/', { waitUntil: 'networkidle' });
  await page.mouse.move(1500, 780);
  await rec.wait(3500);
  await rec.click(page.getByLabel('Your company website'), { dx: 0.3 });
  await page.keyboard.type('eygentic.com', { delay: 120 });
  await rec.wait(500);
  await rec.click(page.getByRole('group', { name: 'Companies to find' }).getByText('5', { exact: true }));
  await rec.wait(500);
  rec.mark('find');
  await rec.click(page.getByRole('button', { name: 'Find 5 companies' }));
  await page.mouse.move(1500, 780, { steps: 20 });
  const t0 = rec.now();
  let last = '';
  while (rec.now() - t0 < 600) {
    const status = (await page.getByRole('status').first().innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 120);
    if (status && status !== last) { rec.mark('status: ' + status); last = status; }
    if (status.includes('Done:')) break;
    await rec.wait(1000);
  }
  await rec.wait(2500);
  rec.mark('url ' + page.url());
  const card = page.locator('article.agent-row.verdict-shortlisted').first();
  if (!(await card.count())) { rec.mark('no shortlisted company'); await rec.stop(); return; }
  await rec.scrollToShow(card, 260);
  rec.mark('draft-click');
  await rec.click(card.getByRole('button', { name: 'Draft outreach' }));
  const dialog = page.getByRole('dialog', { name: 'First message' });
  await dialog.locator('.agent-email-subject').filter({ hasText: /\S/ }).waitFor({ timeout: 120000 });
  await rec.wait(600);
  rec.mark('email-shown');
  await rec.moveTo(dialog.locator('.agent-email-subject'), { dx: 0.2 });
  await rec.wait(6000);
  rec.mark('linkedin-click');
  await rec.click(dialog.getByRole('tab', { name: 'LinkedIn' }));
  await rec.wait(4500);
  rec.mark('email-tab');
  await rec.click(dialog.getByRole('tab', { name: 'Email' }));
  await rec.wait(2500);
  await rec.stop();
})();
