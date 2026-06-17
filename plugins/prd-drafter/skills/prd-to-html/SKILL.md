---
name: prd-to-html
description: Convert an existing PRD Markdown file into a standalone, browser-printable HTML document. Use when the user asks to format, export, render, print, or turn a PRD .md file into HTML or a PDF-ready browser document with dark screen styling and light print styling.
license: MIT
---

# PRD to HTML

Convert a PRD Markdown file into a polished standalone HTML document that can be opened in a browser and printed to PDF.

The generated HTML uses a dark theme on screen and switches to a light, ink-friendly theme for print via CSS `@media print`.

## Bundled Resource

Use the bundled converter script:

```bash
python skills/prd-to-html/scripts/prd_to_html.py path/to/prd.md
```

The default output path is next to the input file with the same name and an `.html` extension. To choose the destination:

```bash
python skills/prd-to-html/scripts/prd_to_html.py path/to/prd.md --output path/to/prd.html
```

If the output file already exists, ask before overwriting and then pass `--force` if overwrite is intended.

## Workflow

1. Read the source PRD enough to confirm it is the intended file.
2. Choose an output path. Prefer the same folder and filename stem unless the user requested a separate destination.
3. Run `scripts/prd_to_html.py`.
4. Open the HTML file in a browser if the user wants a preview.
5. Tell the user to use the browser print dialog to save as PDF. The print stylesheet is already embedded in the file.

## Output Expectations

The HTML should:

- Preserve Markdown structure: headings, paragraphs, blockquotes, lists, nested lists, tables, code spans, fenced code blocks, horizontal rules, links, and PRD header fields.
- Render PRD header fields such as `Status`, `Author`, `Date`, and `Version` as a compact metadata block.
- Keep `Question` and `Answer` lines visually distinct in Open Questions.
- Be self-contained: no external CSS, fonts, JavaScript, or network dependencies.
- Use dark colors only for screen display.
- Use white background, dark text, printable links, and sensible margins when printed.

## Constraints

- Do not rewrite the PRD content while exporting. This skill formats the document; it does not update requirements, answer open questions, change status, or bump version.
- Do not delete or replace the source Markdown file.
- Do not overwrite an existing HTML export without user confirmation.
- Do not rely on browser extensions or online Markdown renderers. The export must work offline from the generated HTML file.
