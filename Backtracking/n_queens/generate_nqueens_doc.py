"""
Generate N-Queens Theory Word Document
with detailed theory, backtracking illustration, constraints,
chessboard-style matrix visualization, and test cases.
Same formatting style as LCS, MCM, and Floyd docs.
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml


# =====================================================================
#  Formatting helpers (same as other docs)
# =====================================================================

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
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Pt(36)
    run = p.add_run("\u25cb " + text)
    run.font.size = Pt(size)
    run.font.name = font
    return p


# =====================================================================
#  N-Queens Solver with backtracking trace
# =====================================================================

QUEEN = "\u265B"       # ♛ Black chess queen
CROSS = "\u00d7"       # × attack marker
EMPTY = ""

LIGHT_SQUARE = "FFF8DC"   # Light cream/cornsilk
DARK_SQUARE  = "D2B48C"   # Tan
QUEEN_BG     = "90EE90"   # Light green — queen placed
ATTACK_BG    = "FFB6C1"   # Light pink — under attack


def is_safe(board, row, col, n):
    """Check if placing queen at (row, col) is safe."""
    for i in range(row):
        if board[i] == col:
            return False
        if abs(i - row) == abs(board[i] - col):
            return False
    return True


def get_attack_cells(board, row, n):
    """Return set of cells attacked by queens in rows 0..row-1."""
    attacked = set()
    for i in range(row):
        c = board[i]
        # Full row, column, and diagonals from queen at (i, c)
        for r in range(n):
            attacked.add((r, c))                   # column
        for r in range(n):
            attacked.add((i, r))                   # row
        for d in range(-n, n):
            if 0 <= i + d < n and 0 <= c + d < n:
                attacked.add((i + d, c + d))       # main diagonal
            if 0 <= i + d < n and 0 <= c - d < n:
                attacked.add((i + d, c - d))       # anti-diagonal
    return attacked


def solve_all(n, max_solutions=None):
    """Find all (or up to max_solutions) solutions."""
    solutions = []
    board = [-1] * n

    def backtrack(row):
        if max_solutions and len(solutions) >= max_solutions:
            return
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col, n):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1

    backtrack(0)
    return solutions


def solve_with_trace(n):
    """
    Solve N-Queens for the FIRST solution only, recording a
    step-by-step backtracking trace.
    Returns: (solution_board, trace_steps)
    Each trace step = (action, row, col, board_snapshot, explanation)
    action = 'try' | 'place' | 'fail' | 'backtrack'
    """
    board = [-1] * n
    trace = []
    found = [False]

    def backtrack(row):
        if found[0]:
            return
        if row == n:
            found[0] = True
            trace.append(('done', -1, -1, board[:], 'All queens placed successfully!'))
            return

        for col in range(n):
            if found[0]:
                return

            # Try
            if not is_safe(board, row, col, n):
                # Conflict — show why
                conflict_reason = ""
                for i in range(row):
                    if board[i] == col:
                        conflict_reason = f"Column conflict with Queen at Row {i+1}"
                        break
                    if abs(i - row) == abs(board[i] - col):
                        conflict_reason = f"Diagonal conflict with Queen at Row {i+1}, Col {board[i]+1}"
                        break
                trace.append((
                    'fail', row, col, board[:],
                    f"Try Q at ({row+1},{col+1}): UNSAFE — {conflict_reason}"
                ))
            else:
                board[row] = col
                trace.append((
                    'place', row, col, board[:],
                    f"Place Q at ({row+1},{col+1}): Safe — no conflicts"
                ))
                backtrack(row + 1)

                if not found[0]:
                    trace.append((
                        'backtrack', row, col, board[:],
                        f"Backtrack: Remove Q from ({row+1},{col+1})"
                    ))
                    board[row] = -1

    backtrack(0)
    return board if found[0] else None, trace


# =====================================================================
#  Board rendering in Word
# =====================================================================

def add_chessboard(doc, board, n, label, show_attacks=False):
    """Add a visually styled chessboard table with queens."""
    add_styled_para(doc, label, bold=True, size=11)

    # n+1 rows/cols (extra for labels)
    tbl = doc.add_table(rows=n + 1, cols=n + 1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    # Attacked cells
    attacked = set()
    if show_attacks:
        for i in range(n):
            if board[i] != -1:
                attacked = attacked.union(get_attack_cells(board, n, n))
        # Recompute properly
        attacked = set()
        for i in range(n):
            if board[i] == -1:
                continue
            c = board[i]
            for r in range(n):
                if r != i:
                    attacked.add((r, c))
            for r in range(n):
                if r != c:
                    attacked.add((i, r))
            for d in range(1, n):
                if 0 <= i + d < n and 0 <= c + d < n:
                    attacked.add((i + d, c + d))
                if 0 <= i - d < n and 0 <= c - d < n:
                    attacked.add((i - d, c - d))
                if 0 <= i + d < n and 0 <= c - d < n:
                    attacked.add((i + d, c - d))
                if 0 <= i - d < n and 0 <= c + d < n:
                    attacked.add((i - d, c + d))

    # Top-left corner
    cell = tbl.cell(0, 0)
    cell.text = ""
    set_cell_shading(cell, "D9E2F3")

    # Column headers
    for j in range(n):
        cell = tbl.cell(0, j + 1)
        cell.text = str(j + 1)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(10); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

    # Rows
    for i in range(n):
        # Row header
        cell = tbl.cell(i + 1, 0)
        cell.text = str(i + 1)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(10); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

        # Board cells
        for j in range(n):
            cell = tbl.cell(i + 1, j + 1)

            if board[i] == j:
                # Queen cell
                cell.text = QUEEN
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.size = Pt(14); r.font.name = 'Segoe UI Symbol'
                        r.bold = True
                set_cell_shading(cell, QUEEN_BG)
            elif show_attacks and (i, j) in attacked:
                cell.text = CROSS
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.size = Pt(10); r.font.name = 'Times New Roman'
                        r.font.color.rgb = RGBColor(200, 50, 50)
                set_cell_shading(cell, ATTACK_BG)
            else:
                cell.text = ""
                # Checkerboard pattern
                if (i + j) % 2 == 0:
                    set_cell_shading(cell, LIGHT_SQUARE)
                else:
                    set_cell_shading(cell, DARK_SQUARE)

    doc.add_paragraph()


def add_backtracking_snapshot(doc, board_snap, n, row, col, action, step_num, explanation):
    """Add a small board snapshot showing the current backtracking state."""
    add_styled_para(doc,
        f"Step {step_num}: {explanation}",
        bold=(action in ('place', 'done')),
        size=10,
        font='Times New Roman'
    )

    # Build a mini board
    tbl = doc.add_table(rows=n + 1, cols=n + 1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    # Corner
    cell = tbl.cell(0, 0)
    cell.text = ""
    set_cell_shading(cell, "D9E2F3")

    # Column headers
    for j in range(n):
        cell = tbl.cell(0, j + 1)
        cell.text = str(j + 1)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(8); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

    for i in range(n):
        # Row header
        cell = tbl.cell(i + 1, 0)
        cell.text = str(i + 1)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(8); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

        for j in range(n):
            cell = tbl.cell(i + 1, j + 1)

            if board_snap[i] == j:
                cell.text = QUEEN
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.size = Pt(12); r.font.name = 'Segoe UI Symbol'
                        r.bold = True
                set_cell_shading(cell, QUEEN_BG)
            elif action == 'fail' and i == row and j == col:
                # Mark the attempted cell in red
                cell.text = CROSS
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.size = Pt(10); r.font.name = 'Times New Roman'
                        r.font.color.rgb = RGBColor(200, 50, 50)
                set_cell_shading(cell, ATTACK_BG)
            else:
                cell.text = ""
                if (i + j) % 2 == 0:
                    set_cell_shading(cell, LIGHT_SQUARE)
                else:
                    set_cell_shading(cell, DARK_SQUARE)

    doc.add_paragraph()


# =====================================================================
#  Test case section
# =====================================================================

def add_test_case(doc, case_num, n):
    """Add a complete test case for N-Queens."""
    heading = doc.add_heading(f'Test Case {case_num}: N = {n}', level=2)
    fix_heading(heading)
    for run in heading.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    # Input
    add_styled_para(doc, "Input:", bold=True, size=11)
    add_styled_para(doc, f"N = {n}  (Place {n} queens on a {n}\u00d7{n} chessboard)", size=11)

    # Handle special cases
    if n == 2 or n == 3:
        add_styled_para(doc, "Output:", bold=True, size=11)
        add_styled_para(doc,
            f"No solution exists for N = {n}. It is impossible to place {n} "
            f"non-attacking queens on a {n}\u00d7{n} board.",
            size=11, italic=True)
        doc.add_page_break()
        return

    # Solve
    solutions = solve_all(n, max_solutions=100)
    total = len(solutions)

    # Show first 2 solutions with chessboards
    add_styled_para(doc, "Output:", bold=True, size=11)
    add_styled_para(doc, f"Total number of solutions: {total}", size=11)

    show_count = min(total, 2)
    for idx in range(show_count):
        sol = solutions[idx]
        placement_str = ", ".join(f"Row {i+1}\u2192Col {sol[i]+1}" for i in range(n))
        add_chessboard(doc, sol, n,
            f"Solution {idx+1}:  [{placement_str}]",
            show_attacks=False)

    # Show one solution with attack zones highlighted
    if total > 0:
        add_chessboard(doc, solutions[0], n,
            f"Solution 1 — Attack Zones Visualization  (\u00d7 = attacked, {QUEEN} = queen, green = queen cell, pink = attacked):",
            show_attacks=True)

    # Summary table of all solutions (if n is small)
    if n <= 8 and total > 2:
        add_styled_para(doc, f"All {total} Solution Placements:", bold=True, size=11)

        sol_tbl = doc.add_table(rows=min(total, 20) + 1, cols=n + 1)
        sol_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(sol_tbl)

        # Header
        cell = sol_tbl.cell(0, 0)
        cell.text = "#"
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

        for col_idx in range(n):
            cell = sol_tbl.cell(0, col_idx + 1)
            cell.text = f"Q{col_idx + 1} Col"
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.bold = True; r.font.size = Pt(9); r.font.name = 'Times New Roman'
            set_cell_shading(cell, "D9E2F3")

        for s_idx in range(min(total, 20)):
            cell = sol_tbl.cell(s_idx + 1, 0)
            cell.text = str(s_idx + 1)
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.size = Pt(9); r.font.name = 'Times New Roman'

            for col_idx in range(n):
                cell = sol_tbl.cell(s_idx + 1, col_idx + 1)
                cell.text = str(solutions[s_idx][col_idx] + 1)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.size = Pt(9); r.font.name = 'Times New Roman'

        doc.add_paragraph()

    doc.add_page_break()


# =====================================================================
#  Main document
# =====================================================================

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
    title = doc.add_heading('Experiment 17', level=0)
    fix_heading(title)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(22)
        run.font.color.rgb = RGBColor(0, 0, 0)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('N-Queens Problem using Backtracking')
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
        'To solve the N-Queens problem using the backtracking approach — placing N queens on an '
        'N\u00d7N chessboard such that no two queens attack each other — and to demonstrate how the '
        'backtracking phenomenon systematically explores and prunes the solution space.'
    )

    # ===== PROBLEM STATEMENT =====
    h = doc.add_heading('Problem Statement:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_paragraph(
        'Given a positive integer N, place N queens on an N\u00d7N chessboard such that no two queens '
        'threaten each other. Two queens attack each other if they share the same row, the same '
        'column, or the same diagonal. Find all valid configurations (or verify that none exist).'
    )

    # ===== THEORY =====
    h = doc.add_heading('Theory:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    # Introduction
    p = doc.add_paragraph()
    run = p.add_run(
        'The N-Queens problem is one of the most classic problems in computer science and artificial '
        'intelligence. Originally posed in 1848 by chess composer Max Bezzel for the 8-queens case, '
        'the problem asks: "How can N queens be placed on an N\u00d7N chessboard so that no two queens '
        'attack each other?" A queen in chess can attack along its row, column, and both diagonals, '
        'making the placement constraints quite restrictive. The problem beautifully illustrates '
        'constraint satisfaction, recursive search, and the power of the backtracking paradigm.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Constraints
    p = doc.add_paragraph()
    run = p.add_run('Constraints:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'For a valid N-Queens configuration, the following constraints must be satisfied:'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    for constraint in [
        'No two queens can be in the same row — since we place exactly one queen per row, this is automatically ensured.',
        'No two queens can be in the same column — if queen in row i is in column c[i], then c[i] \u2260 c[j] for all i \u2260 j.',
        'No two queens can be on the same main diagonal — |row_i \u2212 row_j| \u2260 |col_i \u2212 col_j| for all pairs.',
        'No two queens can be on the same anti-diagonal — same condition as above covers both diagonals.',
        'Exactly N queens must be placed (one per row) on the N\u00d7N board.'
    ]:
        pp = doc.add_paragraph(constraint, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # Feasibility
    p = doc.add_paragraph()
    run = p.add_run('Feasibility:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'Solutions exist for all N \u2265 1 except N = 2 and N = 3. For N = 1, the trivial solution '
        'is a single queen on a 1\u00d71 board. For N = 2 and N = 3, no valid configuration exists — '
        'any placement of 2 queens on a 2\u00d72 board results in an attack, and similarly for 3 on '
        'a 3\u00d73 board. For N \u2265 4, at least one valid solution always exists.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Backtracking
    p = doc.add_paragraph()
    run = p.add_run('What is Backtracking?')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'Backtracking is a systematic algorithmic technique for solving constraint satisfaction '
        'problems by incrementally building candidates and abandoning ("backtracking from") a '
        'candidate as soon as it is determined that it cannot lead to a valid solution. It is '
        'essentially a depth-first search of the solution space tree with pruning. Instead of '
        'generating all N! permutations (brute force), backtracking prunes entire subtrees that '
        'violate constraints, dramatically reducing the search space.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # How it works
    p = doc.add_paragraph()
    run = p.add_run('How Backtracking Works for N-Queens:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'The algorithm places queens one row at a time, starting from row 1. For each row, it tries '
        'each column from left to right. Before placing a queen, it checks whether the position is '
        '"safe" — i.e., no previously placed queen attacks this cell. If safe, the queen is placed '
        'and the algorithm moves to the next row. If no safe column exists in the current row, the '
        'algorithm backtracks to the previous row, removes the queen there, and tries the next column. '
        'This process continues until all N queens are placed (solution found) or all possibilities '
        'are exhausted.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Step-by-step algorithm
    for step in [
        'Start with an empty board. Set row = 1.',
        'For column = 1 to N in the current row:',
        '    Check if placing a queen at (row, column) is safe (no conflicts).',
        '    If safe: place the queen, move to row + 1, and repeat from step 2.',
        '    If not safe: try the next column.',
        'If no column is safe in this row: BACKTRACK — go to the previous row, remove the queen, and try the next column.',
        'If row > N: a valid solution is found — record it.',
        'Continue until all solutions are found (or just the first one).'
    ]:
        pp = doc.add_paragraph(step, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # ===== EXAMPLE: 4-Queens with Backtracking Trace =====
    p = doc.add_paragraph()
    run = p.add_run('Worked Example — 4-Queens with Backtracking Trace:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'Let us trace the backtracking algorithm for N = 4. We place one queen per row and '
        'try columns 1 through 4 in each row. When a conflict is detected, we backtrack.'
    )
    run.font.size = Pt(12); run.font.name = 'Times New Roman'

    # Run the trace for N=4
    _, trace = solve_with_trace(4)

    # Filter trace to show key steps (not every single fail for brevity but enough to show backtracking)
    # We'll show all steps but limit to ~20 most important ones
    key_steps = []
    for step in trace:
        action = step[0]
        if action in ('place', 'backtrack', 'done'):
            key_steps.append(step)
        elif action == 'fail':
            key_steps.append(step)

    # Limit to first ~25 steps to keep the document manageable
    display_steps = key_steps[:25]

    step_num = 0
    for (action, row, col, board_snap, explanation) in display_steps:
        step_num += 1
        add_backtracking_snapshot(doc, board_snap, 4, row, col, action, step_num, explanation)

        if action == 'done':
            break

    # If trace was truncated
    if len(key_steps) > 25:
        remaining = len(key_steps) - 25
        add_styled_para(doc, f"... ({remaining} more steps until first solution found)", size=10, italic=True)

    # Show the final solution
    first_sol = solve_all(4, max_solutions=1)[0]
    add_styled_para(doc, "First Valid Solution Found:", bold=True, size=12)
    add_chessboard(doc, first_sol, 4,
        f"4-Queens Solution:  [" +
        ", ".join(f"Row {i+1}\u2192Col {first_sol[i]+1}" for i in range(4)) + "]",
        show_attacks=True)

    add_styled_para(doc,
        'The backtracking algorithm explored only a fraction of the 4! = 24 possible permutations. '
        'By pruning invalid branches early (when a conflict is detected), it efficiently navigated '
        'the solution space to find the first valid placement. For 4-Queens, there are exactly 2 '
        'distinct solutions.',
        size=11)

    # Time Complexity
    p = doc.add_paragraph()
    run = p.add_run('Time and Space Complexity:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    complexity_data = [
        ("Aspect", "Complexity"),
        ("Worst-case Time", "O(N!) — but pruning makes it much faster in practice"),
        ("Space Complexity", "O(N) — board array of size N + recursion stack depth N"),
        ("Safety Check", "O(N) per cell (check against all previously placed queens)")
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

    # Known solution counts
    p = doc.add_paragraph()
    run = p.add_run('Known Solution Counts:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'

    count_tbl = doc.add_table(rows=9, cols=2)
    count_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(count_tbl)
    known_counts = [
        ("N", "Solutions"),
        ("1", "1"), ("2", "0"), ("3", "0"), ("4", "2"),
        ("5", "10"), ("6", "4"), ("7", "40"), ("8", "92")
    ]
    for idx, (c1, c2) in enumerate(known_counts):
        for ci, val in enumerate([c1, c2]):
            cell = count_tbl.cell(idx, ci)
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
        'Systematically explores all valid configurations without missing any.',
        'Pruning eliminates large portions of the search space, making it far faster than brute force.',
        'Simple and elegant recursive implementation.',
        'Space-efficient: requires only O(N) storage for the board state.',
        'Can be extended to find all solutions or just the first one.'
    ]:
        pp = doc.add_paragraph(adv, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # Limitations
    p = doc.add_paragraph()
    run = p.add_run('Limitations:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for lim in [
        'Worst-case time complexity is still exponential O(N!).',
        'For very large N (e.g., N > 25), finding all solutions becomes impractical.',
        'Does not use heuristics — more advanced techniques (e.g., min-conflicts) can be faster for large N.',
        'The number of solutions grows super-exponentially, making enumeration infeasible for large N.'
    ]:
        pp = doc.add_paragraph(lim, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # Applications
    p = doc.add_paragraph()
    run = p.add_run('Applications:')
    run.bold = True; run.font.size = Pt(12); run.font.name = 'Times New Roman'
    for app in [
        'VLSI circuit design — placing non-interfering components on a chip.',
        'Scheduling problems — assigning tasks without conflicts.',
        'Constraint satisfaction in artificial intelligence and operations research.',
        'Parallel processing — assigning independent tasks to processors.',
        'Testing and benchmarking backtracking and search algorithms.'
    ]:
        pp = doc.add_paragraph(app, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    # ===== ALGORITHM =====
    h = doc.add_heading('Algorithm:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    for step in [
        'Create an array board[1..N] where board[i] = column of queen in row i.',
        'Call solveNQueens(board, row=1, N).',
        'In solveNQueens(board, row, N):',
        '    If row > N: all queens placed \u2014 record/print the solution.',
        '    For col = 1 to N:',
        '        If isSafe(board, row, col): no conflicts with rows 1..row\u22121',
        '            board[row] = col  (place queen)',
        '            solveNQueens(board, row+1, N)  (recurse for next row)',
        '            board[row] = \u22121  (backtrack \u2014 remove queen)',
        'isSafe checks: same column and both diagonals against all placed queens.'
    ]:
        pp = doc.add_paragraph(step, style='List Bullet')
        for r in pp.runs: r.font.size = Pt(11); r.font.name = 'Times New Roman'

    add_styled_para(doc, "Pseudocode:", bold=True, size=12)
    pseudocode = """N-QUEENS(board[], row, N):
    if row > N then
        print board[]  (solution found)
        return
    for col \u2190 1 to N do
        if IS-SAFE(board, row, col) then
            board[row] \u2190 col
            N-QUEENS(board, row + 1, N)
            board[row] \u2190 -1       \u2190 BACKTRACK

IS-SAFE(board[], row, col):
    for i \u2190 1 to row - 1 do
        if board[i] = col then return false              (same column)
        if |i - row| = |board[i] - col| then return false (same diagonal)
    return true"""
    p = doc.add_paragraph()
    run = p.add_run(pseudocode)
    run.font.size = Pt(10); run.font.name = 'Consolas'
    doc.add_paragraph()

    # ===== INPUT =====
    h = doc.add_heading('Input:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph('Using 4 predefined test cases with different values of N.')
    doc.add_page_break()

    # ===== TEST CASES =====
    h = doc.add_heading('Test Cases:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    add_test_case(doc, 1, 4)    # Classic — 2 solutions
    add_test_case(doc, 2, 5)    # 10 solutions
    add_test_case(doc, 3, 6)    # 4 solutions
    add_test_case(doc, 4, 8)    # Classic 8-queens — 92 solutions

    # ===== RESULT =====
    h = doc.add_heading('Result:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph(
        'All 4 test cases were executed successfully. The backtracking algorithm correctly found '
        'all valid configurations for each value of N, matching the known solution counts '
        '(N=4: 2, N=5: 10, N=6: 4, N=8: 92).'
    )

    # ===== CONCLUSION =====
    h = doc.add_heading('Conclusion:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph(
        'The N-Queens problem was successfully solved using the backtracking approach. The algorithm '
        'placed queens row by row, checking safety constraints (column and diagonal conflicts) before '
        'each placement. When no safe column was available in a row, the algorithm backtracked to the '
        'previous row and explored alternative column placements. The detailed 4-Queens trace '
        'demonstrated how backtracking prunes invalid branches early — exploring only a fraction of '
        'the total search space compared to brute-force enumeration. The chessboard visualizations '
        'with attack zones confirmed that no two queens share a row, column, or diagonal in any '
        'solution. The test cases covered N = 4 (2 solutions), N = 5 (10 solutions), N = 6 (4 '
        'solutions), and the classic N = 8 (92 solutions), validating the correctness and efficiency '
        'of the O(N!) worst-case backtracking implementation.'
    )

    # Save
    output_path = r"c:\C++\ADA\n_queens\NQueens_Theory.docx"
    try:
        doc.save(output_path)
        print(f"Document saved to: {output_path}")
    except PermissionError:
        output_path = r"c:\C++\ADA\n_queens\NQueens_Theory_v2.docx"
        doc.save(output_path)
        print(f"Original locked. Saved to: {output_path}")


if __name__ == "__main__":
    create_document()
