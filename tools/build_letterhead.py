"""Builds the Word letterhead: tools/.out/Accuminds-Letterhead.docx (A4).

Needs tools/.out/letterhead-logo.png first (see tools/letterhead-logo.html).
Run from the repo root:  python tools/build_letterhead.py
Placeholders in [square brackets] are filled in per letter; the licence and TRN
placeholders are highlighted until the real numbers are added here.
"""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

OUT = Path(__file__).parent / ".out"
NAVY, GOLD, GREY = RGBColor(0x1A, 0x2E, 0x4A), RGBColor(0xC9, 0x97, 0x2B), RGBColor(0x5B, 0x67, 0x78)
FONT = "Calibri"  # installed everywhere Word runs; the brand font lives in the logo image

# TODO: replace with the real numbers once confirmed, and drop the highlight
LICENCE, TRN = "[Licence no.]", "[TRN]"


def border(paragraph, side, colour, size_eighths, space=4):
    p_pr = paragraph._p.get_or_add_pPr()
    bdr = p_pr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr")
        p_pr.append(bdr)
    el = OxmlElement(f"w:{side}")
    for k, v in {"val": "single", "sz": str(size_eighths), "space": str(space), "color": colour}.items():
        el.set(qn(f"w:{k}"), v)
    bdr.append(el)


def run(paragraph, text, size=10, colour=None, bold=False, highlight=False):
    r = paragraph.add_run(text)
    r.font.name, r.font.size, r.font.bold = FONT, Pt(size), bold
    if colour:
        r.font.color.rgb = colour
    if highlight:
        r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return r


def tight(paragraph, before=0, after=0, align=None):
    pf = paragraph.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), 1.0
    if align is not None:
        paragraph.alignment = align
    return paragraph


def build():
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = FONT, Pt(10.5)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    normal.font.color.rgb = RGBColor(0x22, 0x2B, 0x36)
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = 1.15

    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin = s.right_margin = Cm(2.2)
    s.top_margin, s.bottom_margin = Cm(4.2), Cm(2.8)
    s.header_distance, s.footer_distance = Cm(1.1), Cm(0.9)
    width = s.page_width - s.left_margin - s.right_margin

    # ---- Header: logo left, contact details right, gold rule underneath
    head = s.header
    head.paragraphs[0].text = ""
    t = head.add_table(1, 2, width)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    mar = OxmlElement("w:tblCellMar")  # no cell padding, so logo and text line up with the rule
    for side in ("left", "right"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), "0")
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    t._tbl.tblPr.append(mar)
    left, right = t.rows[0].cells
    left.width, right.width = Cm(9.6), width - Cm(9.6)
    tight(left.paragraphs[0]).add_run().add_picture(str(OUT / "letterhead-logo.png"), width=Cm(7.4))
    for i, line in enumerate(["+971 50 98 67247", "info@accumindsconsulting.ae", "www.accumindsconsulting.ae"]):
        p = right.paragraphs[0] if i == 0 else right.add_paragraph()
        run(tight(p, after=1, align=WD_ALIGN_PARAGRAPH.RIGHT), line, 9, GREY)
    right.vertical_alignment = 1  # centre
    rule = tight(head.add_paragraph(), before=6)
    border(rule, "bottom", "C9972B", 12)
    head.paragraphs[0]._p.getparent().remove(head.paragraphs[0]._p)

    # ---- Footer: legal details over a thin navy rule, page number right
    foot = s.footer
    p = tight(foot.paragraphs[0], align=WD_ALIGN_PARAGRAPH.CENTER)
    border(p, "top", "1A2E4A", 4, space=6)
    run(p, "Accuminds Consulting FZCO", 8.5, NAVY, bold=True)
    run(p, "  ·  DSO – IFZA, IFZA Properties, Dubai Silicon Oasis, Dubai, UAE", 8.5, GREY)
    p = tight(foot.add_paragraph(), before=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    run(p, "IFZA trade licence no. ", 8.5, GREY)
    run(p, LICENCE, 8.5, GREY, highlight=LICENCE.startswith("["))
    run(p, "  ·  TRN ", 8.5, GREY)
    run(p, TRN, 8.5, GREY, highlight=TRN.startswith("["))

    # ---- Body: a ready-to-edit letter layout
    def para(text="", after=8, **kw):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        if text:
            run(p, text, **kw)
        return p

    doc.paragraphs[0]._p.getparent().remove(doc.paragraphs[0]._p) if doc.paragraphs else None
    para("[Date]", after=14, size=10.5)
    for i, line in enumerate(["[Recipient name]", "[Title]", "[Company]", "[Address]"]):
        para(line, after=0 if i < 3 else 14, size=10.5)
    para("Subject: [Subject]", after=12, size=10.5, colour=NAVY, bold=True)
    para("Dear [Name],", size=10.5)
    para("[Letter text.]", after=20, size=10.5)
    para("Yours sincerely,", after=36, size=10.5)
    para("[Name]", after=0, size=10.5, colour=NAVY, bold=True)
    para("[Title]", after=0, size=10.5)
    para("Accuminds Consulting FZCO", after=0, size=10.5)

    doc.core_properties.title = "Accuminds Consulting FZCO letterhead"
    doc.core_properties.author = "Accuminds Consulting FZCO"
    out = OUT / "Accuminds-Letterhead.docx"
    doc.save(out)
    print("wrote", out)


if __name__ == "__main__":
    build()
