import { useEffect, useRef, useState } from 'react';

// One request per domain per page load, shared by every icon showing it.
const asked = new Map<string, Promise<{ url: string | null; placeholder: boolean }>>();
const isDomain = (value?: string) => Boolean(value && /^[a-z0-9-]+(?:\.[a-z0-9-]+)+$/i.test(value));

function declaredIcon(domain: string) {
  let pending = asked.get(domain);
  if (!pending) {
    pending = fetch(`/api/site-icon/${encodeURIComponent(domain)}`)
      .then(response => (response.ok ? response.json() : { url: null, placeholder: false }))
      .then(data => {
        const url = typeof data?.url === 'string' && data.url.startsWith('https://') ? data.url : null;
        return { url, placeholder: data?.placeholder === true };
      })
      .catch(() => ({ url: null, placeholder: false }));
    asked.set(domain, pending);
  }
  return pending;
}

/** A company's icon: the one its homepage declares, else its /favicon.ico, else the fallback letter. A search for a
    business without a website is labelled by its name, which has no icon. Asks only once the icon is on screen. */
export function SiteIcon({ domain, fallback, className, lookup = false }: {
  domain?: string; fallback: string; className: string; lookup?: boolean;
}) {
  const host = useRef<HTMLSpanElement>(null);
  const [seen, setSeen] = useState(false);
  const [declared, setDeclared] = useState<{ domain: string; url: string | null; placeholder: boolean } | null>(null);
  const [failed, setFailed] = useState<ReadonlySet<string>>(() => new Set());
  const known = isDomain(domain) ? domain : undefined;
  useEffect(() => {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) { setSeen(true); observer.disconnect(); }
    });
    if (host.current) observer.observe(host.current);
    return () => observer.disconnect();
  }, []);
  useEffect(() => {
    if (!seen || !known || !lookup) return;
    let live = true;
    void declaredIcon(known).then(found => { if (live) setDeclared({ domain: known, ...found }); });
    return () => { live = false; };
  }, [seen, known, lookup]);
  const answer = declared?.domain === known ? declared : null;
  const waiting = Boolean(lookup && known && !answer);
  // A site builder's blank stand-in icon is served at /favicon.ico too, so skip the guess then.
  const guess = known && !answer?.placeholder ? `https://${known}/favicon.ico` : undefined;
  const source = waiting ? undefined : [answer?.url ?? undefined, guess].find(url => url && !failed.has(url));
  return <span ref={host} className={`site-icon ${className}`} aria-hidden="true">
    {source ? <img src={source} alt="" referrerPolicy="no-referrer"
      onError={() => setFailed(previous => new Set([...previous, source]))} /> : fallback}
  </span>;
}
