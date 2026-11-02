import { useId } from 'react';
import type { ReactNode } from 'react';
import { domainOf, quoteLink } from './agent-api';
import type { Company, EvidenceItem, Quote } from './agent-api';

const sourceLabel: { [kind in Quote['source_type']]: string } = {
  own_site: 'Company site', job_post: 'Job post', news: 'News', review: 'Review site',
  competitor_site: 'Competitor site', other: 'Other site', description: 'Your description',
};
const day = (value: string) => new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date(value));
const pathOf = (url: string) => { try { const path = new URL(url).pathname; return path === '/' ? '' : path; } catch { return ''; } };

/** An exact quote. The words link to the source page, scrolled to the quote where the browser supports it. */
export function QuoteBlock({ quote }: { quote: Quote }) {
  // Words a business without a website typed about itself: there is no page to link to.
  if (quote.source_type === 'description') return <figure className="agent-quote">
    <blockquote className="agent-quote-text">“{quote.text}”</blockquote>
    <figcaption><span>From your description</span><span>Written {day(quote.fetched_at)}</span></figcaption>
  </figure>;
  return <figure className="agent-quote">
    <a className="agent-quote-text" href={quoteLink(quote)} target="_blank" rel="noopener noreferrer">“{quote.text}”</a>
    <figcaption>
      <span>{domainOf(quote.url)}{pathOf(quote.url)}</span>
      <span>{sourceLabel[quote.source_type]}{quote.location === 'html' ? ', found in the page code' : ''}</span>
      <span>{quote.published_date ? `Published ${day(quote.published_date)}` : 'Publication date not stated'}</span>
      {quote.open_posting && <span>Job post open when read</span>}
      <span>Read {day(quote.fetched_at)}</span>
    </figcaption>
  </figure>;
}

/** A compact label that opens its quotes and optional edit controls in a native popover. */
export function Chip({ label, tag, quotes, note, off = false, tone = 'neutral', children }: {
  label: string; tag?: string; quotes: Quote[]; note?: string; off?: boolean;
  tone?: 'neutral' | 'good' | 'bad' | 'open'; children?: ReactNode;
}) {
  const id = `chip-${useId().replace(/[^a-zA-Z0-9_-]/g, '')}`;
  return <>
    <button type="button" className={`agent-chip tone-${tone}${off ? ' is-off' : ''}`} popoverTarget={id}
      aria-label={`${label}${tag ? `, ${tag}` : ''}${off ? ', not used' : ''}. Show the quote`}>
      <span className="agent-chip-label">{label}</span>{tag && <span className="agent-chip-tag">{tag}</span>}
    </button>
    <div id={id} popover="auto" className="agent-popover" role="dialog" aria-label={label}>
      <div className="agent-popover-head">
        <p>{label}</p>
        <button type="button" className="agent-popover-close" popoverTarget={id} popoverTargetAction="hide" aria-label="Close">
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="m7 7 10 10M17 7 7 17" /></svg>
        </button>
      </div>
      {quotes.length ? quotes.map((quote, index) => <QuoteBlock key={index} quote={quote} />)
        : <p className="agent-popover-note">{note ?? 'No quote: you added this.'}</p>}
      {quotes.length > 0 && note && <p className="agent-popover-note">{note}</p>}
      {children}
    </div>
  </>;
}

const claimLabel: { [kind in EvidenceItem['claim_type']]: string } = {
  fit: 'Fit', need: 'Need', timing: 'Timing', disqualifier: 'Disqualifier',
};
const decisionLabel = { supports: 'Supports', contradicts: 'Contradicts', insufficient: 'Not enough' } as const;

/** Who judged the quotes: the second Meta model, or the scripted stand-in on synthetic test data. */
export const checkerName = (synthetic: boolean) => synthetic ? 'Checker (synthetic)' : 'Muse Spark Open';
const short = (text: string, limit = 220) => text.length > limit ? `${text.slice(0, limit - 1).trimEnd()}…` : text;

export function EvidenceList({ company, checkName, checker }: { company: Company; checkName: (item: EvidenceItem) => string;
  checker: string }) {
  const decisions = new Map(company.decisions.map(decision => [decision.evidence_id, decision]));
  const supported = company.evidence.filter(item => decisions.get(item.id)?.decision === 'supports' && item.claim_type !== 'disqualifier');
  // The second model's work, in the open: every quote it threw out, with its reason.
  const thrownOut = company.evidence.filter(item => {
    const decision = decisions.get(item.id);
    return decision?.decided_by === 'skeptic' && decision.decision !== 'supports';
  });
  // One chip per check: a check supported by several quotes showed up as repeated chips on a live board.
  const byCheck = new Map<string, EvidenceItem[]>();
  for (const item of supported) {
    const key = `${item.claim_type}:${item.criterion_id}`;
    byCheck.set(key, [...byCheck.get(key) ?? [], item]);
  }
  return <>
    {byCheck.size > 0 && <div className="agent-evidence-chips" aria-label="Supported evidence">
      {[...byCheck.values()].map(items => <Chip key={items[0].id} label={checkName(items[0])} tag={claimLabel[items[0].claim_type]}
        quotes={items.map(item => item.quote)} tone="good" note={`${checker}: ${decisions.get(items[0].id)?.reason || 'supports'}`} />)}
    </div>}
    {thrownOut.length > 0 && <section className="agent-thrown" aria-label={`Thrown out by ${checker}`}>
      <p className="agent-thrown-title">Thrown out by {checker} <span>{thrownOut.length}</span></p>
      <ul>{thrownOut.map(item => {
        const decision = decisions.get(item.id)!;
        return <li key={item.id}>
          <p className="agent-thrown-claim">{claimLabel[item.claim_type]}: {checkName(item)}</p>
          <q className="agent-thrown-quote">{short(item.quote.text)}</q>
          <p className="agent-thrown-why"><span className={`agent-decision ${decision.decision}`}>{decisionLabel[decision.decision]}</span>
            {decision.reason}</p>
        </li>;
      })}</ul>
    </section>}
    {company.evidence.length > 0 && <details className="agent-all-quotes">
      <summary>All checked quotes ({company.evidence.length})</summary>
      <ul>
        {company.evidence.map(item => {
          const decision = decisions.get(item.id);
          return <li key={item.id}>
            <p className="agent-evidence-line"><span className={`agent-decision ${decision?.decision ?? 'insufficient'}`}>
              {decision ? decisionLabel[decision.decision] : 'Not checked'}</span>{claimLabel[item.claim_type]}: {checkName(item)}</p>
            <QuoteBlock quote={item.quote} />
            {decision?.reason && <p className="agent-decision-reason">{decision.decided_by === 'rule' ? 'Rule' : decision.decided_by === 'no_skeptic' ? 'Not reviewed' : checker}: {decision.reason}</p>}
          </li>;
        })}
      </ul>
    </details>}
  </>;
}
