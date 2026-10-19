---
name: brand-guide-builder
description: >-
  Runs the actual guided, six-step flow that dedicated brand-guideline
  generator tools use to produce a complete brand
  guide: foundations (name, tagline, personality, voice, audience), a
  color palette with role assignment and WCAG accessibility checks, a
  typography system, button and link styling, logo usage rules, and a
  final export as a published shareable page, a downloadable document,
  and a condensed AI-ready brand prompt. Use this whenever the user wants
  to create, define, or document their brand's visual identity, wants
  help building a brand guide / brand book / style guide from scratch,
  wants a cohesive and accessible color palette, wants to define their
  brand voice and visual rules systematically, or asks to build their own
  brand guidelines the way a dedicated generator tool would. This is for
  actually producing a brand guide, not for writing code — if the user
  wants to build the generator tool itself as software, that's a
  different request.
---

# Brand Guide Builder

Runs the six-step guided flow conversationally. Keep the source product's
core discipline: **every step ends in an explicit confirmation before
moving on — nothing advances silently**, and later steps only use
decisions already locked in earlier ones (button colors only come from
the approved palette, never a new color introduced on the fly).

Track progress visibly in chat (e.g. a short "Step 2 of 6 — Colors" line)
so the user always knows where they are. Ask each step's questions
together in one message rather than one field per message — that matches
chat's natural rhythm better than a literal one-field-per-screen wizard
would.

## Step 1 — Foundations
Ask for: brand name (required), tagline (optional — say it can be
skipped), 2-4 personality traits, 1-3 voice words, target audience (a
sentence or two). If the user is unsure on any of these, offer to
brainstorm 3-4 options for them to react to rather than leaving it blank.

## Step 2 — Colors
1. Starting palette: use what the user already has (hex codes, a logo, a
   reference image or site) if they have one. Otherwise propose a palette
   grounded in the Step 1 personality/voice — explain the reasoning, don't
   just output hex codes with no rationale.
2. Assign roles together with the user: **Hero** (primary, most
   prominent), **Accent** (1-3 colors for highlights/CTAs), **Light
   Neutral**, **Dark Neutral** (for backgrounds/text).
3. Run `scripts/contrast_check.py` with the full palette (pass it as a
   JSON array of `{"name": ..., "hex": ...}`) to get every ordered
   text-on-background pair's WCAG ratio and AA/AAA pass status. It
   exits with status 2 when fewer than 2 pairs pass AA, which is the
   signal that the forcing function below isn't satisfied yet.
4. **Forcing function — do not skip this**: before moving to Step 3, get
   the user's explicit confirmation of at least 2 AA-passing (4.5:1+)
   combinations they'll actually use. If fewer than 2 pass, propose a
   tint/shade adjustment to one color, re-run the script, and check again.
   Don't let the flow proceed with zero confirmed accessible pairs.

## Step 3 — Typography
Ask for heading font, body font, and an optional accent font (used only
for emphasis inside headlines/pull-quotes). If the user has no fonts in
mind, suggest 2-3 real, freely-available pairings (Google Fonts is a safe
default) that fit the Step 1 personality — name actual fonts, don't
invent placeholder names. Mention the accent-font convention if relevant:
wrapping a word in `*asterisks*` in generated copy marks it for
accent-font treatment.

## Step 4 — Buttons & Links
Ask for: fill style (filled / outline / filled+outline), corner shape
(sharp / slightly rounded / pill), and which Step 2 colors map to button
background, button text, hover background, and hover text. Every color
here must come from the already-approved palette — if the user suggests
a new color, point that out and ask them to either add it to the Step 2
palette first or pick from what's already approved.

## Step 5 — Logo Rules
Ask if they have a logo to upload (an attached image file). If yes: note
which variant it is (primary / horizontal / stacked / favicon / wordmark
/ other — ask if unclear) and capture any usage rules (clear space,
minimum size). If no logo yet, offer either: (a) a ready-to-use AI
image-generation prompt built from the brand name/personality/colors, for
them to run in an external image tool, or (b) a simple wordmark set in
the chosen typography and hero color, built directly in the output guide.

## Step 6 — Export
Generate from everything collected. Offer the user a choice of format
(or build more than one if they want several) rather than assuming:

1. **Published, shareable brand guide** — build a single self-contained
   HTML page (structure from `references/brand-guide-template.md`) and
   publish it as an Artifact. This is a genuine advantage over a static
   file: it gives a live link that stays current if you edit it later,
   matching the "sharable link, no attachments" promise of the source
   product's export, using a capability already built into this
   environment rather than something to build from scratch.
2. **Paginated visual guide (artifact)** — when the user wants to *see*
   the guide rendered the way a dedicated generator tool would show it
   (page by page, with a distinct sidebar/content/footer treatment per
   page) rather than one long scroll, build this using
   `references/visual-guide-pages.md`. Still a single self-contained
   HTML file, published as an Artifact, just with the paginated
   sidebar-page template instead of (or alongside) the scrolling layout
   from option 1 — ask which the user prefers if it's not obvious, since
   they're genuinely different reading experiences, not just a style
   difference.
3. **Downloadable document** — also offer a PDF or Word version of the
   same content for the user to keep/send as a file (check available
   skills for document/PDF generation and follow that skill's guidance;
   don't hand-roll PDF generation).
4. **AI-ready prompt** — build this using `references/ai-prompt-format.md`.
   Give it to the user as a copyable block in chat AND include it as a
   labeled section in the published guide. This is the single most
   distinctive deliverable here — put real effort into the voice-guidance
   line specifically, since it's the one part that requires actual
   translation rather than restating inputs.

### Visual design of the guide itself — leave this open
Don't default to any fixed house style for the guide's own page design.
The whole point is that the user's own brand (their palette, their fonts,
their logo) drives what the page looks like — use the frontend-design
skill for layout and typographic craft, but let the content be the
aesthetic. If the user has opinions about the guide's own layout, ask;
otherwise make a tasteful, content-driven default and offer to adjust
once they've seen it.
