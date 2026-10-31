"""Merges docs/01-08 into one Word file. Mermaid diagrams don't survive, the .md files have them.
"""
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches

ROOT = Path(__file__).resolve().parent.parent
FILES = sorted((ROOT / "docs").glob("0[1-8]_*.md"))


def add_runs(par, text):
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        r = par.add_run(re.sub(r"`([^`]*)`", r"\1", part))
        r.bold = i % 2 == 1


def table(doc, rows):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]), style="Light Grid Accent 1")
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            t.cell(i, j).text = ""
            add_runs(t.cell(i, j).paragraphs[0], cell)
            for r in t.cell(i, j).paragraphs[0].runs:
                r.font.size = Pt(8.5)
                r.bold = r.bold or i == 0


def main():
    d = Document()
    s = d.sections[0]
    s.left_margin = s.right_margin = Inches(0.8)
    s.top_margin = s.bottom_margin = Inches(0.7)
    d.styles["Normal"].font.name = "Calibri"
    d.styles["Normal"].font.size = Pt(10)
    d.add_heading("Refund and Cancellation Reduction: Business Analysis Case Pack", 0)
    d.add_paragraph("Fictional marketplace: Plateful. All data is synthetic. Stakeholder needs are assumptions to be validated in interviews.").runs[0].bold = True
    d.add_paragraph("Contents: 1 Problem and scope; 2 Stakeholders; 3 Process as-is and to-be; 4 Requirements (BRD); 5 User stories; 6 UAT plan; 7 KPIs and benefits case; 8 RAID and rollout.")
    for f in FILES:
        d.add_page_break()
        lines = f.read_text(encoding="utf-8").splitlines()
        i, in_code = 0, False
        while i < len(lines):
            ln = lines[i]
            if ln.startswith("```"):
                if not in_code and ln.strip() == "```mermaid":
                    d.add_paragraph("[Diagram: see the Markdown version of this document]").runs[0].italic = True
                in_code = not in_code
            elif in_code:
                pass
            elif ln.startswith("|"):
                block = []
                while i < len(lines) and lines[i].startswith("|"):
                    if not re.match(r"^\|[\s\-:|]+\|$", lines[i]):
                        block.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                    i += 1
                table(d, block)
                continue
            elif ln.startswith("# "):
                d.add_heading(ln[2:], 1)
            elif ln.startswith("## "):
                d.add_heading(ln[3:], 2)
            elif ln.startswith("### "):
                d.add_heading(ln[4:], 3)
            elif ln.startswith("> "):
                p = d.add_paragraph()
                add_runs(p, ln[2:])
                p.runs[0].italic = True
            elif re.match(r"^\s*- ", ln):
                add_runs(d.add_paragraph(style="List Bullet"), re.sub(r"^\s*- ", "", ln))
            elif re.match(r"^\d+\. ", ln):
                add_runs(d.add_paragraph(style="List Number"), re.sub(r"^\d+\. ", "", ln))
            elif ln.startswith("!["):
                pass
            elif ln.strip():
                add_runs(d.add_paragraph(), ln)
            i += 1
    d.save(ROOT / "docs" / "BA_Case_Pack.docx")
    print("BA_Case_Pack.docx written from", len(FILES), "documents")


if __name__ == "__main__":
    main()
