# Example: Fernhill Bakery

A fictional brand, run through the six steps, to show what the skill's
deliverables look like.

- `palette.json`: the Step 2 palette, ready to feed to `contrast_check.py`
- `contrast-output.txt`: the real output of the script on that palette
- `ai-prompt.md`: the Step 6 AI-ready prompt, built from the approved pairs

Regenerate the contrast output:

```bash
python3 ../../skills/brand-guide-builder/scripts/contrast_check.py --file palette.json
```
