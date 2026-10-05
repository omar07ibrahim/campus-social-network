#!/usr/bin/env python3
"""Assemble Report.pdf from the section files tracked under docs/.

Each section already lives in its own reviewed Markdown file (single source
of truth per the repo's doc map in README.md). This script only concatenates
them in assignment order, renders Mermaid diagrams live via headless
Chromium, and prints the result to PDF. Re-run after editing any section:

    cd docs && ../backend/.venv/bin/python build_report.py
"""
import re
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUTPUT = ROOT / "Report.pdf"

# (Section title, file relative to docs/) in assignment order.
SECTIONS = [
    ("1.1 Stakeholder Analysis", "requirements/stakeholders.md"),
    ("1.1-1.3 Product Scope", "requirements/scope.md"),
    ("1.2 Functional Requirements", "requirements/functional-requirements.md"),
    ("1.3 Non-Functional Requirements & Architectural Drivers (2.1)", "requirements/non-functional-requirements.md"),
    ("1.4-1.5 User Stories, Traceability & Review", "requirements/user-stories.md"),
    ("1.5 Requirements Review", "requirements/requirements-review.md"),
    ("2.2 C4 — System Context", "architecture/diagrams/c4-context.md"),
    ("2.2 C4 — Containers", "architecture/diagrams/c4-container.md"),
    ("2.3 Collaboration Sequence Diagram", "architecture/diagrams/sequence-create-post.md"),
    ("2.4 API Contract", "architecture/api-contract.md"),
    ("2.5 Repository Structure", "architecture/repository-structure.md"),
    ("2.6 ER Diagram", "architecture/diagrams/er-diagram.md"),
    ("2.7 ADR-01: Visibility & Access Control", "architecture/adr/adr-01-visibility-access-control.md"),
    ("2.7 ADR-02: AI Feature", "architecture/adr/adr-02-ai-feature.md"),
    ("2.7 ADR-03: Data Storage", "architecture/adr/adr-03-data-storage.md"),
    ("2.7 ADR-04: Collaboration & Concurrent Editing", "architecture/adr/adr-04-collaboration-concurrent-editing.md"),
    ("Section 3: Project Management", "project-management/README.md"),
    ("Proof-of-Concept Demo Script", "demo-script.md"),
]

MERMAID_FENCE = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)

HTML_HEAD = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({ startOnLoad: true, securityLevel: "loose" });</script>
<style>
  @page { size: A4; margin: 20mm 16mm; }
  body { font-family: -apple-system, Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.5; color: #111; }
  h1 { font-size: 15pt; border-bottom: 2px solid #333; padding-bottom: 4px; margin-top: 0; }
  h2 { font-size: 12.5pt; margin-top: 18px; }
  h3 { font-size: 11pt; }
  table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9pt; }
  th, td { border: 1px solid #999; padding: 4px 6px; text-align: left; vertical-align: top; }
  th { background: #eee; }
  code { background: #f2f2f2; padding: 1px 4px; border-radius: 3px; font-size: 9.5pt; }
  pre code { display: block; padding: 8px; overflow-x: auto; white-space: pre-wrap; }
  blockquote { border-left: 3px solid #999; margin: 8px 0; padding: 2px 12px; color: #555; }
  .section { page-break-before: always; }
  .section:first-child { page-break-before: avoid; }
  .source-path { color: #777; font-size: 8.5pt; margin-top: -6px; }
  .titlepage { text-align: center; padding-top: 30%; page-break-after: always; }
  .titlepage h1 { border: none; font-size: 26pt; }
  .mermaid { text-align: center; }
  .mermaid svg { max-width: 100%; }
</style>
</head>
<body>
"""

HTML_TAIL = "</body></html>"


def protect_mermaid(md_text):
    blocks = []

    def repl(m):
        blocks.append(m.group(1).strip())
        return f"\n\nMERMAIDPLACEHOLDER{len(blocks) - 1}\n\n"

    return MERMAID_FENCE.sub(repl, md_text), blocks


def restore_mermaid(html_text, blocks):
    for i, code in enumerate(blocks):
        html_text = html_text.replace(
            f"<p>MERMAIDPLACEHOLDER{i}</p>", f'<pre class="mermaid">\n{code}\n</pre>'
        )
    return html_text


def build_html():
    parts = [HTML_HEAD]
    parts.append(
        '<div class="titlepage"><h1>CampusConnect</h1>'
        "<p>Campus Social Network — Requirements, Architecture &amp; Proof of Concept</p>"
        "<p>Assignment 1 Report — Omar Ibrahim, Salama Aldhaheri, Makar Ulesov, Aro Dana</p>"
        "<p>MBZUAI — generated from docs/ in this repository</p></div>"
    )
    for title, relpath in SECTIONS:
        path = DOCS / relpath
        md_text = path.read_text(encoding="utf-8")
        protected, mermaid_blocks = protect_mermaid(md_text)
        body_html = markdown.markdown(protected, extensions=["tables", "fenced_code"])
        body_html = restore_mermaid(body_html, mermaid_blocks)
        parts.append(f'<div class="section">')
        parts.append(f'<div class="source-path">docs/{relpath}</div>')
        parts.append(body_html)
        parts.append("</div>")
    parts.append(HTML_TAIL)
    return "\n".join(parts)


def main():
    html = build_html()
    html_path = DOCS / "_report_build.html"
    html_path.write_text(html, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(f"file://{html_path}")
        n_diagrams = html.count('class="mermaid"')
        if n_diagrams:
            page.wait_for_function(
                f"document.querySelectorAll('.mermaid svg').length >= {n_diagrams}",
                timeout=30000,
            )
        page.pdf(path=str(OUTPUT), format="A4", print_background=True,
                 margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        browser.close()

    html_path.unlink()
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
