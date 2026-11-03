// R3b: the 31 Oct eygentic.com search on eygentic.tech: ContactMonkey Shortlisted, its open job post quote ("hiring four
// talented, driven Sales Development Representatives") and its checked opening line. Read-only: no new searches.
const { start } = require('./recorder.cjs');

(async () => {
  const rec = await start('contactmonkey', process.argv[2]);
  const { page } = rec;
  await page.goto('https://eygentic.tech/?agent=cde5c7624fb943a68f27ceb49753f5c3', { waitUntil: 'networkidle' });
  await page.mouse.move(1500, 700);
  await rec.wait(3500);
  rec.mark('board');
  await rec.wait(2500);
  const card = page.locator('article.agent-row').filter({ has: page.getByRole('heading', { name: 'contactmonkey.com' }) }).first();
  rec.mark('details-click');
  await rec.click(card.getByRole('button', { name: 'Details' }));
  await rec.wait(1200);
  await rec.scrollToShow(card, 90);
  rec.mark('open');
  await rec.wait(2500);
  const chip = card.getByRole('button', { name: /^Hiring SDRs or outbound sales reps/ });
  await chip.scrollIntoViewIfNeeded();
  rec.mark('chip-click');
  await rec.click(chip);
  await rec.wait(5000);
  rec.mark('popover-close');
  await page.keyboard.press('Escape');
  await rec.wait(800);
  await rec.moveTo(card.getByRole('button', { name: 'Copy opening line' }));
  rec.mark('opener');
  await rec.wait(5000);
  await rec.stop();
})();
