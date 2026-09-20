# Workflow 01: Competitor Intelligence and Market Monitoring

## Objective
For any business (fashion, quick commerce, healthcare, tech, anything), identify its major competitors, keep watching them every day, and turn what changes into a short morning report: what competitors are doing, what is working for them, and what our business should do about it.

The analysis covers three lenses and ranks findings by which is likely to have the greater impact on our business performance:
- **Product / quality:** search, catalog, UX, app quality, delivery experience
- **Strategy:** pricing, growth, market share, funding, expansion, partnerships
- **Expansion / whitespace:** new arenas the business could enter or deepen, found by watching big rivals moving into adjacent areas and small, unusual startups solving an adjacent problem in a new way

## Required inputs
1. A business profile at `profiles/<business_slug>.md` (copy `profiles/_template.md`). Existing: `profiles/tata_1mg.md`.
2. Report recipient and schedule, set in `.env`: `REPORT_EMAIL_TO`, `REPORT_TIMEZONE=Asia/Kolkata`, `REPORT_SEND_HOUR=9`.
3. Budget: **free sources only** until the owner says otherwise.

To run for a new business, add a profile and start at Phase 1. Nothing in the tools should be hard-coded to one industry.

## Safety rules for data collection (apply to every tool)
- Public pages only. Never log in, never bypass a login wall, paywall, CAPTCHA or bot detection.
- Read `robots.txt` first and skip anything it disallows.
- Rate limit: at most 1 request per 3 seconds per domain, a descriptive User-Agent, exponential backoff on 429/5xx, stop on repeated blocks.
- Prefer official or structured sources (RSS, sitemaps, public APIs, app store listings) over scraping HTML.
- Do not collect personal data. Store only what the analysis needs.
- If a site's terms clearly forbid automated access, record it in the Learnings log and use another source.

## Phase 1: Understand the business and discover competitors (one-time, refresh quarterly)
1. Read the profile. Ask the owner about any gap that would change the research.
2. Research competitors with web search, in tiers:
   - **Direct:** same customer, same offering
   - **Indirect / adjacent:** different offering, same customer need, or a platform expanding into this space
   - **Emerging:** new entrants and funded startups
   - **Innovators:** small or early-stage players (a handful of people, pre-seed to seed) whose product is unusual, even if they are not yet a real competitor. They are tracked for ideas and for the arenas they point to, not for market share.
3. For each competitor record: name, tier, business line it competes in, website, app names/URLs, social handles, one-line positioning, and evidence for why it is a competitor.
4. Verify every competitor with a live source. A competitor from memory is a hypothesis until confirmed.
5. Confirm the final list with the owner (aim for 5 to 10 that matter most, not 30).

Output: competitor master list, drafted in `.tmp/` and, once the owner confirms it, saved as `profiles/<business_slug>_competitors.md` (durable, so the scheduled run can read it).

## Phase 1b: Innovator radar and expansion arenas (one-time, refresh monthly)
Big competitors show where the market is; small innovators show where it is going.
1. From the profile, list the business's **current arenas** and **candidate adjacent arenas** (the profile's "Expansion arenas" section). Ask the owner if the profile has none.
2. For each arena, search for small or early-stage startups doing something different: funding announcements (pre-seed, seed), accelerator batches, launch posts, "startups building X" articles, awards and demo-day lists.
3. Record for each innovator: what it does in one line, what is unusual about it, founding year and location, funding and investors, traction evidence (customers, pilots, users), and the arena it points to.
4. Judge fit for our business: do we already hold an asset that would let us do this better (customers, data, brand, supply chain, doctors/sellers/partners)? Decide **build, partner, acquire, or ignore**, with a reason.
5. Keep a running shortlist of about 5 to 10 innovators, and drop ones that go quiet for 6 months.

Innovators do not need the daily monitoring the main competitors get; a weekly check is enough, but a funding round or launch is reported the day it is found.

## Phase 2: Daily collection (free sources)
Tool names below are planned, not yet built. Check `tools/` before creating any.

| Signal | Free source | Planned tool |
|---|---|---|
| News, funding, launches, leadership | Google News RSS per competitor, company blogs and press pages | `tools/collect_news.py` |
| Website and offer changes (homepage, offers, pricing pages) | Public page fetch, content hash, diff against last snapshot | `tools/snapshot_pages.py` |
| Catalog and product growth | Public sitemap diff (new and removed URLs) | `tools/diff_sitemaps.py` |
| App ratings and review themes | Google Play listing and reviews (`google-play-scraper`), Apple iTunes lookup/RSS | `tools/collect_app_data.py` |
| Product-level prices for a fixed basket | Public product pages, only where robots.txt allows | `tools/check_price_basket.py` |
| Search interest and brand demand | Google Trends (`pytrends`, unofficial, may be flaky) | `tools/collect_trends.py` |
| Customer sentiment | Reddit public search, public forums | `tools/collect_sentiment.py` |
| Hiring signals | Public careers pages | `tools/collect_jobs.py` |
| Site history | Wayback Machine CDX API | used ad hoc |
| Innovators: funding, launches, "startups building X" | Google News RSS for arena keywords plus "startup raises", startup-news RSS feeds (Inc42, Entrackr, YourStory), accelerator directories (e.g. Y Combinator), Product Hunt, Hacker News | `tools/collect_innovators.py` |

Each tool writes structured JSON to `.tmp/<business_slug>/<date>/`. A tool that fails must say so in its output rather than silently returning nothing.

## Phase 3: Change detection and history
- Compare today's snapshot to the previous one and keep only real changes.
- History is **not** disposable: baselines are needed tomorrow. Keep them in the cloud location chosen under "Open decisions", not in `.tmp/`.
- First run only builds the baseline. The first useful daily report is the second run.

## Phase 4: Analysis (the agent's job)
For each change or pattern, decide:
1. **What happened**, with the source link.
2. **Why it likely matters** and what appears to be working for the competitor (evidence, not guesses).
3. **Lens:** Product/quality, Strategy, or Expansion. For Expansion items also state: the arena, the unmet need, which of our existing assets give us an edge, and build / partner / acquire / ignore.
4. **Impact on us:** High / Medium / Low, based on how directly it affects our revenue, retention or acquisition, and how many of our customers it touches.
5. **Confidence:** High / Medium / Low, based on source quality. Label inference as inference.
6. **Suggested action** for our business, or "monitor" if there is nothing to do yet.

Rank by impact, then confidence, then recency. Cap the daily email at the top 5 items plus a short "also noted" list.

Weekly (Mondays) add a trend section and an **Innovator spotlight**: one small startup worth knowing about this week, what is unusual about it, and what it suggests for our expansion. Monthly (first of the month) add a gap analysis: where competitors are ahead of us, where we are ahead, and 3 to 5 recommended improvements, plus an **Expansion map**: each current and candidate arena, who is moving in it (big and small), and the best build / partner / acquire / ignore call.

## Phase 5: Deliver
- **Daily email at 09:00 IST (03:30 UTC)** to `REPORT_EMAIL_TO`. Subject format: `[<Business>] Competitor brief, <date>`.
- Email structure: one-line summary, top items (what / why it matters / lens / impact / action), source links, data-quality notes (which sources failed today).
- If nothing meaningful changed, send a short "quiet day" note. Do not pad.
- Email body rules: the body is the brief itself (summary and top findings), not a table of contents for an attachment. No project status (what is built, pushed or scheduled), no tool or sender signature lines. Anything about how the system works goes in chat or this workflow, not in the reader's inbox.
- Supporting data (competitor master list, price basket history, change log) lives in Google Drive.
- Do not send the first real email until the owner has approved a sample of it.
- **Archive every sent email in MongoDB** with `tools/save_email.py` (fields: `company_name`, `date`, `header` (the subject), `content` (the text extracted from the attached PDF, one string, empty if no PDF), `email_content` (the email body, one string)). Only text is stored; the PDF file itself is not kept. Save only after the send succeeds. Needs `MONGODB_URI` in `.env` (an Atlas connection string). The archive also lets later runs check what was already reported.

## Edge cases
- **Source blocks or rate-limits us:** back off, skip that source today, note it in the email's data-quality section, do not retry aggressively.
- **Site layout changed and a scraper returns nothing:** flag it, fix the tool, retest, log it below.
- **Unverifiable claim or rumor:** include only if impact is high, labelled "unconfirmed".
- **A paid tool would be much better:** note it once in the monthly report with the specific gap it would fill. Do not use it.
- **Tool that calls a paid API:** ask the owner before running (per CLAUDE.md).

## Open decisions
1. **Where the daily job runs: DECIDED (2026-09-19), scheduled cloud agent (routine).** Cron is UTC, so 09:00 IST = `30 3 * * *`. Not created yet. Cloud runs start in a fresh sandbox with a git checkout of a repo and cannot see local files, so setup needs: the project in a GitHub repo, the Gmail and Drive connectors attached, and a self-contained prompt. Cost and usage limits: unconfirmed, check before enabling.
2. **Email sending: RESOLVED 2026-09-20.** The owner disconnected and reconnected the Gmail connector (account aditijain11021@gmail.com) and the send worked; a PDF attachment was delivered to aditijain1100@gmail.com. Cause of the earlier failure: the connector's Google grant lacked send permission, and changing other Google settings did not fix it; only reconnecting the connector did. Mail is sent FROM the connected account (aditijain11021@gmail.com). Original problem for reference: The Gmail connector on the owner's claude.ai account returned "Insufficient scope" (needs gmail.send or gmail.compose) when sending a PDF. The daily 9 AM email cannot work until the connector is re-authorised with send permission, or another sender is used (for example a Python script using Gmail API OAuth with `credentials.json`/`token.json`, as in the WAT layout, or SMTP with a Google app password stored in `.env`). Resolve this before scheduling anything.
3. **Where history is stored: sent emails DECIDED (MongoDB, see Phase 5); competitor baselines/snapshots still OPEN** (MongoDB would also work for them). The cloud sandbox is wiped each run, so baselines go either in Google Drive or committed back to the repo.
4. **Recipient address: CONFIRMED** as `aditijain1100@gmail.com` (differs from the account email `aditijain11021@gmail.com`, owner confirmed the former).

## Build order
1. Phase 1 for Tata 1mg: verify competitors, confirm the list with the owner.
2. Build `collect_news.py` and `snapshot_pages.py` first (highest signal, lowest scraping risk).
3. Add app data, sitemap diff, trends, sentiment, jobs, then the price basket last (highest risk and effort).
4. Build the email builder and send a sample for approval.
5. Schedule the daily run.

## Learnings log
(Add rate limits, quirks, broken sources and fixes here as they are found.)

- 2026-09-19: Workflow created. No tools built yet.
- 2026-09-19: Phase 1 run for Tata 1mg. Confirmed list in `profiles/tata_1mg_competitors.md`. Business Standard returns 403 to automated fetch, so use Entrackr, Inc42, Investing.com or company filings instead. Many "top e-pharmacy" listicles are unsourced promotional copy; do not cite them for numbers. Old market-share claims (2023) circulate as if current; always check the date.
- 2026-09-19: `git push` to github.com/aditijain-11/Clarix failed with "Permission denied to aditijain-1111": the Mac's stored GitHub credentials belong to a different account than the repo owner. Fix by adding that account as a collaborator or signing in as the owner. Never work around this by hunting for other credentials. RESOLVED 2026-09-20: the owner changed the git config; `origin` now uses the SSH host alias `github-aditi11` and the push succeeded.
- 2026-09-20: MongoDB Atlas connected (cluster userdb). Emails go in database `clarix`, collection `emails`; the cluster's other database `user_db` (collection `user_info`) belongs to something else and must not be touched. First record saved: the Phase 1 report email. Connection string lives only in the gitignored `.env`. It was pasted into chat with a weak password, so the owner should rotate it and use a dedicated user limited to readWrite on `clarix`.
- 2026-09-20: Cloud scheduler test PASSED (routine `trig_01XMLENg9wzrxUt3iM8tdARM`, one-time, model claude-sonnet-5, Default environment, Gmail connector attached). The agent cloned the private repo, read CLAUDE.md and the profile, ran web search, and sent one plain-text email per run (two runs: one manual at 08:39 UTC, one scheduled). Findings: (1) a scheduled run starts about 1 minute after its set time and the email lands about 2.5 minutes after it, so to arrive by 9:00 AM IST schedule around 8:55 AM IST (cron `25 3 * * *`); (2) the agent is a fresh session with no memory, so the prompt plus repo must hold everything; (3) an over-strict "last 30 days" requirement made the agent burn ~6+ searches and still find nothing, so daily prompts must cap searches and allow "nothing new"; (4) not yet tested from the cloud: PDF generation and attachment (the PDF builder is not in the repo yet), MongoDB access (no credentials in the cloud, do not put the password in a prompt), pip installs.
- 2026-09-20: Owner rule: never store generated PDFs inside the repo (not under `.tmp/` either; `*.pdf` is now gitignored). Generate them in the system temp folder, attach and send, archive the extracted text in MongoDB, then discard the file. The sent copy lives in Gmail.
- 2026-09-19: PDF reports: reportlab's built-in fonts lack the rupee sign, so write "Rs". Gmail attachments go in as base64 in the tool call (25 MB cap), so keep PDFs small.
