#!/usr/bin/env python3
"""Assemble Report.pdf from the section files tracked under docs/.

Each section already lives in its own reviewed Markdown file (single source
of truth per the repo's doc map in README.md). This script only concatenates
them in assignment order, renders Mermaid diagrams live via headless
Chromium, and prints the result to PDF. Re-run after editing any section:

    python docs/build_report.py   (needs docs/report-requirements.txt)
"""
import re
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUTPUT = ROOT / "Report.pdf"

# (Section title, file relative to docs/) in the brief's section order.
SECTIONS = [
    ("Product Scope", "requirements/scope.md"),
    ("1.1 Stakeholders", "requirements/stakeholders.md"),
    ("1.2 Functional Requirements", "requirements/functional-requirements.md"),
    ("1.3 Non-Functional Requirements and 2.1 Architectural Drivers", "requirements/non-functional-requirements.md"),
    ("1.4 User Stories and Scenarios", "requirements/user-stories.md"),
    ("1.5 Validation and Traceability", "requirements/requirements-review.md"),
    ("2.2 C4 System Context", "architecture/diagrams/c4-context.md"),
    ("2.2 C4 Containers", "architecture/diagrams/c4-container.md"),
    ("2.2 C4 Components (Backend API)", "architecture/diagrams/c4-component.md"),
    ("2.3 Behaviour and Design Decisions", "architecture/behaviour-and-design.md"),
    ("2.3 Collaborative Sequence Diagram", "architecture/diagrams/sequence-draft-handoff.md"),
    ("2.4 Interfaces", "architecture/api-contract.md"),
    ("2.5 Code and Repository Structure", "architecture/repository-structure.md"),
    ("2.6 Data Model", "architecture/diagrams/er-diagram.md"),
    ("2.7 ADR-01 Audience Visibility and Access Control (Salama)", "architecture/adr/adr-01-visibility-access-control.md"),
    ("2.7 ADR-02 AI Feature (Aro)", "architecture/adr/adr-02-ai-feature.md"),
    ("2.7 ADR-03 Data Storage (Makar)", "architecture/adr/adr-03-data-storage.md"),
    ("2.7 ADR-04 Collaboration and Concurrent Editing (Omar)", "architecture/adr/adr-04-collaboration-concurrent-editing.md"),
    ("3 Project Management and Team Collaboration", "project-management/README.md"),
    ("4 Proof of Concept", "poc.md"),
    ("4 Proof-of-Concept Sequence", "architecture/diagrams/sequence-create-post.md"),
    ("4 Demo Script", "demo-script.md"),
]

MERMAID_FENCE = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)

HTML_HEAD = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({ startOnLoad: true, securityLevel: "loose" });</script>
<style>
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
  .source-path { color: #777; font-size: 8.5pt; margin: -6px 0 10px; }
  .titlepage { text-align: center; padding-top: 30%; page-break-after: always; }
  .titlepage h1 { border: none; font-size: 26pt; }
  .toc { page-break-after: always; }
  .toc ol { line-height: 1.9; }
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
        "<p>AI1220 — MBZUAI — October 2026</p>"
        "<p>Repository: github.com/omar07ibrahim/campus-social-network</p></div>"
    )
    parts.append('<div class="toc"><h1>Contents</h1><ol>')
    for i, (title, _) in enumerate(SECTIONS):
        parts.append(f'<li><a href="#s{i}">{title}</a></li>')
    parts.append("</ol></div>")
    for i, (title, relpath) in enumerate(SECTIONS):
        path = DOCS / relpath
        md_text = path.read_text(encoding="utf-8")
        protected, mermaid_blocks = protect_mermaid(md_text)
        body_html = markdown.markdown(protected, extensions=["tables", "fenced_code"])
        body_html = restore_mermaid(body_html, mermaid_blocks)
        parts.append(f'<div class="section" id="s{i}">')
        source = f'<div class="source-path">Source: docs/{relpath}</div>'
        parts.append(body_html.replace("</h1>", "</h1>" + source, 1))
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
                 display_header_footer=True, header_template="<span></span>",
                 footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#777">'
                                 'CampusConnect — Assignment 1 — <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                 margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"})
        browser.close()

    html_path.unlink()
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
