/* Cloudflare Turnstile for the public demo: loaded only when a search starts and the server has a site key. It stays
   out of sight unless Cloudflare needs the visitor to act; the server checks the token before any model call. */
type Turnstile = {
  render(host: HTMLElement, options: Record<string, unknown>): string;
  remove(widget: string): void;
};
declare global { interface Window { turnstile?: Turnstile } }

let script: Promise<Turnstile> | null = null;

function loadTurnstile(): Promise<Turnstile> {
  script ??= new Promise<Turnstile>((resolve, reject) => {
    if (window.turnstile) return resolve(window.turnstile);
    const tag = Object.assign(document.createElement('script'), {
      src: 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit', async: true });
    tag.onload = () => (window.turnstile ? resolve(window.turnstile) : reject(new Error('The browser check could not start.')));
    tag.onerror = () => { script = null; tag.remove(); reject(new Error('The browser check could not load. Check your connection and try again.')); };
    document.head.append(tag);
  });
  return script;
}

/** One token for one search, from a widget drawn into `host`. */
export async function turnstileToken(siteKey: string, host: HTMLElement): Promise<string> {
  const turnstile = await loadTurnstile();
  return new Promise<string>((resolve, reject) => {
    let widget = '';
    const finish = () => window.setTimeout(() => { if (widget) turnstile.remove(widget); });
    widget = turnstile.render(host, {
      sitekey: siteKey, appearance: 'interaction-only', action: 'search',
      callback: (token: string) => { finish(); resolve(token); },
      'error-callback': () => { finish(); reject(new Error('The browser check did not pass. Reload the page and try again.')); },
      'expired-callback': () => { finish(); reject(new Error('The browser check expired. Try again.')); },
    });
  });
}
