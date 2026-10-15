"""Generates the before/after SVG markup for the automation showcase.

Usage: python tools/gen_showcase.py out.html  -> writes both <svg> elements;
paste them into the #automation section of index.html. Edit ROWS / KPIS / SUP
here so the dashboard figures keep reconciling to the workbook rows."""
import re
import sys
from html import escape

W, H = 640, 400

# ---------------- BEFORE: messy workbook ----------------
COLS = [  # name, x, width, clean anchor
    ("Date", 16, 104, "start"),
    ("Supplier", 120, 170, "start"),
    ("TRN", 290, 118, "start"),
    ("Amount", 408, 96, "end"),
    ("VAT", 504, 80, "end"),
    ("", 584, 40, "middle"),
]
HEAD_Y, HEAD_H = 44, 32
ROW_Y, ROW_H = 76, 36


def ax(ci, anchor):
    _, x, w, _ = COLS[ci]
    return {"start": x + 10, "end": x + w - 10, "middle": x + w / 2}[anchor]


# cell = (messy text, messy anchor, extra dx, messy class, clean text or None, flag)
# flag: None | 'problem' (red) | 'dup' (amber, applied per row)
ROWS = [
    [("03/04/26", "start", 0, "", "03 Apr 2026", None),
     ("Northwind Trading", "start", 0, "", None, None),
     ("100•••••0003", "start", 0, "", None, None),
     ("1,250.00", "end", 0, "", None, None),
     ("62.5", "end", -14, "", "62.50", "problem")],
    [("2026-04-05", "end", 0, "", "05 Apr 2026", None),
     ("northwind trdg", "start", 12, "", "Northwind Trading", None),
     ("#N/A", "start", 0, "is-error", "100•••••0003", "problem"),
     ("AED 980", "start", 0, "", "980.00", None),
     ("49", "middle", 0, "", "49.00", None)],
    [("5 Apr", "start", 0, "", "05 Apr 2026", None),
     ("Dune Office Supplies", "start", 0, "", None, None),
     ("100•••••0071", "start", 0, "", None, None),
     ("1.430,50", "end", 0, "", "1,430.50", "problem"),
     ("71.53", "end", 0, "", None, None)],
    [("05/04/2026", "start", 0, "", None, None),           # duplicate of the row above
     ("Dune Office Supplies", "start", 0, "", None, None),
     ("100•••••0071", "start", 0, "", None, None),
     ("1.430,50", "end", 0, "", None, None),
     ("71.53", "end", 0, "", None, None)],
    [("Apr-7", "start", 18, "", "07 Apr 2026", None),
     ("FALCON LOGISTICS", "start", 0, "", "Falcon Logistics", None),
     ("", "start", 0, "", "100•••••0145", "problem"),
     ("2100", "start", 6, "", "2,100.00", None),
     ("", "end", 0, "", "105.00", "problem")],
    [("08.04.26", "start", 0, "", "08 Apr 2026", None),
     ("Palm Media FZ", "start", 0, "is-highlight", None, None),
     ("100•••••0256", "start", 0, "", None, None),
     ("760.00", "end", 0, "", None, None),
     ("38", "end", 0, "", "38.00", None)],
]
DUP_ROWS = {2, 3}
DUP_REMOVED = 3
TOTAL = [("Total", "start", 0, "is-bold", None, None),
         ("", "start", 0, "", None, None),
         ("", "start", 0, "", None, None),
         ("#VALUE!", "end", 0, "is-error", "6,520.50", "problem"),
         ("=SUM(E2:E7)", "end", 0, "is-formula", "326.03", "problem")]


def cell_markup(ci, y, cell):
    messy, manchor, dx, cls, clean, flag = cell
    _, x, w, canchor = COLS[ci]
    out = []
    ty = y + ROW_H / 2 + 4.5
    if flag == "problem":
        out.append(f'<rect class="problem-fill" x="{x}" y="{y}" width="{w}" height="{ROW_H}" />')
        out.append(f'<path class="flag" d="M{x + w - 9} {y + 1}h8v8z" />')
    mx = ax(ci, manchor) + dx
    if messy:
        if clean is None and manchor == canchor and dx == 0:
            out.append(f'<text class="cell {cls}".strip() x="{mx:g}" y="{ty:g}" text-anchor="{manchor}">{escape(messy)}</text>'.replace('".strip()', '"'))
        else:
            cx = ax(ci, canchor)
            out.append(f'<text class="cell messy {cls}" x="{mx:g}" y="{ty:g}" text-anchor="{manchor}" data-dx="{cx - mx:g}">{escape(messy)}</text>')
    if clean is not None or (messy and (manchor != canchor or dx != 0)):
        cx = ax(ci, canchor)
        out.append(f'<text class="cell clean" x="{cx:g}" y="{ty:g}" text-anchor="{canchor}">{escape(clean if clean is not None else messy)}</text>')
    return out


def row_markup(cells, y, cls, tick=True, bold=False):
    parts = [f'<g class="{cls}">']
    for ci, (_, x, w, _) in enumerate(COLS):
        parts.append(f'<rect class="gridcell" x="{x}" y="{y}" width="{w}" height="{ROW_H}" />')
    for ci, cell in enumerate(cells):
        parts += cell_markup(ci, y, cell)
    if tick:
        cx = ax(5, "middle")
        cy = y + ROW_H / 2
        parts.append(f'<path class="tick" d="M{cx - 6:g} {cy:g}l4 4 8-9" />')
    parts.append("</g>")
    return parts


before = [
    f'<svg class="scene scene--before" viewBox="0 0 {W} {H}" role="img" aria-labelledby="sc-before-t sc-before-d">',
    '<title id="sc-before-t">Before: a manual invoice workbook</title>',
    '<desc id="sc-before-d">A spreadsheet of April supplier invoices with mixed date and number formats, '
    'inconsistent supplier names, a duplicated invoice, missing tax registration numbers and a broken total.</desc>',
    f'<rect class="frame" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" />',
    f'<path class="chrome" d="M0.5 14.5a14 14 0 0 1 14-14h{W - 29}a14 14 0 0 1 14 14v17h-{W - 1}z" />',
    '<circle class="dot-r" cx="20" cy="16" r="4" /><circle class="dot-y" cx="34" cy="16" r="4" /><circle class="dot-g" cx="48" cy="16" r="4" />',
    '<text class="chrome-title" x="320" y="20" text-anchor="middle">Q2_invoices_FINAL_v3 (2).xlsx</text>',
    '<g class="sheet-head">',
]
for name, x, w, anchor in COLS:
    before.append(f'<rect class="headcell" x="{x}" y="{HEAD_Y}" width="{w}" height="{HEAD_H}" />')
    if name:
        before.append(f'<text class="head" x="{ax(COLS.index((name, x, w, anchor)), anchor):g}" y="{HEAD_Y + 20}" text-anchor="{anchor}">{name}</text>')
before.append("</g>")

for i, cells in enumerate(ROWS):
    y = ROW_Y + i * ROW_H
    cls = "row"
    if i == DUP_REMOVED:
        cls += " dup-row"
    elif i > DUP_REMOVED:
        cls += " row-below"
    g = row_markup(cells, y, cls, tick=(i != DUP_REMOVED))
    if i in DUP_ROWS:
        g.insert(1, f'<rect class="dup-fill" x="16" y="{y}" width="568" height="{ROW_H}" />')
        g.insert(2, f'<path class="flag flag--dup" d="M{16 + 568 - 9} {y + 1}h8v8z" />')
    before += g
ty = ROW_Y + len(ROWS) * ROW_H
before += row_markup(TOTAL, ty, "row row-below row-total")

before += [
    f'<g class="sheet-tabs"><rect class="tabbar" x="0.5" y="{H - 40}" width="{W - 1}" height="39.5" />',
    f'<text class="tabtext is-active" x="24" y="{H - 15}">Sheet1</text>',
    f'<text class="tabtext" x="88" y="{H - 15}">Sheet1 (2)</text>',
    f'<text class="tabtext" x="176" y="{H - 15}">Copy of Sheet1</text>',
    f'<text class="tabtext" x="300" y="{H - 15}">OLD - do not use</text></g>',
    "</svg>",
]

# ---------------- AFTER: dashboard ----------------
after = [
    f'<svg class="scene scene--after" viewBox="0 0 {W} {H}" role="img" aria-labelledby="sc-after-t sc-after-d">',
    '<title id="sc-after-t">After: a reconciled dashboard</title>',
    '<desc id="sc-after-d">The same April invoices, cleaned and reconciled: expenses AED 6,520.50, input VAT AED 326.03, '
    '5 of 5 documents reconciled, a monthly expenses chart and expenses by supplier.</desc>',
    f'<rect class="frame" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" />',
    f'<path class="chrome" d="M0.5 14.5a14 14 0 0 1 14-14h{W - 29}a14 14 0 0 1 14 14v17h-{W - 1}z" />',
    '<circle class="dot-r" cx="20" cy="16" r="4" /><circle class="dot-y" cx="34" cy="16" r="4" /><circle class="dot-g" cx="48" cy="16" r="4" />',
    '<text class="chrome-title" x="320" y="20" text-anchor="middle">April close · Dashboard</text>',
    '<g class="chip"><rect x="532" y="7" width="92" height="20" rx="10" /><path d="M545 17l3 3 6-6.5" /><text x="560" y="21">Reconciled</text></g>',
]
KPIS = [("Expenses (Apr)", "AED ", 6520.50, 2), ("Input VAT (Apr)", "AED ", 326.03, 2), ("Documents reconciled", "", 5, 0)]
for i, (label, prefix, value, dec) in enumerate(KPIS):
    x = 16 + i * 210
    shown = f"{prefix}{value:,.{dec}f}" if dec else f"{int(value)} of 5"
    fmt = "of5" if not dec else "aed"
    after += [
        f'<g class="tile"><rect class="panel" x="{x}" y="48" width="198" height="84" rx="10" />',
        f'<text class="kpi-label" x="{x + 16}" y="76">{escape(label)}</text>',
        f'<text class="kpi-value" x="{x + 16}" y="112" data-value="{value}" data-format="{fmt}">{escape(shown)}</text></g>',
    ]
# Monthly expenses (illustrative heights; April matches the sheet total)
after += ['<g class="chart"><rect class="panel" x="16" y="146" width="290" height="238" rx="10" />',
          '<text class="panel-title" x="32" y="174">Monthly expenses</text>',
          '<path class="axis" d="M32 352h258" />']
for i, (m, h) in enumerate([("Jan", 96), ("Feb", 118), ("Mar", 104), ("Apr", 150)]):
    x = 50 + i * 62
    cls = "m-bar is-current" if m == "Apr" else "m-bar"
    after += [f'<rect class="{cls}" x="{x}" y="{352 - h}" width="34" height="{h}" rx="4" />',
              f'<text class="axis-label" x="{x + 17}" y="371" text-anchor="middle">{m}</text>']
after.append("</g>")
# By supplier (derived from the cleaned sheet)
SUP = [("Northwind Trading", 2230.00), ("Falcon Logistics", 2100.00), ("Dune Office Supplies", 1430.50), ("Palm Media FZ", 760.00)]
after += ['<g class="suppliers"><rect class="panel" x="320" y="146" width="304" height="238" rx="10" />',
          '<text class="panel-title" x="336" y="174">By supplier (Apr)</text>']
for i, (name, v) in enumerate(SUP):
    y = 206 + i * 44
    after += [f'<text class="sup-label" x="336" y="{y}">{escape(name)}</text>',
              f'<text class="sup-value" x="608" y="{y}" text-anchor="end">{v:,.2f}</text>',
              f'<rect class="s-track" x="336" y="{y + 8}" width="272" height="8" rx="4" />',
              f'<rect class="s-bar" x="336" y="{y + 8}" width="{272 * v / 2230:.1f}" height="8" rx="4" />']
after += ["</g>", "</svg>"]

out = "<!--BEFORE-->\n" + "\n".join(before) + "\n<!--AFTER-->\n" + "\n".join(after) + "\n"
out = re.sub(r'class="([^"]*?)\s+"', r'class="\1"', out)  # tidy empty modifier classes
with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write(out)
print("ok", len(out))
