---
name: backlog-grooming
description: Turns raw requirements — meeting notes, transcripts, PRDs, feature requests, rough feature lists, or an existing messy backlog — into a well-structured product backlog with epics, user stories, and Gherkin-style acceptance criteria. Also re-grooms and cleans up existing backlogs (finds duplicates, missing acceptance criteria, oversized stories, stale items) and applies INVEST/MoSCoW best practices. Use this skill whenever the user asks for requirement analysis, backlog grooming or refinement, writing user stories, breaking down a feature or PRD into tickets, estimating or prioritizing backlog items, or converting notes/transcripts into actionable dev tickets — even if they don't use the words "backlog" or "agile" explicitly (e.g. "turn this PRD into tickets," "help me plan out this feature," "clean up my Jira backlog").
---

# Backlog Grooming & Requirement Analysis

Turns messy, informal, or incomplete input into a structured, ready-to-work backlog: **Epics → User Stories → Acceptance Criteria → (optional) Tasks**, following INVEST and MoSCoW best practices.

## When this skill applies

- Raw input: meeting notes, call transcripts, Slack threads, rambling feature requests, PRDs
- Structured-ish input: a rough feature list, a PRD, a spec doc
- Existing backlog: a list of tickets/stories that need re-grooming, deduping, or AC added
- Any request to "turn X into stories/tickets," "break down this feature," "groom the backlog," "write acceptance criteria," or "prioritize this backlog"

## Workflow

### Step 1 — Ingest and identify the mode

Read whatever the user gives you (paste, file, transcript). Determine which mode you're in — **this changes what you produce**:

| Mode | Signal | What to do |
|---|---|---|
| **Extraction** | Raw notes/transcript/PRD, no existing structure | Extract requirements, then build the backlog from scratch |
| **Re-grooming** | User already has stories/tickets (e.g. a CSV/Jira export, a bullet list of tickets) | Audit against the checklist in Step 5, then restructure/fix rather than starting over |
| **Hybrid** | New feature request mixed into an existing backlog | Groom new material, then check for overlap/duplication with existing items |

If the input is ambiguous or you can't tell the mode from content alone, make a reasonable assumption (usually Extraction) and say so — don't stall on a clarifying question if you can proceed.

### Step 2 — Extract requirements

Read through the source material and pull out **every distinct piece of intended functionality, constraint, or need** — even ones mentioned in passing or only implied. For transcripts/notes specifically, watch for:

- Explicit asks ("we need users to be able to...")
- Implied needs (a complaint or workaround implies an unmet requirement)
- Non-functional requirements (performance, security, compliance, accessibility) — these often get mentioned once and forgotten; don't drop them
- Out-of-scope statements ("we're NOT doing X yet") — capture these as explicit exclusions so they don't silently reappear later

Keep a running list before you start structuring. It's fine — encouraged — to over-extract at this stage and consolidate later, rather than under-extract and lose something.

### Step 3 — Structure into Epics → Stories

**Epics** are the large capability groupings ("User Authentication", "Checkout Flow"). Group related requirements under an epic rather than leaving a flat story list — flat lists don't scale past ~10 items and lose the map of how things relate.

**User Stories** follow the standard form and must each pass the **INVEST test**:

```
As a [role], I want [capability], so that [benefit].
```

- **I**ndependent — doesn't hard-depend on another unshipped story (flag it if it must)
- **N**egotiable — describes outcome, not implementation
- **V**aluable — delivers value to a user or the business on its own, not a technical sub-task disguised as a story
- **E**stimable — the team could size it without needing to first do a spike
- **S**mall — completable within roughly one sprint; if it feels bigger, split it (see Step 4)
- **T**estable — has or can have clear acceptance criteria

If a requirement doesn't survive as a standalone story (too small, purely technical, or a dependency of another story), it becomes a **Task** under the relevant story instead of its own story.

### Step 4 — Split oversized stories

If a story can't reasonably be called "Small," split it. Use whichever axis fits, and say which one you used:

- **Workflow steps** — split a multi-step process into one story per step
- **Business rule variations** — split "handle payment" into "handle credit card payment," "handle PayPal payment," etc.
- **CRUD operations** — split "manage X" into Create/Read/Update/Delete stories
- **Happy path vs. edge cases** — ship the core path as one story, edge cases as follow-on stories
- **Data variations** — e.g. "import CSV" vs. "import Excel" if the parsing logic meaningfully differs

Don't split by technical layer (e.g. "frontend story" + "backend story" for the same feature) — that breaks the Valuable and Independent INVEST criteria, since neither half is shippable or demoable alone.

### Step 5 — Write acceptance criteria

Default to **Gherkin-style** (Given/When/Then) — it's the most common format and translates directly into test cases:

```
Given [context/precondition]
When [action]
Then [expected outcome]
```

Write enough scenarios to cover:
1. The happy path
2. The most likely edge case(s) or failure mode(s) mentioned or implied by the source material
3. Any non-functional requirement that applies (e.g. "Then the page loads in under 2 seconds")

Don't invent edge cases the source material gives no basis for — flag them as open questions instead (Step 6) rather than guessing at business rules.

If the user's team uses a plain checklist style instead of Gherkin, match that instead — ask if unclear, or default to Gherkin since it's the safer default.

### Step 6 — Flag gaps and ambiguities

Requirement extraction from informal sources is almost always incomplete. Rather than silently filling gaps with assumptions, surface them as an **"Open Questions / Assumptions"** list at the end of the backlog output — e.g.:

- "Notes mention 'admins can override this' but don't specify who counts as an admin — assumed existing admin role."
- "No mention of what happens if the payment fails mid-flow — flagged as a gap, not covered by any story below."

This is one of the most valuable things this skill produces — it's the difference between a backlog that looks complete and one that actually is.

### Step 7 — Prioritize (if requested or if input implies urgency signals)

Default to **MoSCoW** (Must have / Should have / Could have / Won't have this time) unless the user specifies something else (e.g. RICE, value-vs-effort). Base priority on signals in the source material (explicit statements of urgency, dependencies, stated business goals) — don't invent priority out of nothing. If there's no signal at all, leave priority unset rather than guessing, and say so.

### Step 8 — Re-grooming mode specifics

When the input is an existing backlog rather than raw material, run this checklist against each item instead of Steps 2–4:

- [ ] Does it pass INVEST? Note which criterion fails if any.
- [ ] Does it have acceptance criteria at all? If missing, draft them (flag as drafted-not-confirmed).
- [ ] Is it a likely duplicate or near-duplicate of another item? Flag both, don't silently merge.
- [ ] Is it stale (references old/removed functionality, blocked indefinitely, no longer relevant)? Flag for the user to confirm before removal — never delete outright.
- [ ] Is it actually a story, or is it a task/bug/technical-debt item mislabeled as a story?
- [ ] Is it oversized? Apply Step 4 splitting if so.

Output the audit findings alongside the cleaned-up items so the user can see what changed and why.

## Output format

Default to this structure (Markdown). Use a **table** for the epic/story overview and **expandable detail blocks** for full story content, unless the user's backlog is small enough that a flat list reads fine.

```markdown
## Epic: [Epic Name]
[One-line description of the capability this epic covers]

### Story: [Story Title]                              Priority: [Must/Should/Could/Won't]
**As a** [role], **I want** [capability], **so that** [benefit].

**Acceptance Criteria:**
- Given [...], When [...], Then [...]
- Given [...], When [...], Then [...]

**Tasks:** (if applicable)
- [ ] Technical sub-task
- [ ] Technical sub-task

---
```

End every backlog output with:

```markdown
## Open Questions / Assumptions
- ...
```

**File output**: If the user wants this saved as a file rather than shown inline (e.g. "give me a Word doc," "export as CSV for Jira import," "put this in a spreadsheet"), use the appropriate skill (`docx` for a document, `xlsx` for a spreadsheet/CSV import format) rather than hand-rolling the file. A CSV/xlsx export should flatten to one row per story with columns: Epic, Story Title, Description, Acceptance Criteria (newline-separated within the cell), Priority, Notes.

## Things to avoid

- Don't pad the backlog with filler stories to look thorough — every story should trace back to something in the source material.
- Don't silently resolve ambiguity by picking the most likely interpretation and moving on without flagging it — that's exactly the kind of gap that causes rework later. Flag it, then proceed with your best assumption.
- Don't merge or delete existing backlog items without flagging the change for user confirmation.
- Don't split stories along technical-layer lines (frontend/backend) — see Step 4.
- Don't over-specify acceptance criteria with implementation detail (e.g. specific button colors, exact API payloads) unless the source material specifies it — that's a Negotiable-criterion violation.
