"""Recruiting, staffing and outsourced sales firms: their job posts are written for clients, so they are not their need."""
import re

# Recruiting and staffing firms post roles for their clients, and outsourced sales teams sell for theirs: a hiring
# signal on their site belongs to another company. "Staffing" alone is not enough: scheduling software says it too.
STAFFING = re.compile(
    r"\b(?:recruit(?:ing|ment) (?:agenc(?:y|ies)|firms?|compan(?:y|ies)|partners?|services|solutions)"
    r"|staffing (?:agenc(?:y|ies)|firms?|compan(?:y|ies)|services|solutions|partners?)"
    r"|talent (?:acquisition|placement|sourcing) (?:agenc(?:y|ies)|firms?|partners?|services|solutions)"
    r"|executive search|head-?hunt(?:er|ers|ing)|recruitment process outsourcing|RPO provider"
    r"|(?:outsourced|fractional|dedicated) (?:SDRs?|BDRs?|sales (?:development|reps?|teams?))"
    r"|(?:SDRs?|BDRs?|sales development|lead generation|appointment setting) (?:as a service|agenc(?:y|ies)|services))\b",
    re.IGNORECASE)
# A posting a recruiter or agency wrote for someone else: its need belongs to the unnamed client, not the poster.
CLIENT_ROLE = re.compile(r"\b(?:our|my|a) (?:valued |confidential )?client(?:'s)?\b|\bon behalf of (?:our|a|one of our) "
                         r"(?:client|customer|partner)s?\b|\bconfidential (?:client|company|search)\b", re.IGNORECASE)
RECRUITING_BUYER = re.compile(r"\b(?:recruit\w*|staffing|hiring teams?|talent acquisition|headhunt\w*)\b", re.IGNORECASE)


def staffing_firm(text: str) -> bool:
    """Whether a page title or opening line says the company recruits, staffs or sells for other companies."""
    head = re.split(r"\b(?:for|to)\b", text, maxsplit=1, flags=re.IGNORECASE)[0]
    head = re.sub(r"\b(?:recruit\w*|staffing|hiring|talent)\s+(?:management\s+)?(?:software|platform|app|tool|system|crm|ats)\b",
                  "", head, flags=re.IGNORECASE)
    return bool(STAFFING.search(head))
