// Serves the public demo at https://eygentic.tech: a Cloudflare Worker that forwards every request to the Modal app
// and streams the answer back. The browser only ever sees eygentic.tech; the Modal app accepts its own modal.run name
// through AGENT_PUBLIC_ALSO_HOSTS and treats https://eygentic.tech as its public origin (AGENT_PUBLIC_URL).
const ORIGIN = 'https://gtmshortlist--gtm-shortlist-agent-web.us-east.modal.run';

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.hostname === 'www.eygentic.tech') {
      url.hostname = 'eygentic.tech';
      return Response.redirect(url.toString(), 301);
    }
    const target = new URL(url.pathname + url.search, ORIGIN);
    const headers = new Headers(request.headers);
    // The visitor's address, for the hourly limit: the app reads the first X-Forwarded-For entry.
    headers.set('X-Forwarded-For', request.headers.get('CF-Connecting-IP') || '');
    headers.delete('Host');
    return fetch(target, {
      method: request.method,
      headers,
      body: ['GET', 'HEAD'].includes(request.method) ? undefined : request.body,
      redirect: 'manual',
    });
  },
};
