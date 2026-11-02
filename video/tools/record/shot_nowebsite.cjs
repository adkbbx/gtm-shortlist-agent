// R4: the "I don't have a website" popup, answers typed slowly, never submitted.
const { start, BASE } = require('./recorder.cjs');

(async () => {
  const rec = await start('nowebsite', process.argv[2]);
  const { page } = rec;
  await page.goto(BASE + '/', { waitUntil: 'networkidle' });
  await page.mouse.move(1500, 780);
  await rec.wait(1500);
  rec.mark('start');
  await rec.click(page.getByRole('button', { name: "I don't have a website" }));
  const dialog = page.getByRole('dialog', { name: 'Describe your business' });
  await dialog.waitFor();
  await rec.wait(900);
  rec.mark('dialog');
  const type = async (label, text) => {
    await rec.click(dialog.getByLabel(label));
    await page.keyboard.type(text, { delay: 38 });
    await rec.wait(500);
  };
  await type('What do you sell or want to build?', 'An AI phone receptionist for dental clinics. It answers every call and books appointments.');
  rec.mark('sell-typed');
  await type('Who is your ideal customer?', 'Independent dental clinics with 1 to 20 locations.');
  rec.mark('buyer-typed');
  await type(/Which markets or geography/, 'United States');
  rec.mark('markets-typed');
  await rec.moveTo(dialog.getByRole('button', { name: /^Find/ }));
  await rec.wait(2500);
  await rec.stop();
})();
