import { useEffect, useId, useRef, useState, type KeyboardEvent } from 'react';

/** A company the visitor may mean, from Brandfetch's public search. */
type Match = { name: string; domain: string; icon: string | null };

// Brandfetch's public client ID (never a secret), which the server puts in the page; empty means no suggestions.
const clientId = () =>
  document.querySelector<HTMLMetaElement>('meta[name="shortlist-company-suggestions-client-id"]')?.content.trim() ?? '';
// Someone typing an address already knows the site: only a plain name is looked up.
const typingAName = (text: string) => text.length >= 2 && !/[./:]/.test(text);
const DOMAIN = /^[a-z0-9-]+(?:\.[a-z0-9-]+)+$/;

async function search(query: string, id: string, signal: AbortSignal): Promise<Match[]> {
  const response = await fetch(`https://api.brandfetch.io/v2/search/${encodeURIComponent(query)}?c=${encodeURIComponent(id)}`,
    { signal, referrerPolicy: 'origin' });
  if (!response.ok) return [];
  const found: unknown = await response.json();
  if (!Array.isArray(found)) return [];
  const seen = new Set<string>();
  return found.flatMap(item => {
    const domain = typeof item?.domain === 'string' ? item.domain.trim().toLowerCase() : '';
    if (!DOMAIN.test(domain) || seen.has(domain)) return [];
    seen.add(domain);
    const name = typeof item.name === 'string' && item.name.trim() ? item.name.trim() : domain;
    const icon = typeof item.icon === 'string' && item.icon.startsWith('https://cdn.brandfetch.io/') ? item.icon : null;
    return [{ name, domain, icon }];
  }).slice(0, 6);
}

/** A suggestion's logo, or its first letter when there is none or it does not load. */
function OptionIcon({ match }: { match: Match }) {
  const [failed, setFailed] = useState(false);
  return <span className="company-option-icon" aria-hidden="true">
    {match.icon && !failed ? <img src={match.icon} alt="" referrerPolicy="no-referrer" onError={() => setFailed(true)} />
      : match.name.slice(0, 1).toUpperCase()}
  </span>;
}

/** The website field on the start page. Typing a company name offers matching companies (Brandfetch); choosing one
    fills in its website. A combobox for screen readers: arrows move, Enter chooses, Escape closes. */
export function WebsiteField({ value, onChange, disabled, label, placeholder, inputId = 'website' }: {
  value: string; onChange: (value: string) => void; disabled: boolean; label: string; placeholder: string; inputId?: string;
}) {
  const listId = useId();
  const [matches, setMatches] = useState<Match[]>([]);
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(-1);
  const chosen = useRef('');
  useEffect(() => {
    const query = value.trim();
    const id = clientId();
    if (!id || !typingAName(query) || query === chosen.current) { setMatches([]); setOpen(false); return; }
    const controller = new AbortController();
    const wait = window.setTimeout(() => {
      search(query, id, controller.signal)
        .then(found => { setMatches(found); setActive(-1); setOpen(found.length > 0); })
        .catch(() => { /* suggestions are optional: a failed lookup leaves the plain field */ });
    }, 220);
    return () => { window.clearTimeout(wait); controller.abort(); };
  }, [value]);
  const choose = (match: Match) => {
    chosen.current = match.domain;
    onChange(match.domain);
    setOpen(false);
    setMatches([]);
  };
  const keys = (event: KeyboardEvent<HTMLInputElement>) => {
    if (!matches.length) return;
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      const step = event.key === 'ArrowDown' ? 1 : -1;
      setOpen(true);
      setActive(current => (current + step + matches.length) % matches.length);
    } else if (event.key === 'Enter' && open && active >= 0) {
      event.preventDefault();
      choose(matches[active]);
    } else if (event.key === 'Escape' && open) {
      event.preventDefault();
      setOpen(false);
    }
  };
  const showing = open && matches.length > 0;
  return <div className="company-search">
    <input id={inputId} type="text" inputMode="url" autoComplete="off" autoCapitalize="none" spellCheck={false}
      role="combobox" aria-expanded={showing} aria-controls={listId} aria-autocomplete="list"
      aria-activedescendant={showing && active >= 0 ? `${listId}-${active}` : undefined}
      aria-label={label} placeholder={placeholder} value={value} disabled={disabled}
      onChange={event => { chosen.current = ''; onChange(event.target.value); }} onKeyDown={keys}
      onBlur={() => setOpen(false)} />
    {showing && <div className="company-options">
      <ul id={listId} role="listbox" aria-label="Matching companies">
        {matches.map((match, index) =>
          <li key={match.domain} id={`${listId}-${index}`} role="option" aria-selected={index === active}
            className={index === active ? 'is-active' : undefined}
            onMouseDown={event => event.preventDefault()} onMouseEnter={() => setActive(index)} onClick={() => choose(match)}>
            <OptionIcon match={match} />
            <span className="company-option-name">{match.name}</span>
            <span className="company-option-domain">{match.domain}</span>
          </li>)}
      </ul>
    </div>}
  </div>;
}
