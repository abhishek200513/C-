"""
Generate LCS Theory Word Document
with expanded theory and new test cases.
Format: DP fill trace with directions, c[][] and b[][] tables, traceback.
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


def solve_lcs(X, Y):
    """
    Solve LCS and return c[][], b[][], and step-by-step trace.
    b[i][j] = 'D' (diagonal/match), 'U' (up), 'L' (left)
    """
    m = len(X)
    n = len(Y)

    c = [[0] * (n + 1) for _ in range(m + 1)]
    b = [[''] * (n + 1) for _ in range(m + 1)]

    # row_traces: list of (i, char_x, cell_traces)
    # cell_traces: list of (j, char_y, match, explanation, val, direction)
    row_traces = []

    for i in range(1, m + 1):
        cell_traces = []
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = 'D'
                explanation = f"Match: c[{i-1}][{j-1}] + 1 = {c[i][j]}"
                cell_traces.append((j, Y[j-1], True, explanation, c[i][j], '\u2196'))
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = 'U'
                explanation = f"No match: c[{i-1}][{j}]={c[i-1][j]} >= c[{i}][{j-1}]={c[i][j-1]}"
                cell_traces.append((j, Y[j-1], False, explanation, c[i][j], '\u2191'))
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = 'L'
                explanation = f"No match: c[{i}][{j-1}]={c[i][j-1]} > c[{i-1}][{j}]={c[i-1][j]}"
                cell_traces.append((j, Y[j-1], False, explanation, c[i][j], '\u2190'))

        row_traces.append((i, X[i-1], cell_traces))

    # Traceback
    traceback_steps = []
    lcs_str = ""
    i, j = m, n
    step = 0

    while i > 0 and j > 0:
        step += 1
        if b[i][j] == 'D':
            traceback_steps.append(
                (step, i, j, '\u2196', f"MATCH '{X[i-1]}'  => LCS prefix = \"{X[i-1] + lcs_str}\"")
            )
            lcs_str = X[i - 1] + lcs_str
            i -= 1
            j -= 1
        elif b[i][j] == 'U':
            traceback_steps.append(
                (step, i, j, '\u2191', "move UP   (i--)")
            )
            i -= 1
        else:
            traceback_steps.append(
                (step, i, j, '\u2190', "move LEFT (j--)")
            )
            j -= 1

    return c, b, row_traces, traceback_steps, lcs_str


def add_lcs_table(doc, data, m, n, X, Y, label, is_direction=False):
    """Add c[][] or b[][] table."""
    add_styled_para(doc, label, bold=True, size=11)

    tbl = doc.add_table(rows=m + 2, cols=n + 2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    # Top-left corner
    cell = tbl.cell(0, 0)
    cell.text = "X\\Y"
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
    set_cell_shading(cell, "D9E2F3")

    # Column header: "0" then Y chars
    cell = tbl.cell(0, 1)
    cell.text = "0"
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
    set_cell_shading(cell, "D9E2F3")

    for j in range(n):
        cell = tbl.cell(0, j + 2)
        cell.text = Y[j]
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

    # Row header: "0" then X chars
    cell = tbl.cell(1, 0)
    cell.text = "0"
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
    set_cell_shading(cell, "D9E2F3")

    for i in range(m):
        cell = tbl.cell(i + 2, 0)
        cell.text = X[i]
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

    # Data
    dir_map = {'D': '\u2196', 'U': '\u2191', 'L': '\u2190', '': '-'}

    for i in range(m + 1):
        for j in range(n + 1):
            cell = tbl.cell(i + 1, j + 1)
            if is_direction:
                if i == 0 or j == 0:
                    cell.text = "-"
                else:
                    cell.text = dir_map.get(data[i][j], '-')
            else:
                cell.text = str(data[i][j])

            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.size = Pt(9)
                    r.font.name = 'Times New Roman'
                    if is_direction and data[i][j] == 'D' and i > 0 and j > 0:
                        r.bold = True
                        r.font.color.rgb = RGBColor(0, 100, 0)

    doc.add_paragraph()


def add_test_case(doc, case_num, label, X, Y):
    """Add a complete LCS test case."""
    m = len(X)
    n = len(Y)

    heading = doc.add_heading(f'Test Case {case_num}: {label}', level=2)
    fix_heading(heading)
    for run in heading.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    # Input
    add_styled_para(doc, "Input:", bold=True, size=11)
    add_styled_para(doc, f'X = "{X}"  (length {m})', size=11, font='Consolas')
    add_styled_para(doc, f'Y = "{Y}"  (length {n})', size=11, font='Consolas')

    # Solve
    c, b, row_traces, traceback_steps, lcs_str = solve_lcs(X, Y)

    # DP Fill Trace
    add_styled_para(doc, "DP Fill Trace (row by row):", bold=True, size=11)
    add_styled_para(doc, "Base case: c[i][0] = c[0][j] = 0 for all i, j.", size=10, italic=True)

    for (i, char_x, cell_traces) in row_traces:
        add_styled_para(doc, f"Row i={i} (X[{i-1}]='{char_x}')", bold=True, size=10)

        for (j, char_y, is_match, explanation, val, direction) in cell_traces:
            add_bullet(doc,
                f"Cell c[{i}][{j}] (X[{i-1}]='{char_x}', Y[{j-1}]='{char_y}')",
                size=10
            )
            add_sub_bullet(doc, explanation, size=9)
            add_sub_bullet(doc, f"Result: val={val}, dir={direction}", size=9)

    # Final tables
    add_styled_para(doc, "Final Tables:", bold=True, size=11)

    add_lcs_table(doc, c, m, n, X, Y,
                  "c[][] (LCS lengths):", is_direction=False)
    add_lcs_table(doc, b, m, n, X, Y,
                  "b[][] (direction table: \u2196=match, \u2191=up, \u2190=left):", is_direction=True)

    # Traceback
    add_styled_para(doc, "Traceback:", bold=True, size=11)
    add_styled_para(doc, f"Traceback (starting from b[{m}][{n}]):", size=10, italic=True)

    for (step, ti, tj, direction, desc) in traceback_steps:
        add_styled_para(doc,
            f"  Step {step}:  b[{ti}][{tj}]={direction}  {desc}",
            size=9, font='Consolas'
        )

    add_styled_para(doc, "  Reached boundary -> traceback complete.", size=9, font='Consolas')

    # Output
    add_styled_para(doc, "Output:", bold=True, size=11)
    add_styled_para(doc, f"LCS length : {c[m][n]}", size=11)
    add_styled_para(doc, f'LCS string : "{lcs_str}"', size=11, font='Consolas')

    doc.add_page_break()


def create_document():
    doc = Document()

    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    for i in range(4):
        hs = doc.styles[f'Heading {i}'] if i > 0 else doc.styles['Title']
        hs.paragraph_format.space_after = Pt(0)

    # ===== TITLE =====
    title = doc.add_heading('Experiment 15', level=0)
    fix_heading(title)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(22)
        run.font.color.rgb = RGBColor(0, 0, 0)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('Longest Common Subsequence (LCS) using Dynamic Programming')
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
        'To find the longest common subsequence (LCS) of two given strings using the dynamic '
        'programming approach, determining both the length and the actual subsequence.'
    )

    # ===== PROBLEM STATEMENT =====
    h = doc.add_heading('Problem Statement:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_paragraph(
        'Given two strings X of length m and Y of length n, find the longest subsequence that '
        'is common to both strings. A subsequence is a sequence that appears in the same relative '
        'order but not necessarily contiguously. The goal is to compute the length of the LCS and '
        'reconstruct the actual subsequence using a DP table and direction pointers.'
    )

    # ===== THEORY (EXPANDED) =====
    h = doc.add_heading('Theory:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    # Introduction
    p = doc.add_paragraph()
    run = p.add_run(
        'The Longest Common Subsequence (LCS) problem is a fundamental problem in computer science '
        'with applications in text comparison, bioinformatics, version control systems, and data '
        'compression. A subsequence differs from a substring in that the characters need not be '
        'contiguous — they must only appear in the same relative order. For example, "ACE" is a '
        'subsequence of "ABCDE" but "AEC" is not. The LCS problem seeks the longest such subsequence '
        'common to two given sequences.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Optimal substructure
    p = doc.add_paragraph()
    run = p.add_run('Optimal Substructure Property:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'The LCS problem exhibits optimal substructure. Let X = x₁x₂…xₘ and Y = y₁y₂…yₙ. '
        'If xₘ = yₙ, then the LCS of X and Y includes this character, and the remaining LCS is the '
        'LCS of X[1..m-1] and Y[1..n-1]. If xₘ ≠ yₙ, then the LCS is the longer of the LCS of '
        'X[1..m-1] with Y, or X with Y[1..n-1]. This recursive structure, combined with overlapping '
        'subproblems (many subproblems are shared), makes it ideal for dynamic programming.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Recurrence
    p = doc.add_paragraph()
    run = p.add_run('Recurrence Relation:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'Let c[i][j] denote the length of the LCS of X[1..i] and Y[1..j]. The recurrence is:'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        'c[i][j] = c[i-1][j-1] + 1              if X[i] = Y[j]\n'
        'c[i][j] = max(c[i-1][j], c[i][j-1])     if X[i] ≠ Y[j]'
    )
    run.bold = True; run.font.size = Pt(11); run.font.name = 'Consolas'

    p = doc.add_paragraph()
    run = p.add_run(
        'Base case: c[i][0] = 0 and c[0][j] = 0 for all i, j (an empty string has no common '
        'subsequence with anything). Along with the cost table c[][], we maintain a direction '
        'table b[][] where b[i][j] records whether the entry came from a diagonal match (\u2196), '
        'an upward move (\u2191), or a leftward move (\u2190). This table enables reconstruction '
        'of the actual LCS string via backtracking.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # How it works
    p = doc.add_paragraph()
    run = p.add_run('How the Algorithm Works:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'The algorithm fills an (m+1) × (n+1) table c[][] row by row. For each cell c[i][j], '
        'it checks whether X[i] equals Y[j]. If they match, the value is c[i-1][j-1] + 1 and '
        'the direction is diagonal (\u2196). If they don\'t match, the value is the maximum of '
        'c[i-1][j] (up) and c[i][j-1] (left), with the direction set accordingly. After filling '
        'the entire table, c[m][n] contains the LCS length. The LCS string is recovered by '
        'tracing back from b[m][n]: at each diagonal arrow, the corresponding character is added '
        'to the LCS; at up/left arrows, we simply move in that direction.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Complexity
    p = doc.add_paragraph()
    run = p.add_run('Time and Space Complexity:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    data = [
        ("Aspect", "Complexity"),
        ("Time Complexity", "O(m × n)"),
        ("Space Complexity", "O(m × n) for c[][] and b[][]"),
        ("Traceback", "O(m + n)")
    ]
    for idx, (c1, c2) in enumerate(data):
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

    # Advantages
    p = doc.add_paragraph()
    run = p.add_run('Advantages:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for adv in [
        'Guarantees the optimal (longest) common subsequence.',
        'Polynomial O(m×n) time complexity, far better than exponential brute force.',
        'The direction table b[][] allows easy reconstruction of the actual LCS.',
        'Space can be optimized to O(min(m,n)) if only the length is needed.',
        'Generalizable to multiple sequences (k-way LCS).'
    ]:
        pp = doc.add_paragraph(adv, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # Limitations
    p = doc.add_paragraph()
    run = p.add_run('Limitations:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for lim in [
        'O(m×n) space can be large for very long strings.',
        'Multiple LCS of the same length may exist; the algorithm finds only one.',
        'For k sequences, the problem becomes NP-hard in general.',
        'Not suitable for real-time applications with very large inputs.'
    ]:
        pp = doc.add_paragraph(lim, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # Applications
    p = doc.add_paragraph()
    run = p.add_run('Applications:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for app in [
        'diff utilities in version control systems (Git, SVN) for file comparison.',
        'DNA/protein sequence alignment in bioinformatics.',
        'Spell checking and autocorrect algorithms.',
        'Data compression and file synchronization.',
        'Plagiarism detection in text documents.'
    ]:
        pp = doc.add_paragraph(app, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # ===== ALGORITHM =====
    h = doc.add_heading('Algorithm:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    for step in [
        'Initialize c[i][0] = 0 for all i, and c[0][j] = 0 for all j.',
        'For i = 1 to m:',
        '    For j = 1 to n:',
        '        If X[i] = Y[j]: c[i][j] = c[i-1][j-1] + 1, b[i][j] = \u2196 (diagonal)',
        '        Else if c[i-1][j] >= c[i][j-1]: c[i][j] = c[i-1][j], b[i][j] = \u2191 (up)',
        '        Else: c[i][j] = c[i][j-1], b[i][j] = \u2190 (left)',
        'c[m][n] is the LCS length. Trace back through b[][] to reconstruct the LCS string.'
    ]:
        pp = doc.add_paragraph(step, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    add_styled_para(doc, "Pseudocode:", bold=True, size=12)
    pseudocode = """LCS-DP(X, Y, m, n):
    for i \u2190 0 to m do c[i][0] \u2190 0
    for j \u2190 0 to n do c[0][j] \u2190 0
    for i \u2190 1 to m do
        for j \u2190 1 to n do
            if X[i] = Y[j] then
                c[i][j] \u2190 c[i-1][j-1] + 1
                b[i][j] \u2190 \u2196
            else if c[i-1][j] \u2265 c[i][j-1] then
                c[i][j] \u2190 c[i-1][j]
                b[i][j] \u2190 \u2191
            else
                c[i][j] \u2190 c[i][j-1]
                b[i][j] \u2190 \u2190
    return c, b"""
    p = doc.add_paragraph()
    run = p.add_run(pseudocode)
    run.font.size = Pt(10); run.font.name = 'Consolas'
    doc.add_paragraph()

    # ===== INPUT =====
    h = doc.add_heading('Input:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph('Using 4 predefined test cases including classic and edge cases.')
    doc.add_page_break()

    # ===== TEST CASES (ALL NEW VALUES) =====
    h = doc.add_heading('Test Cases:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    # Test Case 1: Classic Case
    add_test_case(doc, 1, "Classic Case", "ACADB", "CBDA")

    # Test Case 2: Single Character Match
    add_test_case(doc, 2, "Single Character Match", "XYZ", "XZ")

    # Test Case 3: Identical Strings
    add_test_case(doc, 3, "Identical Strings — LCS = full string", "WORLD", "WORLD")

    # Test Case 4: No Common Subsequence
    add_test_case(doc, 4, "No Common Subsequence", "MNO", "PQR")

    # ===== RESULT =====
    h = doc.add_heading('Result:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph(
        'All 4 predefined test cases were successfully processed, correctly identifying the longest '
        'common subsequence strings and their lengths via dynamic programming.'
    )

    # ===== CONCLUSION =====
    h = doc.add_heading('Conclusion:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph(
        'The Longest Common Subsequence algorithm, implemented using bottom-up dynamic programming, '
        'successfully determined the LCS for all four test cases. The DP table c[][] was filled '
        'row by row, comparing characters from both strings and recording optimal substructure '
        'decisions in the direction table b[][]. The traceback phase reconstructed the actual LCS '
        'string by following the direction pointers from b[m][n] back to the boundary. The test '
        'cases covered diverse scenarios — a classic multi-character LCS, a single-character match, '
        'identical strings (where LCS equals the full string), and completely disjoint strings '
        '(where LCS is empty) — confirming the correctness and robustness of the O(m\u00d7n) '
        'implementation.'
    )

    # Save
    output_path = r"c:\C++\ADA\lcs\LCS_Theory.docx"
    try:
        doc.save(output_path)
        print(f"Document saved to: {output_path}")
    except PermissionError:
        output_path = r"c:\C++\ADA\lcs\LCS_Theory_v2.docx"
        doc.save(output_path)
        print(f"Original locked. Saved to: {output_path}")


if __name__ == "__main__":
    create_document()
