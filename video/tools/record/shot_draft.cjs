// R6: "Draft outreach" on a Shortlisted company of a real finished search: subject, email and LinkedIn note, checked by
// Muse Spark Open. Runs against the local app holding that search (argv[3], e.g. http://127.0.0.1:8031/?agent=<id>),
// because only the browser that started a search on the public demo may draft for it. One draft: a few cents.
const { start } = require('./recorder.cjs');

(async () => {
  const rec = await start('draft', process.argv[2]);
  const { page } = rec;
  await page.goto(process.argv[3], { waitUntil: 'networkidle' });
  await page.mouse.move(1500, 780);
  await rec.wait(2500);
  const card = page.locator('article.agent-row.verdict-shortlisted').first();
  await rec.scrollToShow(card, 260);
  await rec.wait(800);
  rec.mark('draft-click');
  await rec.click(card.getByRole('button', { name: 'Draft outreach' }));
  const dialog = page.getByRole('dialog', { name: 'First message' });
  await dialog.locator('.agent-email-subject').filter({ hasText: /\S/ }).waitFor({ timeout: 180000 });
  await rec.wait(500);
  rec.mark('email-shown');
  await rec.moveTo(dialog.locator('.agent-email-subject'), { dx: 0.2 });
  await rec.wait(7000);
  rec.mark('linkedin-click');
  await rec.click(dialog.getByRole('tab', { name: 'LinkedIn' }));
  await rec.wait(5000);
  rec.mark('end');
  await rec.stop();
})();
