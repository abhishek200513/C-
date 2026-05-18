"""
Generate 0/1 Knapsack Theory Word Document
with expanded theory, recurrence, comparison with fractional knapsack,
worked example, and test cases with DP tables.
Same formatting style as LCS & MCM docs.
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml


def fix_heading(heading):
    heading.paragraph_format.space_after = Pt(0)
    return heading


def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f'<w:tblPr {nsdecls("w")}/>')
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '  <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '  <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '  <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '</w:tblBorders>'
    )
    tblPr.append(borders)


def add_styled_para(doc, text, bold=False, italic=False, size=11, font='Times New Roman'):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = font
    return p


def add_bullet(doc, text, size=10, font='Times New Roman'):
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = font
    return p


def add_sub_bullet(doc, text, size=9, font='Times New Roman'):
    """Add an indented sub-point (using normal paragraph with indent)."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Pt(36)
    run = p.add_run("○ " + text)
    run.font.size = Pt(size)
    run.font.name = font
    return p


# =====================================================================
#  0/1 Knapsack DP Solver
# =====================================================================

def solve_knapsack(weights, profits, n, capacity):
    """
    Solve 0/1 knapsack and return:
      - dp[][] table
      - step-by-step row traces
      - list of selected items
    """
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # row_traces: list of (i, weight_i, profit_i, cell_traces)
    # cell_traces: list of (w, explanation, value)
    row_traces = []

    for i in range(1, n + 1):
        cell_traces = []
        for w in range(0, capacity + 1):
            if weights[i - 1] <= w:
                include = profits[i - 1] + dp[i - 1][w - weights[i - 1]]
                exclude = dp[i - 1][w]
                if include > exclude:
                    dp[i][w] = include
                    explanation = (
                        f"w[{i}]={weights[i-1]} ≤ {w}: "
                        f"include = p[{i}] + dp[{i-1}][{w}-{weights[i-1]}] = "
                        f"{profits[i-1]} + {dp[i-1][w - weights[i-1]]} = {include} > "
                        f"exclude = dp[{i-1}][{w}] = {exclude}  →  dp[{i}][{w}] = {include}"
                    )
                else:
                    dp[i][w] = exclude
                    explanation = (
                        f"w[{i}]={weights[i-1]} ≤ {w}: "
                        f"include = {profits[i-1]} + {dp[i-1][w - weights[i-1]]} = {include} ≤ "
                        f"exclude = {exclude}  →  dp[{i}][{w}] = {exclude}"
                    )
            else:
                dp[i][w] = dp[i - 1][w]
                explanation = (
                    f"w[{i}]={weights[i-1]} > {w}: item too heavy  →  dp[{i}][{w}] = dp[{i-1}][{w}] = {dp[i][w]}"
                )
            cell_traces.append((w, explanation, dp[i][w]))
        row_traces.append((i, weights[i - 1], profits[i - 1], cell_traces))

    # Traceback — find selected items
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append((i, weights[i - 1], profits[i - 1]))
            w -= weights[i - 1]
    selected.reverse()

    return dp, row_traces, selected


# =====================================================================
#  Add DP table to document
# =====================================================================

def add_dp_table(doc, dp, n, capacity, weights, profits):
    """Add the full DP table to the document."""
    add_styled_para(doc, "DP Table (dp[i][w]):", bold=True, size=11)

    # Limit display if capacity is large
    if capacity > 15:
        add_styled_para(doc,
            f"(Table has {capacity + 1} columns — showing abbreviated view)",
            size=9, italic=True)

    tbl = doc.add_table(rows=n + 2, cols=capacity + 2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    # Top-left corner
    cell = tbl.cell(0, 0)
    cell.text = "i\\w"
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True; r.font.size = Pt(8); r.font.name = 'Times New Roman'
    set_cell_shading(cell, "D9E2F3")

    # Column headers (w = 0 to capacity)
    for w in range(capacity + 1):
        cell = tbl.cell(0, w + 1)
        cell.text = str(w)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(8); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

    # Row headers and data
    for i in range(n + 1):
        cell = tbl.cell(i + 1, 0)
        if i == 0:
            cell.text = "0"
        else:
            cell.text = f"{i}(w={weights[i-1]},p={profits[i-1]})"
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(7); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

        for w in range(capacity + 1):
            cell = tbl.cell(i + 1, w + 1)
            cell.text = str(dp[i][w])
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.size = Pt(8); r.font.name = 'Times New Roman'

    doc.add_paragraph()


# =====================================================================
#  Add a complete test case
# =====================================================================

def add_test_case(doc, case_num, label, weights, profits, capacity, show_trace=True):
    n = len(weights)

    heading = doc.add_heading(f'Test Case {case_num}: {label}', level=2)
    fix_heading(heading)
    for run in heading.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    # Input
    add_styled_para(doc, "Input:", bold=True, size=11)
    add_styled_para(doc, f"Number of items: n = {n}", size=11)
    add_styled_para(doc, f"Knapsack capacity: W = {capacity}", size=11)

    # Item table
    item_tbl = doc.add_table(rows=n + 1, cols=3)
    item_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(item_tbl)

    headers = ["Item", "Weight", "Profit"]
    for ci, h in enumerate(headers):
        cell = item_tbl.cell(0, ci)
        cell.text = h
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(10); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

    for i in range(n):
        for ci, val in enumerate([i + 1, weights[i], profits[i]]):
            cell = item_tbl.cell(i + 1, ci)
            cell.text = str(val)
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.size = Pt(10); r.font.name = 'Times New Roman'
    doc.add_paragraph()

    # Solve
    dp, row_traces, selected = solve_knapsack(weights, profits, n, capacity)

    # Step-by-step trace (only for small cases)
    if show_trace and capacity <= 10:
        add_styled_para(doc, "DP Fill Trace (row by row):", bold=True, size=11)
        add_styled_para(doc, "Base case: dp[0][w] = 0 for all w (no items selected).", size=10, italic=True)

        for (i, wi, pi, cell_traces) in row_traces:
            add_styled_para(doc, f"Row i={i} (Item {i}: weight={wi}, profit={pi})", bold=True, size=10)
            for (w, explanation, value) in cell_traces:
                if w == 0:
                    continue  # skip w=0 (always 0)
                add_bullet(doc, f"w={w}: {explanation}", size=9)

    # DP Table
    if capacity <= 15:
        add_dp_table(doc, dp, n, capacity, weights, profits)

    # Selected items
    add_styled_para(doc, "Traceback — Selected Items:", bold=True, size=11)
    if selected:
        sel_tbl = doc.add_table(rows=len(selected) + 1, cols=3)
        sel_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(sel_tbl)

        for ci, h in enumerate(["Item", "Weight", "Profit"]):
            cell = sel_tbl.cell(0, ci)
            cell.text = h
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.bold = True; r.font.size = Pt(10); r.font.name = 'Times New Roman'
            set_cell_shading(cell, "D9E2F3")

        total_w = 0
        total_p = 0
        for idx, (item_id, w, p_val) in enumerate(selected):
            for ci, val in enumerate([item_id, w, p_val]):
                cell = sel_tbl.cell(idx + 1, ci)
                cell.text = str(val)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.size = Pt(10); r.font.name = 'Times New Roman'
            total_w += w
            total_p += p_val
        doc.add_paragraph()
        add_styled_para(doc, f"Total Weight = {total_w} / {capacity}", size=11)
    else:
        add_styled_para(doc, "No items selected.", size=11)
        total_p = 0

    # Output
    add_styled_para(doc, "Output:", bold=True, size=11)
    add_styled_para(doc, f"Maximum Profit = {dp[n][capacity]}", size=11)

    doc.add_page_break()


# =====================================================================
#  Create the full document
# =====================================================================

def create_document():
    doc = Document()

    # Page margins
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    # Default font
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    # Remove spacing after heading styles
    for i in range(4):
        hs = doc.styles[f'Heading {i}'] if i > 0 else doc.styles['Title']
        hs.paragraph_format.space_after = Pt(0)

    # ===== TITLE =====
    title = doc.add_heading('Experiment 16', level=0)
    fix_heading(title)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(22)
        run.font.color.rgb = RGBColor(0, 0, 0)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('0/1 Knapsack Problem using Dynamic Programming')
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'
    doc.add_paragraph()

    # ===== AIM =====
    h = doc.add_heading('Aim:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_paragraph(
        'To solve the 0/1 Knapsack problem using the dynamic programming (bottom-up tabulation) '
        'approach and determine the maximum profit achievable within a given weight capacity, '
        'along with the set of items selected.'
    )

    # ===== PROBLEM STATEMENT =====
    h = doc.add_heading('Problem Statement:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_paragraph(
        'Given n items, each with a weight wᵢ and a profit pᵢ, and a knapsack with maximum weight '
        'capacity W, determine the subset of items to include in the knapsack such that the total '
        'weight does not exceed W and the total profit is maximized. Each item can either be taken '
        'completely or not taken at all (hence "0/1").'
    )

    # ===== THEORY =====
    h = doc.add_heading('Theory:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    # Introduction
    p = doc.add_paragraph()
    run = p.add_run(
        'The 0/1 Knapsack problem is one of the most fundamental problems in combinatorial '
        'optimization and computer science. It models scenarios where a decision-maker must choose '
        'a subset of items — each with a given weight and profit — to maximize total profit without '
        'exceeding a weight limit. The "0/1" constraint means each item is either fully included or '
        'fully excluded; partial fractions are not allowed. This problem arises in resource allocation, '
        'financial portfolio selection, cargo loading, and cutting-stock problems.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Optimal Substructure
    p = doc.add_paragraph()
    run = p.add_run('Optimal Substructure Property:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'The 0/1 Knapsack problem exhibits optimal substructure. Consider item i with weight wᵢ '
        'and profit pᵢ. For a knapsack of capacity w, if item i is included in the optimal solution, '
        'then the remaining items must form an optimal solution for capacity w − wᵢ. If item i is '
        'excluded, the optimal solution is the same as the optimal solution for the first i−1 items '
        'with capacity w. This property, combined with overlapping subproblems (many subproblems are '
        'solved repeatedly in the recursive approach), makes the problem ideal for dynamic programming.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Recurrence Relation
    p = doc.add_paragraph()
    run = p.add_run('Recurrence Relation:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'Let dp[i][w] denote the maximum profit achievable using items 1 to i with knapsack '
        'capacity w. The recurrence relation is:'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Formula block
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        'dp[i][w] = 0                                          if i = 0 or w = 0\n'
        'dp[i][w] = dp[i-1][w]                                 if wᵢ > w\n'
        'dp[i][w] = max(dp[i-1][w], pᵢ + dp[i-1][w - wᵢ])     if wᵢ ≤ w'
    )
    run.bold = True; run.font.size = Pt(11); run.font.name = 'Consolas'

    p = doc.add_paragraph()
    run = p.add_run(
        'Base case: dp[0][w] = 0 for all w (no items → zero profit) and dp[i][0] = 0 for all i '
        '(zero capacity → zero profit). For each item i and capacity w, if the item\'s weight '
        'exceeds w, it cannot be included. Otherwise, we choose the maximum of excluding the item '
        '(dp[i-1][w]) or including it (pᵢ + dp[i-1][w − wᵢ]).'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # How it works with example
    p = doc.add_paragraph()
    run = p.add_run('How 0/1 Knapsack Works — Worked Example:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'Consider 3 items with weights {2, 3, 4} and profits {3, 4, 5}, and a knapsack capacity W = 5.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    add_styled_para(doc, "Step 1: Initialize the DP table with base cases.", size=11, italic=True)
    add_styled_para(doc, "dp[0][w] = 0 for w = 0, 1, 2, 3, 4, 5.", size=10, font='Consolas')

    add_styled_para(doc, "Step 2: Fill row i=1 (Item 1: w=2, p=3).", size=11, italic=True)
    for line in [
        "w=0: can't fit → dp[1][0] = 0",
        "w=1: w₁=2 > 1, can't fit → dp[1][1] = dp[0][1] = 0",
        "w=2: w₁=2 ≤ 2, include = 3 + dp[0][0] = 3, exclude = 0 → dp[1][2] = 3",
        "w=3: w₁=2 ≤ 3, include = 3 + dp[0][1] = 3, exclude = 0 → dp[1][3] = 3",
        "w=4: w₁=2 ≤ 4, include = 3 + dp[0][2] = 3, exclude = 0 → dp[1][4] = 3",
        "w=5: w₁=2 ≤ 5, include = 3 + dp[0][3] = 3, exclude = 0 → dp[1][5] = 3",
    ]:
        add_bullet(doc, line, size=9)

    add_styled_para(doc, "Step 3: Fill row i=2 (Item 2: w=3, p=4).", size=11, italic=True)
    for line in [
        "w=0,1,2: item too heavy → copy from above → dp[2][0..2] = {0, 0, 3}",
        "w=3: include = 4 + dp[1][0] = 4, exclude = 3 → dp[2][3] = 4",
        "w=4: include = 4 + dp[1][1] = 4, exclude = 3 → dp[2][4] = 4",
        "w=5: include = 4 + dp[1][2] = 7, exclude = 3 → dp[2][5] = 7",
    ]:
        add_bullet(doc, line, size=9)

    add_styled_para(doc, "Step 4: Fill row i=3 (Item 3: w=4, p=5).", size=11, italic=True)
    for line in [
        "w=0..3: item too heavy → copy from above → dp[3][0..3] = {0, 0, 3, 4}",
        "w=4: include = 5 + dp[2][0] = 5, exclude = 4 → dp[3][4] = 5",
        "w=5: include = 5 + dp[2][1] = 5, exclude = 7 → dp[3][5] = 7",
    ]:
        add_bullet(doc, line, size=9)

    add_styled_para(doc, "Result: dp[3][5] = 7. Traceback: Items 1 and 2 selected (weight 2+3=5, profit 3+4=7).",
                    bold=True, size=11)

    # Final DP table for the example
    add_styled_para(doc, "DP Table for the example:", bold=True, size=11)
    example_dp = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 3, 3, 3, 3],
        [0, 0, 3, 4, 4, 7],
        [0, 0, 3, 4, 5, 7],
    ]
    ex_weights = [2, 3, 4]
    ex_profits = [3, 4, 5]
    ex_cap = 5

    tbl = doc.add_table(rows=5, cols=7)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    # Header
    cell = tbl.cell(0, 0)
    cell.text = "i\\w"
    for pp in cell.paragraphs:
        pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in pp.runs:
            r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
    set_cell_shading(cell, "D9E2F3")

    for w in range(6):
        cell = tbl.cell(0, w + 1)
        cell.text = str(w)
        for pp in cell.paragraphs:
            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in pp.runs:
                r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

    for i in range(4):
        cell = tbl.cell(i + 1, 0)
        cell.text = str(i)
        for pp in cell.paragraphs:
            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in pp.runs:
                r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

        for w in range(6):
            cell = tbl.cell(i + 1, w + 1)
            cell.text = str(example_dp[i][w])
            for pp in cell.paragraphs:
                pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in pp.runs:
                    r.font.size = Pt(9); r.font.name = 'Times New Roman'
    doc.add_paragraph()

    # Time Complexity
    p = doc.add_paragraph()
    run = p.add_run('Time and Space Complexity:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    complexity_data = [
        ("Aspect", "Complexity"),
        ("Time Complexity", "O(n × W)"),
        ("Space Complexity", "O(n × W) for dp[][] table"),
        ("Traceback", "O(n)")
    ]
    for idx, (c1, c2) in enumerate(complexity_data):
        for ci, val in enumerate([c1, c2]):
            cell = table.cell(idx, ci)
            cell.text = val
            for par in cell.paragraphs:
                par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in par.runs:
                    r.font.size = Pt(10); r.font.name = 'Times New Roman'
                    if idx == 0: r.bold = True
            if idx == 0:
                set_cell_shading(cell, "D9E2F3")
    doc.add_paragraph()

    p = doc.add_paragraph()
    run = p.add_run(
        'Where n is the number of items and W is the knapsack capacity. The algorithm fills an '
        '(n+1) × (W+1) table, examining each cell exactly once. The traceback phase takes O(n) '
        'time to determine which items were selected. Note that this is a pseudo-polynomial '
        'time algorithm — it is polynomial in the numeric value of W, not in the number of bits '
        'needed to represent W.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # ===== DIFFERENCE: Fractional vs 0/1 =====
    p = doc.add_paragraph()
    run = p.add_run('Difference Between Fractional Knapsack and 0/1 Knapsack:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'While both problems involve selecting items to maximize profit within a weight constraint, '
        'they differ fundamentally in how items can be chosen:'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Comparison table
    comp_tbl = doc.add_table(rows=8, cols=3)
    comp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(comp_tbl)

    comp_data = [
        ("Aspect", "Fractional Knapsack", "0/1 Knapsack"),
        ("Item Selection", "Items can be taken in fractions", "Items are taken wholly or not at all"),
        ("Approach", "Greedy (sort by profit/weight ratio)", "Dynamic Programming (bottom-up table)"),
        ("Optimal Guarantee", "Greedy gives optimal solution", "Greedy does NOT guarantee optimality"),
        ("Time Complexity", "O(n log n) due to sorting", "O(n × W) — pseudo-polynomial"),
        ("Space Complexity", "O(1) extra space", "O(n × W) for DP table"),
        ("Solution Type", "May include fractional items", "Always integer (binary) selection"),
        ("Profit Relation", "Fractional profit ≥ 0/1 profit", "0/1 profit ≤ Fractional profit"),
    ]

    for idx, row_data in enumerate(comp_data):
        for ci, val in enumerate(row_data):
            cell = comp_tbl.cell(idx, ci)
            cell.text = val
            for par in cell.paragraphs:
                par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in par.runs:
                    r.font.size = Pt(9); r.font.name = 'Times New Roman'
                    if idx == 0: r.bold = True
            if idx == 0:
                set_cell_shading(cell, "D9E2F3")
    doc.add_paragraph()

    p = doc.add_paragraph()
    run = p.add_run(
        'Key insight: The greedy approach (sorting by profit-to-weight ratio) works perfectly for '
        'Fractional Knapsack because we can take any fraction of an item. However, for 0/1 Knapsack, '
        'the greedy approach may fail. For example, with items {(w=10, p=60), (w=20, p=100), '
        '(w=30, p=120)} and capacity W=50: greedy by ratio selects items 1 and 2 (profit=160), '
        'but the optimal 0/1 solution is items 2 and 3 (profit=220). Dynamic programming is '
        'required to guarantee the optimal solution for 0/1 Knapsack.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Advantages
    p = doc.add_paragraph()
    run = p.add_run('Advantages:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for adv in [
        'Guarantees the globally optimal solution.',
        'Systematic bottom-up approach avoids redundant computation.',
        'The DP table enables easy traceback to find selected items.',
        'Space can be optimized to O(W) using a 1D rolling array if only the max profit is needed.',
        'Applicable to a wide range of resource-constrained optimization problems.'
    ]:
        pp = doc.add_paragraph(adv, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # Limitations
    p = doc.add_paragraph()
    run = p.add_run('Limitations:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for lim in [
        'Pseudo-polynomial time: impractical for very large capacities (e.g., W = 10⁹).',
        'O(n × W) space can be prohibitive for large inputs.',
        'The problem is NP-hard in general (no known polynomial-time algorithm in input size).',
        'Cannot handle fractional items — use Fractional Knapsack for that.'
    ]:
        pp = doc.add_paragraph(lim, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # Applications
    p = doc.add_paragraph()
    run = p.add_run('Applications:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for app in [
        'Resource allocation and capital budgeting in project management.',
        'Cargo loading in logistics and transportation.',
        'Cutting stock problems in manufacturing.',
        'Cryptographic key generation and subset-sum based cryptosystems.',
        'Feature selection in machine learning with budget constraints.'
    ]:
        pp = doc.add_paragraph(app, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # ===== ALGORITHM =====
    h = doc.add_heading('Algorithm:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    for step in [
        'Initialize dp[i][0] = 0 for all i, and dp[0][w] = 0 for all w.',
        'For i = 1 to n:',
        '    For w = 1 to W:',
        '        If wᵢ > w: dp[i][w] = dp[i-1][w]  (item too heavy, skip)',
        '        Else: dp[i][w] = max(dp[i-1][w], pᵢ + dp[i-1][w - wᵢ])',
        'dp[n][W] gives the maximum profit.',
        'Traceback: For i = n down to 1, if dp[i][w] ≠ dp[i-1][w], item i is selected; set w = w - wᵢ.'
    ]:
        pp = doc.add_paragraph(step, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    add_styled_para(doc, "Pseudocode:", bold=True, size=12)
    pseudocode = """KNAPSACK-01(w[], p[], n, W):
    for i ← 0 to n do dp[i][0] ← 0
    for w ← 0 to W do dp[0][w] ← 0
    for i ← 1 to n do
        for w ← 1 to W do
            if w[i] > w then
                dp[i][w] ← dp[i-1][w]
            else
                dp[i][w] ← max(dp[i-1][w], p[i] + dp[i-1][w - w[i]])
    return dp[n][W]

TRACEBACK(dp[][], w[], n, W):
    w ← W
    for i ← n down to 1 do
        if dp[i][w] ≠ dp[i-1][w] then
            print "Item i selected"
            w ← w - w[i]"""
    p = doc.add_paragraph()
    run = p.add_run(pseudocode)
    run.font.size = Pt(10); run.font.name = 'Consolas'
    doc.add_paragraph()

    # ===== INPUT =====
    h = doc.add_heading('Input:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph('Using 4 predefined test cases with varying sizes and capacities.')
    doc.add_page_break()

    # ===== TEST CASES =====
    h = doc.add_heading('Test Cases:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    # Test Case 1: Classic textbook example (small, with full trace)
    add_test_case(doc, 1, "Classic Example",
                  weights=[2, 3, 4, 5],
                  profits=[3, 4, 5, 6],
                  capacity=7,
                  show_trace=True)

    # Test Case 2: All items fit
    add_test_case(doc, 2, "All Items Fit",
                  weights=[1, 2, 3],
                  profits=[6, 10, 12],
                  capacity=10,
                  show_trace=True)

    # Test Case 3: Single item that fits
    add_test_case(doc, 3, "Greedy Trap — Ratio vs Optimal",
                  weights=[10, 20, 30],
                  profits=[60, 100, 120],
                  capacity=50,
                  show_trace=False)

    # Test Case 4: No item fits
    add_test_case(doc, 4, "No Item Fits",
                  weights=[5, 8, 10],
                  profits=[20, 30, 50],
                  capacity=3,
                  show_trace=True)

    # ===== RESULT =====
    h = doc.add_heading('Result:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph(
        'All 4 predefined test cases were successfully executed. The 0/1 Knapsack DP algorithm '
        'correctly computed the maximum achievable profit and identified the optimal set of items '
        'for each test case.'
    )

    # ===== CONCLUSION =====
    h = doc.add_heading('Conclusion:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph(
        'The 0/1 Knapsack problem was successfully solved using the bottom-up dynamic programming '
        'approach. The algorithm constructed an (n+1) × (W+1) DP table by systematically evaluating '
        'whether to include or exclude each item for every possible capacity value. The recurrence '
        'relation dp[i][w] = max(dp[i-1][w], pᵢ + dp[i-1][w − wᵢ]) was applied to guarantee the '
        'globally optimal solution. The traceback phase identified the selected items by comparing '
        'adjacent rows of the DP table. The test cases covered diverse scenarios — a classic '
        'textbook example, a case where all items fit, a greedy trap where ratio-based selection '
        'fails but DP succeeds, and a case where no items can be packed — confirming the correctness '
        'and robustness of the O(n × W) implementation. The key difference from Fractional Knapsack '
        'was also demonstrated: the greedy approach fails for 0/1 selection, necessitating dynamic '
        'programming for optimality.'
    )

    # Save
    output_path = r"c:\C++\ADA\knapsack_01\Knapsack_01_Theory.docx"
    try:
        doc.save(output_path)
        print(f"Document saved to: {output_path}")
    except PermissionError:
        output_path = r"c:\C++\ADA\knapsack_01\Knapsack_01_Theory_v2.docx"
        doc.save(output_path)
        print(f"Original locked. Saved to: {output_path}")


if __name__ == "__main__":
    create_document()
