# AI-ready brand prompt — format

This is the product's standout feature: a condensed, structured text block
the user can paste directly into any AI chat tool (Claude, ChatGPT, etc.)
so that future AI-generated copy, code, or design stays on-brand without
re-explaining the brand every time. Make this genuinely useful, not a
token gesture — it should be something that actually changes what a
downstream AI produces if pasted in as context.

## Structure

Use clean markdown headers, short declarative lines (not prose paragraphs
— this is meant to be skimmed by a model, not read by a human for
pleasure), and keep the whole thing under roughly 300 words so it's cheap
to paste repeatedly.

```markdown
## Brand
Name: [name]
Tagline: [tagline, if set]
Personality: [trait, trait, trait]
Voice: [voice word, voice word]
Audience: [one sentence]

## Voice guidance
Write in a [voice words] tone. [1 sentence translating the voice words
into an actual instruction — e.g. "Direct / Witty" becomes "Keep
sentences short, avoid corporate hedging, allow a dry joke when it fits
naturally — never force one."]

## Colors
Hero: [name] [hex]
Accent: [name] [hex], [name] [hex]
Light neutral: [name] [hex]
Dark neutral: [name] [hex]
Approved text/background pairs: [X] on [Y], [X] on [Y]

## Typography
Headings: [font name]
Body: [font name]
Accent (optional emphasis only): [font name]

## Buttons
[Fill style], [shape] corners. Default: [button color] bg / [text color]
text. Hover: [hover color] bg / [hover text color] text.

## Logo
[One line: what the logo is, where primary vs. alternate variants apply,
minimum size / clear space if defined.]
```

## Notes
- Omit any section whose inputs weren't provided rather than leaving
  placeholder brackets in the actual output — an empty/fake-looking field
  undermines trust in the whole block.
- The "Voice guidance" line is the one piece that isn't a direct restatement
  of earlier inputs — it's a genuine translation of voice adjectives into
  something an LLM can act on, so spend real effort on it rather than
  template-filling.
- Offer this as both a copyable code block in chat and as plain text
  inside the generated HTML guide (a labeled section with a visible "copy"
  affordance if the guide is interactive) so it's usable from either
  export path.
