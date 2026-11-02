// R3 + R5: the finished eygentic.com example. ThriveCart's quote and opening line, Storable's rejection, the Needs a
// look column with Tenstreet's thrown-out quote, then back to the header stats. No new searches.
const { start, BASE } = require('./recorder.cjs');

(async () => {
  const rec = await start('example', process.argv[2]);
  const { page } = rec;
  await page.goto(BASE + '/?agent=ddb51670fc004142b90bce02f42447f9', { waitUntil: 'networkidle' });
  await page.mouse.move(1500, 700);
  await rec.wait(1200);
  rec.mark('board');
  await rec.wait(2500);

  const thrive = page.locator('article.agent-row').filter({ has: page.getByRole('heading', { name: 'thrivecart.com' }) }).first();
  rec.mark('thrive-details');
  await rec.click(thrive.getByRole('button', { name: 'Details' }));
  await rec.wait(1200);
  await rec.scrollToShow(thrive, 90);
  rec.mark('thrive-open');
  await rec.wait(2500);
  const chip = thrive.getByRole('button', { name: /Preparing to hire first SDRs/ });
  await chip.scrollIntoViewIfNeeded();
  rec.mark('thrive-chip');
  await rec.click(chip);
  await rec.wait(4000);
  rec.mark('thrive-popover-close');
  await page.keyboard.press('Escape');
  await rec.wait(800);
  const opener = page.getByRole('button', { name: 'Copy opening line' });
  await rec.moveTo(opener);
  rec.mark('thrive-opener');
  await rec.wait(3500);

  const storable = page.locator('article.agent-row').filter({ has: page.getByRole('heading', { name: 'storable.com' }) }).first();
  await rec.scrollToShow(storable, 200);
  rec.mark('storable');
  await rec.wait(1500);
  await rec.click(storable.getByRole('button', { name: 'Details' }));
  await rec.wait(900);
  const employs = storable.locator('.agent-quote-text', { hasText: '800 employees' }).first();
  await rec.scrollToShow(employs, 300);
  rec.mark('storable-quote');
  await rec.moveTo(employs, { dx: 0.3 });
  await rec.wait(4500);

  const tenstreet = page.locator('article.agent-row').filter({ has: page.getByRole('heading', { name: 'Tenstreet' }) }).first();
  await rec.scrollToShow(tenstreet, 160);
  rec.mark('needs-look');
  await rec.wait(1500);
  await rec.click(tenstreet.getByRole('button', { name: 'Details' }));
  await rec.wait(1000);
  const thrown = tenstreet.getByRole('region', { name: /Thrown out by/ });
  await rec.scrollToShow(thrown, 160);
  rec.mark('thrown-out');
  await rec.moveTo(thrown, { dy: 0.3 });
  await rec.wait(5000);

  await rec.scrollBy(-6000, { steps: 40 });
  rec.mark('top-stats');
  await rec.moveTo(page.getByText('$0.42').first());
  await rec.wait(3500);
  await rec.stop();
})();

