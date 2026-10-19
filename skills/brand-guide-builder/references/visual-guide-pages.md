# Paginated visual guide — page template

A concrete, reusable template for the "visualize as an artifact, page by
page" export option, based on a layout pattern common to generated
brand-guide exports. Use this when the user
wants to *see* their guide rendered the way a dedicated generator tool
would show it, not just read a single long scrolling page.

## Structural pattern (per page)

Every page shares one consistent chrome, and only the content area and
sidebar color change:

- **Sidebar** (narrow, ~15-18% of width, full height): solid color block,
  with the page's section label running vertically (rotated -90deg),
  large, bold, in a color that contrasts with the sidebar fill (usually
  white). The sidebar's color is the "payload" — it's what signals which
  section you're in at a glance, so vary it meaningfully by section
  rather than using one color for every page (one hero color on every
  sidebar is a valid, calmer choice; varying by section mirrors the
  per-step color-coding of the wizard itself).
- **Content area** (remaining width): white/light background, generous
  padding, the actual page content — see "Content templates" below for
  the different layouts this area takes depending on what it's showing.
- **Footer bar** (full width, bottom): a thin top border, a light
  neutral-tint background, split into two columns — **ABOUT** (what this
  page/concept is) and **USAGE** (how/when to apply it). Keep each to
  1-2 short sentences. This footer is what makes every page
  self-explanatory on its own, without needing the rest of the guide for
  context — worth keeping even if nothing else from this pattern is kept.
- **Page navigation**: page number indicator + prev/next controls,
  consistent placement across pages (e.g. fixed prev/next buttons plus
  "Page X of Y").

## Content templates (what goes in the content area)

Different page types call for different content-area layouts. Match the
template to what the page is actually showing — don't force everything
into the same layout:

- **Headline list** — a short intro sentence, then a short list of big,
  bold words/phrases (one per line). Used for brand voice words and
  brand personality traits.
- **Big-statement page** — a short label line ("Our audience is:") then
  one large headline statement. Used for audience.
- **Swatch grid** — rounded-rect cards in a grid, each showing a color
  fill, name, and hex code. Used for the color palette.
- **Role pyramid** — colors shown as circles arranged by role weight
  (one large Hero circle at top, a row of medium Accent circles below,
  a row of smaller Neutral circles at the bottom), each labeled with its
  role and hex. This is a direct visualization of the Colors step's role
  assignment from the main wizard flow — build it from the same role
  data, don't re-derive it.
- **Data table** — rows of structured data (e.g. swatch / name / hex /
  RGB / CMYK, or a contrast-ratio table of approved text/background
  pairs with their scores). Used for color codes and accessibility
  testing.
- **Type specimen cards** — one card per font role (heading/subheading/
  body), each showing the font name + weight, a full alphabet + numeral
  string, and its tracking/line-height settings.
- **In-context type preview** — a colored card rendering real sample
  headline + body copy in the actual chosen fonts, so type choices are
  seen in a realistic context rather than as an isolated specimen.
- **Hierarchy list** — the full H1-H6 + Body L/M/S scale, each row set
  in its own actual size, with a divider between rows.
- **Logo display** — the logo itself, large, centered, with a minimum-
  size or clear-space note beneath it.
- **Button/link demo** — rendered example buttons/links in their default
  state, an arrow, then the same element in its hover state. Show each
  defined button variant (primary filled, secondary filled, text-link)
  as its own row.
- **Color range scale** — for each base color, a vertical column of
  tints above and shades below the base (e.g. 25/50/75% steps each way),
  each step labeled with its hex. Useful as a secondary/extended palette
  reference but not required for a minimal guide.
- **At-a-glance summary** — a single condensed page combining: name +
  tagline, logo, the color palette as a single swatch strip, and the
  three font names with "Aa" specimens. This is the "if someone only
  reads one page" page — put it early (right after the cover) or make it
  easy to jump to.

## Building this as an artifact

Build as one self-contained HTML file (see the main SKILL.md Export
step for the publish mechanics). Practical notes specific to this
paginated format:

- Drive it from a simple JS array of page objects
  (`{sidebarColor, label, contentType, data}`) and one render function
  per content template — don't hand-write 15 near-duplicate page blocks.
- Keep navigation simple and obvious: prev/next buttons plus a page
  counter is enough; a full page-number strip is a nice-to-have for longer guides, not a requirement.
- Pull every color, font, and piece of copy from the user's own Steps
  1-5 answers — this template is a layout to pour their brand into, not
  a themed product with its own fixed colors. Never reuse another brand's
  palette or copy as filler.
- Only include the page types the user actually has data for (skip the
  logo page entirely rather than showing an empty one if they have no
  logo yet, etc.) — same principle as the main guide template in
  `brand-guide-template.md`.
