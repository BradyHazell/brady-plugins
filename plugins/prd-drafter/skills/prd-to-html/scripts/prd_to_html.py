#!/usr/bin/env python3
"""Convert a PRD Markdown file to standalone print-ready HTML."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)\s*([\w.+-]*)\s*$")
LIST_RE = re.compile(r"^(\s*)((?:[-+*])|(?:\d+[.)]))\s+(.*)$")
META_RE = re.compile(r"^\*\*([^*:\n][^*:]*):\*\*\s*(.*)$")
QA_RE = re.compile(r"^\*\*(Question|Answer):\*\*\s*(.*)$", re.IGNORECASE)
HR_RE = re.compile(r"^\s{0,3}(?:-{3,}|\*{3,}|_{3,})\s*$")
TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$"
)


def indent_width(value: str) -> int:
    return len(value.replace("\t", "    "))


def slugify(value: str, seen: dict[str, int]) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = slug or "section"
    count = seen.get(slug, 0)
    seen[slug] = count + 1
    return slug if count == 0 else f"{slug}-{count + 1}"


def escape_attr(value: str) -> str:
    return html.escape(value, quote=True)


def render_inline_text(value: str) -> str:
    protected: dict[str, str] = {}

    def protect(markup: str) -> str:
        token = f"@@PRDHTML{len(protected)}@@"
        protected[token] = markup
        return token

    def render_text_segment(segment: str) -> str:
        rendered = html.escape(segment)

        def link_repl(match: re.Match[str]) -> str:
            label = match.group(1)
            href = html.unescape(match.group(2).strip())
            return protect(
                f'<a href="{escape_attr(href)}">{label}</a>'
            )

        rendered = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link_repl, rendered)

        def autolink_repl(match: re.Match[str]) -> str:
            url = html.unescape(match.group(0))
            trailing = ""
            while url and url[-1] in ".,;:":
                trailing = url[-1] + trailing
                url = url[:-1]
            link = f'<a href="{escape_attr(url)}">{html.escape(url)}</a>'
            return protect(link) + html.escape(trailing)

        rendered = re.sub(r"(?<![\"'=])\bhttps?://[^\s<)]+", autolink_repl, rendered)
        rendered = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", rendered)
        rendered = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", rendered)

        for token, markup in protected.items():
            rendered = rendered.replace(token, markup)
        return rendered

    output: list[str] = []
    last = 0
    for match in re.finditer(r"`([^`\n]+)`", value):
        output.append(render_text_segment(value[last : match.start()]))
        output.append(f"<code>{html.escape(match.group(1))}</code>")
        last = match.end()
    output.append(render_text_segment(value[last:]))
    return "".join(output)


def split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def table_alignments(separator: str, count: int) -> list[str]:
    aligns: list[str] = []
    for cell in split_table_row(separator):
        left = cell.startswith(":")
        right = cell.endswith(":")
        if left and right:
            aligns.append("center")
        elif right:
            aligns.append("right")
        elif left:
            aligns.append("left")
        else:
            aligns.append("")
    while len(aligns) < count:
        aligns.append("")
    return aligns[:count]


def is_table_start(lines: list[str], index: int) -> bool:
    return (
        index + 1 < len(lines)
        and "|" in lines[index]
        and bool(TABLE_SEPARATOR_RE.match(lines[index + 1]))
    )


def is_block_start(lines: list[str], index: int) -> bool:
    line = lines[index]
    return (
        not line.strip()
        or bool(FENCE_RE.match(line))
        or bool(HEADING_RE.match(line))
        or bool(HR_RE.match(line))
        or bool(LIST_RE.match(line))
        or line.lstrip().startswith(">")
        or is_table_start(lines, index)
        or bool(META_RE.match(line))
    )


def render_table(lines: list[str], index: int) -> tuple[str, int]:
    headers = split_table_row(lines[index])
    aligns = table_alignments(lines[index + 1], len(headers))
    rows: list[list[str]] = []
    index += 2
    while index < len(lines) and "|" in lines[index] and lines[index].strip():
        rows.append(split_table_row(lines[index]))
        index += 1

    def cell_attrs(position: int) -> str:
        align = aligns[position] if position < len(aligns) else ""
        return f' style="text-align: {align};"' if align else ""

    header_html = "".join(
        f"<th{cell_attrs(i)}>{render_inline_text(cell)}</th>"
        for i, cell in enumerate(headers)
    )
    body_rows: list[str] = []
    for row in rows:
        padded = row + [""] * max(0, len(headers) - len(row))
        body_rows.append(
            "<tr>"
            + "".join(
                f"<td{cell_attrs(i)}>{render_inline_text(cell)}</td>"
                for i, cell in enumerate(padded[: len(headers)])
            )
            + "</tr>"
        )
    return (
        "<table>\n<thead><tr>"
        + header_html
        + "</tr></thead>\n<tbody>\n"
        + "\n".join(body_rows)
        + "\n</tbody>\n</table>",
        index,
    )


def render_blockquote(lines: list[str], index: int) -> tuple[str, int]:
    quote_lines: list[str] = []
    while index < len(lines) and lines[index].lstrip().startswith(">"):
        quote_lines.append(re.sub(r"^\s*>\s?", "", lines[index]))
        index += 1

    paragraphs: list[str] = []
    current: list[str] = []
    for line in quote_lines:
        if line.strip():
            current.append(line.strip())
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))

    body = "\n".join(f"<p>{render_inline_text(p)}</p>" for p in paragraphs)
    return f"<blockquote>\n{body}\n</blockquote>", index


def render_list(lines: list[str], index: int, indent: int, ordered: bool) -> tuple[str, int]:
    tag = "ol" if ordered else "ul"
    items: list[str] = []

    while index < len(lines):
        match = LIST_RE.match(lines[index])
        if not match:
            break

        current_indent = indent_width(match.group(1))
        current_ordered = match.group(2)[0].isdigit()
        if current_indent != indent or current_ordered != ordered:
            break

        item_parts = [render_inline_text(match.group(3).strip())]
        index += 1

        while index < len(lines):
            if not lines[index].strip():
                index += 1
                continue

            next_match = LIST_RE.match(lines[index])
            if next_match:
                next_indent = indent_width(next_match.group(1))
                next_ordered = next_match.group(2)[0].isdigit()
                if next_indent > indent:
                    nested_html, index = render_list(
                        lines, index, next_indent, next_ordered
                    )
                    item_parts.append(nested_html)
                    continue
                break

            continuation_indent = indent_width(re.match(r"^\s*", lines[index]).group(0))
            if continuation_indent > indent:
                continuation: list[str] = []
                while index < len(lines) and lines[index].strip():
                    nested_match = LIST_RE.match(lines[index])
                    if nested_match:
                        nested_indent = indent_width(nested_match.group(1))
                        if nested_indent >= continuation_indent:
                            break
                    if indent_width(re.match(r"^\s*", lines[index]).group(0)) <= indent:
                        break
                    continuation.append(lines[index].strip())
                    index += 1
                if continuation:
                    item_parts.append(
                        f"<p>{render_inline_text(' '.join(continuation))}</p>"
                    )
                    continue
            break

        items.append("<li>" + "\n".join(item_parts) + "</li>")

    return f"<{tag}>\n" + "\n".join(items) + f"\n</{tag}>", index


def render_metadata(lines: list[str], index: int) -> tuple[str, int]:
    rows: list[str] = []
    while index < len(lines):
        match = META_RE.match(lines[index].strip())
        if not match:
            break
        key = match.group(1).strip()
        if key.lower() in {"question", "answer"}:
            break
        value = match.group(2).strip()
        rows.append(
            "<div>"
            f"<dt>{html.escape(key)}</dt>"
            f"<dd>{render_inline_text(value)}</dd>"
            "</div>"
        )
        index += 1
    return '<dl class="metadata">\n' + "\n".join(rows) + "\n</dl>", index


def render_blocks(lines: list[str]) -> str:
    output: list[str] = []
    index = 0
    seen_heading_ids: dict[str, int] = {}
    seen_h2 = False

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        fence = FENCE_RE.match(line)
        if fence:
            fence_token = fence.group(1)
            language = fence.group(2)
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith(fence_token):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            class_attr = (
                f' class="language-{escape_attr(language)}"' if language else ""
            )
            output.append(
                f"<pre><code{class_attr}>{html.escape(chr(10).join(code_lines))}</code></pre>"
            )
            continue

        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if level >= 2:
                seen_h2 = True
            heading_id = slugify(re.sub(r"`([^`]+)`", r"\1", text), seen_heading_ids)
            output.append(
                f'<h{level} id="{escape_attr(heading_id)}">{render_inline_text(text)}</h{level}>'
            )
            index += 1
            continue

        if HR_RE.match(line):
            output.append("<hr>")
            index += 1
            continue

        qa = QA_RE.match(stripped)
        if qa:
            label = qa.group(1).capitalize()
            css_class = "question" if label == "Question" else "answer"
            value = qa.group(2).strip()
            output.append(
                f'<p class="qa qa-{css_class}"><strong>{label}:</strong> {render_inline_text(value)}</p>'
            )
            index += 1
            continue

        meta = META_RE.match(stripped)
        if meta and not seen_h2:
            metadata_html, index = render_metadata(lines, index)
            output.append(metadata_html)
            continue

        if is_table_start(lines, index):
            table_html, index = render_table(lines, index)
            output.append(table_html)
            continue

        if line.lstrip().startswith(">"):
            quote_html, index = render_blockquote(lines, index)
            output.append(quote_html)
            continue

        list_match = LIST_RE.match(line)
        if list_match:
            list_html, index = render_list(
                lines,
                index,
                indent_width(list_match.group(1)),
                list_match.group(2)[0].isdigit(),
            )
            output.append(list_html)
            continue

        paragraph_lines: list[str] = []
        while index < len(lines) and not is_block_start(lines, index):
            paragraph_lines.append(lines[index].strip())
            index += 1
        if paragraph_lines:
            output.append(f"<p>{render_inline_text(' '.join(paragraph_lines))}</p>")
            continue

        output.append(f"<p>{render_inline_text(stripped)}</p>")
        index += 1

    return "\n\n".join(output)


def extract_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 1:
            return re.sub(r"`([^`]+)`", r"\1", match.group(2).strip())
    return fallback


def build_html(markdown: str, source_path: Path, title_override: str | None = None) -> str:
    title = title_override or extract_title(markdown, source_path.stem)
    body = render_blocks(markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n"))
    generated_date = dt.date.today().isoformat()
    source_name = source_path.name

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0b0f14;
      --panel: #111821;
      --panel-border: #253241;
      --text: #e8edf2;
      --muted: #a8b3bf;
      --strong: #f8fafc;
      --accent: #7cc7ff;
      --accent-soft: rgba(124, 199, 255, 0.14);
      --code-bg: #0a111a;
      --table-stripe: rgba(255, 255, 255, 0.035);
    }}

    * {{
      box-sizing: border-box;
    }}

    html {{
      background: var(--bg);
      color: var(--text);
      font-family: "Segoe UI", Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Arial, sans-serif;
      line-height: 1.58;
      text-rendering: optimizeLegibility;
    }}

    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(124, 199, 255, 0.08), transparent 34rem),
        linear-gradient(180deg, #0b0f14 0%, #0d131a 100%);
    }}

    .page {{
      width: min(100%, 980px);
      margin: 0 auto;
      padding: 48px 24px 72px;
    }}

    .prd {{
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: 8px;
      padding: clamp(24px, 5vw, 52px);
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
    }}

    h1, h2, h3, h4, h5, h6 {{
      color: var(--strong);
      line-height: 1.2;
      margin: 1.7em 0 0.55em;
      letter-spacing: 0;
    }}

    h1 {{
      margin-top: 0;
      padding-bottom: 0.35em;
      border-bottom: 1px solid var(--panel-border);
      font-size: clamp(2rem, 4vw, 3rem);
    }}

    h2 {{
      margin-top: 2.2em;
      font-size: 1.55rem;
    }}

    h3 {{
      font-size: 1.2rem;
    }}

    p, ul, ol, blockquote, table, pre, .metadata {{
      margin-top: 0;
      margin-bottom: 1rem;
    }}

    ul, ol {{
      padding-left: 1.45rem;
    }}

    li {{
      margin: 0.28rem 0;
    }}

    li > ul,
    li > ol {{
      margin-top: 0.35rem;
      margin-bottom: 0.35rem;
    }}

    a {{
      color: var(--accent);
      text-decoration-thickness: 0.08em;
      text-underline-offset: 0.18em;
      overflow-wrap: anywhere;
    }}

    strong {{
      color: var(--strong);
    }}

    code {{
      background: var(--code-bg);
      border: 1px solid var(--panel-border);
      border-radius: 4px;
      color: #d8e6ff;
      font-family: "Cascadia Code", "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      font-size: 0.92em;
      padding: 0.1em 0.32em;
    }}

    pre {{
      overflow-x: auto;
      padding: 1rem;
      background: var(--code-bg);
      border: 1px solid var(--panel-border);
      border-radius: 8px;
    }}

    pre code {{
      display: block;
      padding: 0;
      border: 0;
      background: transparent;
    }}

    blockquote {{
      margin-left: 0;
      padding: 0.85rem 1rem;
      border-left: 4px solid var(--accent);
      background: var(--accent-soft);
      color: var(--text);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      display: block;
      overflow-x: auto;
      border: 1px solid var(--panel-border);
      border-radius: 8px;
    }}

    th, td {{
      padding: 0.68rem 0.78rem;
      border-bottom: 1px solid var(--panel-border);
      vertical-align: top;
      text-align: left;
    }}

    th {{
      color: var(--strong);
      background: rgba(255, 255, 255, 0.055);
    }}

    tbody tr:nth-child(even) {{
      background: var(--table-stripe);
    }}

    tbody tr:last-child td {{
      border-bottom: 0;
    }}

    hr {{
      border: 0;
      border-top: 1px solid var(--panel-border);
      margin: 2rem 0;
    }}

    .metadata {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 0.65rem;
      padding: 1rem;
      border: 1px solid var(--panel-border);
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.03);
    }}

    .metadata div {{
      min-width: 0;
    }}

    .metadata dt {{
      color: var(--muted);
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}

    .metadata dd {{
      margin: 0.15rem 0 0;
      color: var(--strong);
      overflow-wrap: anywhere;
    }}

    .qa {{
      padding: 0.8rem 0.95rem;
      border: 1px solid var(--panel-border);
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.025);
    }}

    .qa-question {{
      margin-bottom: 0.35rem;
    }}

    .qa-answer {{
      margin-top: 0;
      border-color: rgba(124, 199, 255, 0.32);
      background: var(--accent-soft);
    }}

    .doc-footer {{
      margin-top: 1rem;
      color: var(--muted);
      font-size: 0.85rem;
      text-align: center;
    }}

    @media (max-width: 640px) {{
      .page {{
        padding: 20px 12px 40px;
      }}

      .prd {{
        padding: 20px;
      }}
    }}

    @media print {{
      @page {{
        size: A4;
        margin: 16mm 15mm 18mm;
      }}

      :root {{
        color-scheme: light;
      }}

      html, body {{
        background: #ffffff !important;
        color: #111111 !important;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 10.5pt;
        line-height: 1.45;
      }}

      body {{
        margin: 0;
      }}

      .page {{
        width: auto;
        margin: 0;
        padding: 0;
      }}

      .prd {{
        padding: 0;
        border: 0;
        border-radius: 0;
        background: #ffffff !important;
        box-shadow: none;
      }}

      h1, h2, h3, h4, h5, h6, strong {{
        color: #111111 !important;
      }}

      h1 {{
        font-size: 23pt;
        border-bottom: 1px solid #bbbbbb;
      }}

      h2 {{
        font-size: 15pt;
        margin-top: 1.45em;
        break-after: avoid;
      }}

      h3 {{
        font-size: 12.5pt;
        break-after: avoid;
      }}

      a {{
        color: #0645ad !important;
        text-decoration: underline;
      }}

      a[href^="http"]::after {{
        content: " (" attr(href) ")";
        color: #555555;
        font-size: 0.85em;
        overflow-wrap: anywhere;
      }}

      code, pre {{
        color: #111111 !important;
        background: #f4f4f4 !important;
        border-color: #d0d0d0 !important;
      }}

      blockquote, .metadata, .qa {{
        background: #f7f7f7 !important;
        border-color: #cccccc !important;
      }}

      .metadata dt, .doc-footer {{
        color: #555555 !important;
      }}

      .metadata dd {{
        color: #111111 !important;
      }}

      table {{
        display: table;
        overflow: visible;
        border-color: #cccccc;
      }}

      th, td {{
        border-color: #cccccc;
      }}

      th {{
        background: #eeeeee !important;
        color: #111111 !important;
      }}

      tr, li, blockquote, pre, table, .metadata, .qa {{
        break-inside: avoid;
      }}

      .doc-footer {{
        margin-top: 12mm;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <article class="prd">
{body}
    </article>
  </main>
</body>
</html>
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a PRD Markdown file to standalone print-ready HTML."
    )
    parser.add_argument("input", type=Path, help="Path to the source PRD Markdown file.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path for the generated HTML file. Defaults to input path with .html extension.",
    )
    parser.add_argument(
        "--title",
        help="Override the HTML document title. Defaults to the first H1 or input filename.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing output file.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    input_path = args.input.expanduser().resolve()
    output_path = (
        args.output.expanduser().resolve()
        if args.output
        else input_path.with_suffix(".html")
    )

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    if input_path.suffix.lower() not in {".md", ".markdown"}:
        raise SystemExit("Input file must be a Markdown file with .md or .markdown extension.")
    if output_path.exists() and not args.force:
        raise SystemExit(f"Output file already exists: {output_path} (pass --force to overwrite)")

    markdown = input_path.read_text(encoding="utf-8-sig")
    html_document = build_html(markdown, input_path, args.title)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_document, encoding="utf-8", newline="\n")
    print(output_path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        raise SystemExit(130)
