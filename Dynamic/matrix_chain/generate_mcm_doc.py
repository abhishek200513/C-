"""
Generate MCM Theory Word Document
with expanded theory and new test cases.
Same formatting style as Floyd & Multistage docs.
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

INF = float('inf')


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


def build_paren_string(s, i, j):
    if i == j:
        return f"A{i}"
    return f"({build_paren_string(s, i, s[i][j])} x {build_paren_string(s, s[i][j]+1, j)})"


def solve_mcm(p, n):
    """
    Solve MCM and return m[][], s[][], and step-by-step trace.
    n = number of matrices, p has n+1 elements.
    """
    m = [[0]*(n+1) for _ in range(n+1)]
    s = [[0]*(n+1) for _ in range(n+1)]
    for i in range(1, n+1):
        m[i][i] = 0

    steps = []  # list of (chain_length, entries)
    # entries: list of (i, j, dim_str, k_evals, best_cost, best_k)
    # k_evals: list of (k, m_ik, m_k1j, pi_1, pk, pj, cost, is_new_min)

    for l in range(2, n+1):
        chain_entries = []
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = INF
            dim_str = f"{p[i-1]}x{p[j]}"
            k_evals = []

            for k in range(i, j):
                cost = m[i][k] + m[k+1][j] + p[i-1] * p[k] * p[j]
                is_new_min = cost < m[i][j]
                k_evals.append((k, m[i][k], m[k+1][j], p[i-1], p[k], p[j], cost, is_new_min))
                if is_new_min:
                    m[i][j] = cost
                    s[i][j] = k

            chain_entries.append((i, j, dim_str, k_evals, m[i][j], s[i][j]))
        steps.append((l, chain_entries))

    return m, s, steps


def add_dp_table(doc, table_data, n, label, is_split=False):
    """Add m[][] or s[][] table to the document."""
    add_styled_para(doc, label, bold=True, size=11)

    tbl = doc.add_table(rows=n+1, cols=n+1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    # Header: label column
    cell = tbl.cell(0, 0)
    cell.text = "m" if not is_split else "s"
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
    set_cell_shading(cell, "D9E2F3")

    # Column headers
    for j in range(1, n+1):
        cell = tbl.cell(0, j)
        cell.text = f"j={j}"
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

    # Row headers and data
    for i in range(1, n+1):
        cell = tbl.cell(i, 0)
        cell.text = f"i={i}"
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

        for j in range(1, n+1):
            cell = tbl.cell(i, j)
            if i > j:
                cell.text = "--"
            elif i == j:
                cell.text = "0" if not is_split else "--"
            else:
                cell.text = str(table_data[i][j])
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.size = Pt(9); r.font.name = 'Times New Roman'

    doc.add_paragraph()


def add_test_case(doc, case_num, label, p):
    """Add a complete MCM test case to the document."""
    n = len(p) - 1  # number of matrices

    # Heading
    heading = doc.add_heading(f'Test Case {case_num}: {label}', level=2)
    fix_heading(heading)
    for run in heading.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    # Input
    add_styled_para(doc, "Input:", bold=True, size=11)
    add_styled_para(doc, f"n = {n} matrices", size=11)

    p_str = "{ " + ", ".join(str(x) for x in p) + " }"
    add_styled_para(doc, f"p[] = {p_str}", size=11, font='Consolas')

    dims_str = "  ".join(f"A{i+1}({p[i]}x{p[i+1]})" for i in range(n))
    add_styled_para(doc, f"Dims: {dims_str}", size=10, font='Consolas')

    # Solve
    m, s, steps = solve_mcm(p, n)

    # DP Solution
    add_styled_para(doc, "DP Solution (Bottom-Up, filling by chain length l):", bold=True, size=11)
    add_styled_para(doc, "Base case: m[i][i] = 0 for all i  (single matrix, zero cost).", size=10, italic=True)

    for (l, chain_entries) in steps:
        add_styled_para(doc, f"Chain length l = {l}", bold=True, size=11)

        for (i, j, dim_str, k_evals, best_cost, best_k) in chain_entries:
            # Entry header as bullet
            add_bullet(doc, f"m[{i}][{j}] (A{i}..A{j}) dim={dim_str}", size=10)

            # Each k evaluation as sub-bullet (using indented paragraph)
            for (k, m_ik, m_k1j, pi_1, pk, pj, cost, is_new_min) in k_evals:
                text = f"    k={k}: {m_ik} + {m_k1j} + {pi_1} × {pk} × {pj} = {cost}"
                if is_new_min:
                    text += "  ← minimum"
                p_para = doc.add_paragraph()
                run = p_para.add_run(text)
                run.font.size = Pt(9)
                run.font.name = 'Consolas'

            # Result
            p_para = doc.add_paragraph()
            run = p_para.add_run(f"    Result: m[{i}][{j}] = {best_cost}, s[{i}][{j}] = {best_k}")
            run.bold = True
            run.font.size = Pt(9)
            run.font.name = 'Times New Roman'

    # Final Tables
    add_styled_para(doc, "Final Tables:", bold=True, size=11)
    add_dp_table(doc, m, n, "m[][] (min scalar multiplications):", is_split=False)
    add_dp_table(doc, s, n, "s[][] (optimal split positions):", is_split=True)

    # Output
    add_styled_para(doc, "Output:", bold=True, size=11)
    paren = build_paren_string(s, 1, n)
    add_styled_para(doc, f"Min scalar multiplications : {m[1][n]}", size=11)
    add_styled_para(doc, f"Optimal parenthesization   : {paren}", size=11, font='Consolas')

    doc.add_page_break()


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
    title = doc.add_heading('Experiment 14', level=0)
    fix_heading(title)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(22)
        run.font.color.rgb = RGBColor(0, 0, 0)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('Matrix Chain Multiplication (MCM) using Dynamic Programming')
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'

    doc.add_paragraph()

    # ===== AIM =====
    h = doc.add_heading('Aim:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_paragraph(
        'To determine the optimal parenthesization of a chain of matrices that minimizes the '
        'total number of scalar multiplications using dynamic programming.'
    )

    # ===== PROBLEM STATEMENT =====
    h = doc.add_heading('Problem Statement:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_paragraph(
        'Given a sequence of n matrices A₁, A₂, …, Aₙ where matrix Aᵢ has dimensions p[i-1] × p[i], '
        'determine the order of multiplication (parenthesization) that minimizes the total number of '
        'scalar multiplications required to compute the product A₁ × A₂ × … × Aₙ.'
    )

    # ===== THEORY (EXPANDED) =====
    h = doc.add_heading('Theory:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    # Paragraph 1 — Introduction
    p = doc.add_paragraph()
    run = p.add_run(
        'Matrix Chain Multiplication is a classic optimization problem in computer science that '
        'demonstrates the power of dynamic programming. Matrix multiplication is associative — '
        'meaning (A × B) × C = A × (B × C) — but the order in which matrices are multiplied '
        'dramatically affects the computational cost. The MCM problem seeks to find the '
        'parenthesization that minimizes the total number of scalar multiplications.'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Paragraph 2 — Why order matters
    p = doc.add_paragraph()
    run = p.add_run('Why Multiplication Order Matters:')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'Consider three matrices: A₁ (10×30), A₂ (30×5), A₃ (5×60). Computing (A₁×A₂)×A₃ requires '
        '10×30×5 + 10×5×60 = 1500 + 3000 = 4500 multiplications. However, computing A₁×(A₂×A₃) '
        'requires 30×5×60 + 10×30×60 = 9000 + 18000 = 27000 multiplications — six times more! '
        'This dramatic difference motivates the need for an efficient algorithm to find the optimal order.'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Paragraph 3 — Why not brute force
    p = doc.add_paragraph()
    run = p.add_run('Why Not Brute Force?')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'The number of possible parenthesizations for n matrices is given by the Catalan number '
        'C(n-1), which grows exponentially: C(n) = (2n)! / ((n+1)! × n!). For example, 10 matrices '
        'have 4862 possible parenthesizations, and 20 matrices have over 1.7 billion. Exhaustive '
        'enumeration has Ω(4ⁿ/n^(3/2)) complexity, making it infeasible for even moderate n. '
        'Dynamic programming reduces this to O(n³) by exploiting optimal substructure and '
        'overlapping subproblems.'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Paragraph 4 — DP formulation
    p = doc.add_paragraph()
    run = p.add_run('Dynamic Programming Formulation:')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'Let m[i][j] represent the minimum number of scalar multiplications needed to compute the '
        'product Aᵢ × Aᵢ₊₁ × … × Aⱼ. The key observation is that to compute Aᵢ..Aⱼ, we must '
        'split the chain at some position k (i ≤ k < j), compute Aᵢ..Aₖ and Aₖ₊₁..Aⱼ separately, '
        'then multiply the two resulting matrices. The cost of this split is m[i][k] + m[k+1][j] + '
        'p[i-1]×p[k]×p[j]. The recurrence is:'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Formula
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('m[i][j] = min { m[i][k] + m[k+1][j] + p[i-1]·p[k]·p[j] }  for i ≤ k < j')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Consolas'

    p = doc.add_paragraph()
    run = p.add_run(
        'Base case: m[i][i] = 0 (a single matrix requires no multiplication). We also maintain a '
        'split table s[i][j] that records the value of k that achieves the minimum for m[i][j]. '
        'This table is used to reconstruct the optimal parenthesization after the DP computation.'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Paragraph 5 — Bottom-up approach
    p = doc.add_paragraph()
    run = p.add_run('Bottom-Up Computation:')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'The table m[i][j] is filled in order of increasing chain length l = j - i + 1. For l = 1, '
        'all diagonal entries m[i][i] = 0. For l = 2, we compute costs for all pairs of adjacent '
        'matrices. For l = 3, triplets are considered, and so on until l = n covers the entire chain. '
        'At each step, we try all possible split points k and record the minimum cost and the '
        'corresponding split position. This ensures that when computing m[i][j], all smaller '
        'subproblems m[i][k] and m[k+1][j] have already been solved.'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Complexity
    p = doc.add_paragraph()
    run = p.add_run('Time and Space Complexity:')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    complexity_data = [
        ("Aspect", "Complexity"),
        ("Time Complexity", "O(n³)"),
        ("Space Complexity", "O(n²) for m[][] and s[][]"),
        ("Path Reconstruction", "O(n) using s[][] table")
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

    # Advantages
    p = doc.add_paragraph()
    run = p.add_run('Advantages:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for adv in [
        'Reduces exponential brute-force complexity to polynomial O(n³).',
        'Guarantees the globally optimal parenthesization.',
        'The split table s[][] enables efficient reconstruction of the solution.',
        'Applicable to any associative binary operation, not just matrix multiplication.',
        'Foundation for understanding more complex DP problems (e.g., optimal BST, polygon triangulation).'
    ]:
        pp = doc.add_paragraph(adv, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # Limitations
    p = doc.add_paragraph()
    run = p.add_run('Limitations:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for lim in [
        'O(n³) time is still slow for very large n (thousands of matrices).',
        'Requires O(n²) space for the DP tables.',
        'Hu & Shing\'s algorithm can solve MCM in O(n log n) for special cases.',
        'Only optimizes multiplication count, not cache performance or parallelism.'
    ]:
        pp = doc.add_paragraph(lim, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # Applications
    p = doc.add_paragraph()
    run = p.add_run('Applications:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for app in [
        'Optimizing matrix computations in scientific computing and machine learning.',
        'Query optimization in relational database systems (join ordering).',
        'Efficient evaluation of chain products in computer graphics transformations.',
        'Polygon triangulation and optimal binary search tree construction.',
        'Compiler optimization for expression evaluation ordering.'
    ]:
        pp = doc.add_paragraph(app, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # ===== ALGORITHM =====
    h = doc.add_heading('Algorithm:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    for step in [
        'Initialize m[i][i] = 0 for all i = 1 to n (base case).',
        'For chain length l = 2 to n:',
        '    For i = 1 to n - l + 1, set j = i + l - 1:',
        '        For each split point k = i to j - 1:',
        '            Compute cost = m[i][k] + m[k+1][j] + p[i-1] × p[k] × p[j].',
        '            If cost < m[i][j], update m[i][j] = cost and s[i][j] = k.',
        'The answer is m[1][n] with parenthesization reconstructed from s[][].'
    ]:
        pp = doc.add_paragraph(step, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # Pseudocode
    add_styled_para(doc, "Pseudocode:", bold=True, size=12)
    pseudocode = """MCM-DP(p[], n):
    for i ← 1 to n do m[i][i] ← 0
    for l ← 2 to n do
        for i ← 1 to n-l+1 do
            j ← i + l - 1
            m[i][j] ← ∞
            for k ← i to j-1 do
                q ← m[i][k] + m[k+1][j] + p[i-1]·p[k]·p[j]
                if q < m[i][j] then
                    m[i][j] ← q
                    s[i][j] ← k
    return m, s"""
    p = doc.add_paragraph()
    run = p.add_run(pseudocode)
    run.font.size = Pt(10); run.font.name = 'Consolas'
    doc.add_paragraph()

    # ===== INPUT =====
    h = doc.add_heading('Input:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph('Using 5 predefined test cases.')
    doc.add_page_break()

    # ===== TEST CASES (ALL NEW VALUES) =====
    h = doc.add_heading('Test Cases:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    # Test Case 1: Standard — 6 Matrices
    add_test_case(doc, 1, "Standard — 6 Matrices",
                  [20, 25, 10, 15, 5, 30, 20])

    # Test Case 2: Small 3-Matrix — Hand-Verifiable
    add_test_case(doc, 2, "Small 3-Matrix — Hand-Verifiable",
                  [5, 20, 10, 40])

    # Test Case 3: Greedy Trap — 3 Matrices
    add_test_case(doc, 3, "Greedy Trap — 3 Matrices",
                  [2, 50, 2, 50])

    # Test Case 4: Larger — 5 Matrices
    add_test_case(doc, 4, "Larger — 5 Matrices",
                  [15, 10, 20, 25, 15, 30])

    # Test Case 5: 4-Matrix Chain
    add_test_case(doc, 5, "4-Matrix Chain",
                  [8, 15, 5, 20, 10])

    # ===== RESULT =====
    h = doc.add_heading('Result:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph(
        'All 5 predefined test cases were executed successfully, accurately finding the optimal '
        'parenthesization and minimum scalar multiplication cost for the matrix chains.'
    )

    # ===== CONCLUSION =====
    h = doc.add_heading('Conclusion:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph(
        'The Matrix Chain Multiplication algorithm, implemented using the bottom-up dynamic '
        'programming approach, successfully determined the optimal parenthesization to minimize '
        'scalar multiplications across all five test cases. By systematically filling the cost '
        'table m[][] for increasing chain lengths and evaluating all possible split points, the '
        'algorithm guaranteed globally optimal solutions in O(n³) time. The split table s[][] '
        'enabled efficient reconstruction of the parenthesization. The test cases demonstrated '
        'the algorithm\'s ability to handle standard configurations, small hand-verifiable '
        'instances, greedy traps where naive approaches fail, and larger chains — confirming '
        'the correctness and robustness of the implementation.'
    )

    # Save
    output_path = r"c:\C++\ADA\matrix_chain\MCM_Theory.docx"
    try:
        doc.save(output_path)
        print(f"Document saved to: {output_path}")
    except PermissionError:
        output_path = r"c:\C++\ADA\matrix_chain\MCM_Theory_v2.docx"
        doc.save(output_path)
        print(f"Original locked. Saved to: {output_path}")


if __name__ == "__main__":
    create_document()
