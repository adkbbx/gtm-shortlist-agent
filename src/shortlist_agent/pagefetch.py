"""The readable page from an HTML body the safe fetcher already returned.

Added during the event so the agent keeps a fetched page's raw HTML for its code scan without fetching it twice. It
uses the prototype's fetcher (`shortlist.fetch`, unchanged): `fetch_html` does every network and safety check."""
import hashlib
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from shortlist.domain import Source
from shortlist.fetch import MAX_TEXT, FetchError, activity_links, domain_of, research_links


def page_from_html(current: str, body: bytes, expected_domain: str | None = None) -> Source:
    """The readable page, from the final URL and body fetch_html returned."""
    owner = expected_domain or domain_of(current)
    parsed = urlsplit(current)
    soup = BeautifulSoup(body, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else parsed.hostname
    links = research_links(current, soup)
    activity = activity_links(current, soup)
    for tag in soup(["script", "style", "noscript", "nav", "footer", "svg", "form"]):
        tag.decompose()
    text = "\n".join(line.strip() for line in soup.get_text("\n").splitlines() if line.strip())[:MAX_TEXT]
    if len(text) < 30:
        raise FetchError("Website has insufficient readable text")
    return Source(url=current, company_domain=owner, title=title[:500], text=text,
                  content_hash=hashlib.sha256(body).hexdigest(), research_links=links, activity_links=activity)
