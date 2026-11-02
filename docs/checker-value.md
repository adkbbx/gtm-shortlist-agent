# What the checker changes

Measured on 17 saved live searches (82 companies researched), with no model calls: each search's evidence is judged again as if the checker accepted every quote found on its page, and the same verdict code runs.

- Muse Spark Open judged **354 quotes**: kept 234, found 99 too weak and 21 contradicted (**120 thrown out, 34%**).
- It changed **31 of 82 verdicts (38%)**.
- Without it, **6 companies would have been Shortlisted** on quotes it threw out.
- Without it, **25 companies would have been Rejected**, 6 of them companies it Shortlisted. Without a judge, the verdict code counts every quote filed under a disqualifier against the company: an integration read as using a competitor, but also quotes the agent gathered to show the opposite (that the company is still operating, or within the seller's size range). The checker decides which way each quote points, so this number shows how much the design relies on it, not only mistakes it caught.

| Seller | Company | With the checker | Without it |
|---|---|---|---|
| Bookeeping software for independent cafe's | coffeebuddy.in | Needs a look | Rejected |
| Bookeeping software for independent cafe's | manamchocolate.com | Shortlisted | Rejected |
| https://vanta.com/ | omnichat.ai | Shortlisted | Rejected |
| https://vanta.com/ | mattermost.com | Shortlisted | Rejected |
| https://eygentic.com/ | docsumo.com | Needs a look | Rejected |
| https://eygentic.com/ | deliverect.com | Needs a look | Rejected |
| https://eygentic.com/ | chefrobotics.ai | Needs a look | Rejected |
| https://eygentic.com/ | peoplegrove.com | Needs a look | Rejected |
| https://eygentic.com/ | thrivecart.com | Needs a look | Shortlisted |
| https://eygentic.com/ | omnichat.com | Needs a look | Shortlisted |
| https://eygentic.com/ | logixboard.com | Needs a look | Rejected |
| https://eygentic.com/ | sunlightai.com | Needs a look | Rejected |
| https://crisp.chat/ | sharewillow.com | Needs a look | Rejected |
| https://crisp.chat/ | spinquest.com | Shortlisted | Rejected |
| https://eygentic.com/ | decagon.ai | Needs a look | Rejected |
| https://eygentic.com/ | tenstreet.com | Needs a look | Rejected |
| https://eygentic.com/ | setsales.co | Needs a look | Rejected |
| https://eygentic.com/ | facets.cloud | Needs a look | Shortlisted |
| https://eygentic.com/ | reach.industries | Needs a look | Shortlisted |
| https://vanta.com/ | fieldnation.com | Needs a look | Shortlisted |
| https://vanta.com/ | hhaexchange.com | Needs a look | Rejected |
| https://vanta.com/ | rescale.com | Needs a look | Rejected |
| https://vanta.com/ | airwallex.com | Needs a look | Rejected |
| https://crisp.chat/ | emilabs.ai | Needs a look | Shortlisted |
| https://crisp.chat/ | wingassistant.com | Needs a look | Rejected |
| https://crisp.chat/ | journeyclinical.com | Needs a look | Rejected |
| https://vanta.com/ | mintive.com | Needs a look | Rejected |
| https://vanta.com/ | mercury.com | Needs a look | Rejected |
| An AI phone receptionist for dental clinics | artisandental.com | Needs a look | Rejected |
| An AI phone receptionist for dental clinics | austindentalspa.com | Shortlisted | Rejected |
| An AI phone receptionist for dental clinics | pearldentalarts.com | Shortlisted | Rejected |

## Quotes it threw out (8 of them: disqualifiers it contradicted first, then need and timing)

- **manamchocolate.com** (disqualifier, own site): "Your cart is empty"
  - Claim: Site is active with shopping cart and products for sale
  - Checker (contradicts): Cart text shows active e-commerce site, indicating it is still operating not closed or parked.
- **omnichat.ai** (disqualifier, news): "US
$10 million Series A funding round led by
Openspace Capital"
  - Claim: Company is Series A stage within target size range
  - Checker (contradicts): Series A $10M shows early-stage startup within 1-8000 people pre-seed to public range, not much larger/later-stage.
- **mattermost.com** (disqualifier, job post): "Unique scope: Own the compliance program end to end across both federal and commercial markets at a high-growth Series B company"
  - Claim: Mattermost describes itself as a high-growth Series B company.
  - Checker (contradicts): Quote identifies company as Series B, which is within 1-8000 people pre-seed to public range, not disqualifyingly large.
- **docsumo.com** (disqualifier, job post): "We're a hybrid team in the USA, India and Nepal building Docsumo, the intelligent document processing platform lenders, insurers and AP teams use every day."
  - Claim: Docsumo is still operating with an active team
  - Checker (contradicts): Quote describes active hybrid team building Docsumo platform used every day, indicating ongoing operation.
- **deliverect.com** (disqualifier, news): "Deliverect supports more than 80,000 locations worldwide with over 1,000 certified technology integrations."
  - Claim: Deliverect is still operating with live platform and partnerships.
  - Checker (contradicts): Quote shows active operations supporting 80,000 locations, contradicting no-longer-operating status.
- **chefrobotics.ai** (disqualifier, own site): "Chef robots are deployed at more than a dozen customer facilities across the US, Canada, and Europe."
  - Claim: Company is operating with robots deployed at customer facilities
  - Checker (contradicts): Quote shows active deployments at many facilities, indicating company is still operating.
- **peoplegrove.com** (disqualifier, own site): "PeopleGrove announces new capabilities in the CORE for Education Ecosystem, including native field encounter videos, enhanced digital binders, and integrated competency management powered by responsible AI."
  - Claim: PeopleGrove is still operating with new product announcements
  - Checker (contradicts): Quote announces new product capabilities in 2026, showing company is still operating.
- **logixboard.com** (disqualifier, own site): "$50M in venture capital, 100+ people, and customers in 15 countries."
  - Claim: Logixboard describes itself as 100+ people with $50M in venture capital
  - Checker (contradicts): 100+ people and $50M VC indicates growth-stage mid-market size, not much larger than the target profile.
