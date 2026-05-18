"""
Generate Multistage Graph Theory Word Document
with expanded theory and new test cases.
Mirrors the Floyd-Warshall document format.
"""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

INF = float('inf')
INF_STR = "INF"


def fix_heading(heading):
    """Remove spacing after a heading paragraph."""
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


def add_styled_paragraph(doc, text, bold=False, italic=False, size=11, font='Times New Roman'):
    """Add a styled paragraph to the document."""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = font
    return p


def add_bullet(doc, text, size=10, font='Times New Roman'):
    """Add a bullet point."""
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = font
    return p


def solve_multistage(V, stages, stage_of, edges):
    """
    Solve multistage graph using backward DP approach (right to left).
    Returns cost[], next[], and step-by-step trace.
    """
    # Build adjacency: adj[i] = list of (j, weight) for edges i->j
    adj = {i: [] for i in range(V)}
    for (u, v, w) in edges:
        adj[u].append((v, w))

    sink = V - 1
    cost = [INF] * V
    nxt = [-1] * V
    cost[sink] = 0

    steps = []  # Each step: (node, stage, evaluations, final_cost, next_node)

    # Process from sink-1 down to 0
    for i in range(V - 2, -1, -1):
        evaluations = []  # (target_j, edge_weight, cost_j, total, is_min)
        best_cost = INF
        best_next = -1

        for (j, w) in sorted(adj[i], key=lambda x: x[0]):
            if cost[j] != INF:
                total = w + cost[j]
            else:
                total = INF
            evaluations.append((j, w, cost[j], total))
            if total < best_cost:
                best_cost = total
                best_next = j

        cost[i] = best_cost
        nxt[i] = best_next
        steps.append((i, stage_of[i], evaluations, best_cost, best_next))

    # Trace path
    path = []
    path_edges = []
    current = 0
    while current != -1:
        path.append(current)
        next_node = nxt[current]
        if next_node != -1:
            # Find edge weight
            for (j, w) in adj[current]:
                if j == next_node:
                    path_edges.append(w)
                    break
        current = next_node

    return cost, nxt, steps, path, path_edges


def add_final_table(doc, V, cost, nxt):
    """Add the final cost/next table."""
    add_styled_paragraph(doc, "Final Table:", bold=True, size=11)

    table = doc.add_table(rows=V + 1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)

    headers = ["Vertex", "Cost", "Next"]
    for ci, h in enumerate(headers):
        cell = table.cell(0, ci)
        cell.text = h
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(10)
                run.font.name = 'Times New Roman'
        set_cell_shading(cell, "D9E2F3")

    for i in range(V):
        # Vertex
        cell = table.cell(i + 1, 0)
        cell.text = str(i)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(10)
                run.font.name = 'Times New Roman'

        # Cost
        cell = table.cell(i + 1, 1)
        cell.text = str(cost[i]) if cost[i] != INF else INF_STR
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(10)
                run.font.name = 'Times New Roman'

        # Next
        cell = table.cell(i + 1, 2)
        cell.text = str(nxt[i]) if nxt[i] != -1 else "--"
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(10)
                run.font.name = 'Times New Roman'

    doc.add_paragraph()


def add_test_case(doc, case_num, label, V, num_stages, stage_of, edges):
    """Add a complete test case to the document."""
    sink = V - 1

    # Heading
    heading = doc.add_heading(f'Test Case {case_num}: {label}', level=2)
    fix_heading(heading)
    for run in heading.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    # Input section
    add_styled_paragraph(doc, "Input:", bold=True, size=11)
    add_styled_paragraph(
        doc,
        f"nodes = {V}, stages = {num_stages}, source = 0, destination = {sink}, edges = {len(edges)}",
        size=11
    )

    # Edge list
    for (u, v, w) in edges:
        add_styled_paragraph(doc, f"w({u}, {v}) = {w}", size=11, font='Consolas')

    # Solve
    cost, nxt, steps, path, path_edges = solve_multistage(V, num_stages, stage_of, edges)

    # DP Solution
    add_styled_paragraph(doc, "DP Solution (Backward Approach):", bold=True, size=11)

    p = doc.add_paragraph()
    run = p.add_run(f"Initialize cost[{sink}] = 0 at the destination and process nodes {sink} down to 0.")
    run.font.size = Pt(10)
    run.font.name = 'Times New Roman'
    run.italic = True

    for (node, stage, evaluations, final_cost, next_node) in steps:
        if not evaluations:
            # Sink or no outgoing edges
            add_bullet(
                doc,
                f"Node {node} [S{stage}]: No outgoing edges."
            )
        elif len(evaluations) == 1:
            # Single edge — simpler text
            j, w, cj, total = evaluations[0]
            add_bullet(
                doc,
                f"Node {node} [S{stage}]: cost[{node}] = w({node},{j}) + cost[{j}] "
                f"= {w} + {cj} = {total}. UPDATE: next[{node}] = {j}."
            )
        else:
            # Multiple edges — show min comparison
            parts = []
            vals = []
            for (j, w, cj, total) in evaluations:
                parts.append(f"w({node},{j})+cost[{j}]")
                if total == INF:
                    vals.append("INF")
                else:
                    vals.append(f"{w}+{cj}")

            min_expr = ", ".join(parts)
            val_expr = ", ".join(vals)

            # Check for tie
            tie_count = sum(1 for (_, _, _, t) in evaluations if t == final_cost)
            if tie_count > 1:
                add_bullet(
                    doc,
                    f"Node {node} [S{stage}]: cost[{node}] = min({min_expr}) "
                    f"= min({val_expr}) = {final_cost}. TIE: Both paths cost {final_cost}; "
                    f"choose next[{node}] = {next_node} to break the tie."
                )
            else:
                add_bullet(
                    doc,
                    f"Node {node} [S{stage}]: cost[{node}] = min({min_expr}) "
                    f"= min({val_expr}) = {final_cost}. UPDATE: next[{node}] = {next_node}."
                )

    # Final Table
    add_final_table(doc, V, cost, nxt)

    # Output
    add_styled_paragraph(doc, "Output:", bold=True, size=11)

    # Shortest path string
    path_str = ""
    for idx, node in enumerate(path):
        if idx > 0:
            path_str += f" -({path_edges[idx-1]})-> {node}"
        else:
            path_str = str(node)

    add_styled_paragraph(doc, f"Shortest path: {path_str}", size=11)
    add_styled_paragraph(doc, f"Minimum cost : {cost[0]}", size=11)

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
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    # Remove spacing after heading styles
    for i in range(4):
        hstyle = doc.styles[f'Heading {i}'] if i > 0 else doc.styles['Title']
        hstyle.paragraph_format.space_after = Pt(0)

    # ===== TITLE =====
    title = doc.add_heading('Experiment 13', level=0)
    fix_heading(title)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(22)
        run.font.color.rgb = RGBColor(0, 0, 0)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('Shortest Path in a Multistage Graph using Dynamic Programming')
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

    p = doc.add_paragraph(
        'To find the shortest (minimum-cost) path from the source vertex to the destination vertex '
        'in a multistage graph using the dynamic programming approach.'
    )

    # ===== PROBLEM STATEMENT =====
    h = doc.add_heading('Problem Statement:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    p = doc.add_paragraph(
        'Given a weighted directed multistage graph with n vertices divided into k stages, where edges '
        'only go from vertices in stage i to vertices in stage i+1, find the minimum-cost path from the '
        'source (stage 1) to the sink (stage k). The graph is represented as a set of weighted edges '
        'between consecutive stages.'
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
        'A multistage graph is a special type of directed weighted graph in which the vertices are '
        'partitioned into k disjoint stages (S₁, S₂, …, Sₖ). Edges exist only between consecutive '
        'stages — that is, an edge can go from a vertex in stage Sᵢ to a vertex in stage Sᵢ₊₁, but '
        'never within the same stage or to a non-adjacent stage. The first stage S₁ contains a single '
        'source vertex, and the last stage Sₖ contains a single sink (destination) vertex. The objective '
        'is to find the minimum-cost path from the source to the sink.'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Paragraph 2 — Why DP
    p = doc.add_paragraph()
    run = p.add_run('Why Dynamic Programming?')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'The multistage graph problem exhibits two key properties that make it ideal for a dynamic '
        'programming solution: optimal substructure and overlapping subproblems. The optimal '
        'substructure property ensures that any sub-path of the shortest path is itself a shortest '
        'path. The overlapping subproblems property arises because multiple paths from earlier stages '
        'may pass through the same intermediate vertex, and the cost from that vertex to the sink can '
        'be computed once and reused. A greedy approach would simply pick the cheapest edge at every '
        'step, which often leads to suboptimal solutions because a locally cheap edge may connect to '
        'an expensive subsequent path. Dynamic programming avoids this by considering the total cost '
        'to the destination at every decision point.'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Paragraph 3 — Forward vs Backward
    p = doc.add_paragraph()
    run = p.add_run('Forward and Backward Approaches:')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'The problem can be solved using two equivalent approaches. In the Backward Approach '
        '(also called the Forward Formulation), we define cost[i] as the minimum cost from vertex i '
        'to the sink. We start at the sink (cost[sink] = 0) and work backwards to the source, computing '
        'cost[i] = min{w(i,j) + cost[j]} for all edges (i, j). This yields cost[source] as the answer. '
        'In the Forward Approach (also called the Backward Formulation), we define cost[j] as the '
        'minimum cost from the source to vertex j. We start at the source (cost[source] = 0) and work '
        'forward to the sink, computing cost[j] = min{cost[i] + w(i,j)} for all edges (i, j). Both '
        'approaches yield the same optimal cost and path.'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Paragraph 4 — Recurrence
    p = doc.add_paragraph()
    run = p.add_run('Recurrence Relation (Backward Approach):')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'Let cost[i] denote the minimum cost from vertex i to the sink. Let w(i,j) denote the weight '
        'of edge from vertex i to vertex j. The recurrence is:'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Formula
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('cost[i] = min { w(i, j) + cost[j] }  for all edges (i, j)')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Consolas'

    p = doc.add_paragraph()
    run = p.add_run(
        'Base case: cost[sink] = 0. The algorithm processes vertices from right to left (from the '
        'sink toward the source). At each vertex, we also store next[i] — the vertex that achieves '
        'the minimum — so that the actual shortest path can be reconstructed by following the chain '
        'of next[] pointers from the source to the sink.'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Paragraph 5 — How it works step by step
    p = doc.add_paragraph()
    run = p.add_run('Step-by-Step Working:')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    run = p.add_run(
        'The algorithm initializes cost[sink] = 0 and cost[i] = ∞ for all other vertices. It then '
        'iterates from vertex (n-2) down to vertex 0. For each vertex i, it examines all outgoing edges '
        '(i, j). For each such edge, it computes the candidate cost w(i, j) + cost[j]. If this value is '
        'less than the current cost[i], it updates cost[i] and sets next[i] = j. After processing all '
        'vertices, cost[0] contains the minimum cost from source to sink, and the path is reconstructed '
        'by following next[0] → next[next[0]] → … → sink.'
    )
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    # Paragraph 6 — Complexity
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
        ("Time Complexity", "O(V + E)"),
        ("Space Complexity", "O(V²) for adjacency matrix"),
        ("Auxiliary Space", "O(V) for cost[] and next[]")
    ]
    for idx, (col1, col2) in enumerate(complexity_data):
        for ci, val in enumerate([col1, col2]):
            cell = table.cell(idx, ci)
            cell.text = val
            for par in cell.paragraphs:
                par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in par.runs:
                    run.font.size = Pt(10)
                    run.font.name = 'Times New Roman'
                    if idx == 0:
                        run.bold = True
            if idx == 0:
                set_cell_shading(cell, "D9E2F3")

    doc.add_paragraph()

    # Advantages
    p = doc.add_paragraph()
    run = p.add_run('Advantages:')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    advantages = [
        'Guarantees the globally optimal shortest path, unlike greedy approaches.',
        'Efficient O(V + E) time complexity — each vertex and edge is processed exactly once.',
        'Naturally exploits the DAG (Directed Acyclic Graph) structure of multistage graphs.',
        'Simple to implement with two arrays: cost[] and next[].',
        'Both forward and backward formulations can be used depending on the problem setup.'
    ]
    for adv in advantages:
        p = doc.add_paragraph(adv, style='List Bullet')
        for run in p.runs:
            run.font.size = Pt(11)
            run.font.name = 'Times New Roman'

    # Limitations
    p = doc.add_paragraph()
    run = p.add_run('Limitations:')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    limitations = [
        'Only applicable to multistage (layered) graph structures — cannot handle general graphs.',
        'Requires the graph to be a DAG with a well-defined stage assignment for each vertex.',
        'Adjacency matrix representation requires O(V²) space, which is wasteful for sparse graphs.',
        'Does not handle negative edge weights or cycles.'
    ]
    for lim in limitations:
        p = doc.add_paragraph(lim, style='List Bullet')
        for run in p.runs:
            run.font.size = Pt(11)
            run.font.name = 'Times New Roman'

    # Applications
    p = doc.add_paragraph()
    run = p.add_run('Applications:')
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    applications = [
        'Resource allocation problems where resources are distributed across sequential stages.',
        'Project scheduling and pipeline optimization where tasks proceed through defined phases.',
        'Network routing in layered communication networks (e.g., hierarchical network topologies).',
        'Manufacturing process optimization where items pass through sequential production stages.',
        'Dynamic decision-making models in operations research and economics.'
    ]
    for app in applications:
        p = doc.add_paragraph(app, style='List Bullet')
        for run in p.runs:
            run.font.size = Pt(11)
            run.font.name = 'Times New Roman'

    # ===== ALGORITHM =====
    h = doc.add_heading('Algorithm:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    steps = [
        'Initialize cost[sink] = 0 and cost[i] = ∞ for all other vertices. Set next[i] = -1 for all i.',
        'For i = (n-2) down to 0:',
        '    For each edge (i, j) from vertex i:',
        '        If w(i, j) + cost[j] < cost[i], then update cost[i] = w(i, j) + cost[j] and next[i] = j.',
        'The answer is cost[0] (minimum cost from source to sink).',
        'Reconstruct the path by following: source → next[source] → next[next[source]] → … → sink.'
    ]
    for step in steps:
        p = doc.add_paragraph(step, style='List Bullet')
        for run in p.runs:
            run.font.size = Pt(11)
            run.font.name = 'Times New Roman'

    # Pseudocode
    add_styled_paragraph(doc, "Pseudocode:", bold=True, size=12)

    pseudocode = """MULTISTAGE-SHORTEST-PATH(G, V, sink):
    cost[sink] ← 0
    for i ← (V-2) down to 0 do
        for each edge (i, j) in G do
            if w(i,j) + cost[j] < cost[i] then
                cost[i] ← w(i,j) + cost[j]
                next[i] ← j
    return cost[0], next[]"""

    p = doc.add_paragraph()
    run = p.add_run(pseudocode)
    run.font.size = Pt(10)
    run.font.name = 'Consolas'

    doc.add_paragraph()

    # ===== INPUT =====
    h = doc.add_heading('Input:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    p = doc.add_paragraph('Using 4 predefined test cases with varied graph layouts.')

    doc.add_page_break()

    # ===== TEST CASES =====
    h = doc.add_heading('Test Cases:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    # ---- Test Case 1: Small Graph — 4 Stages, 6 Nodes ----
    # Stage 1: {0}, Stage 2: {1,2}, Stage 3: {3,4}, Stage 4: {5}
    tc1_V = 6
    tc1_stages = 4
    tc1_stage_of = [1, 2, 2, 3, 3, 4]
    tc1_edges = [
        (0, 1, 5), (0, 2, 3),
        (1, 3, 2), (1, 4, 6),
        (2, 3, 4), (2, 4, 3),
        (3, 5, 3), (4, 5, 2)
    ]
    add_test_case(doc, 1, "Small Graph — 4 Stages, 6 Nodes",
                  tc1_V, tc1_stages, tc1_stage_of, tc1_edges)

    # ---- Test Case 2: Equal Cost Paths — Tie-Breaking ----
    tc2_V = 6
    tc2_stages = 4
    tc2_stage_of = [1, 2, 2, 3, 3, 4]
    tc2_edges = [
        (0, 1, 2), (0, 2, 5),
        (1, 3, 4), (1, 4, 7),
        (2, 3, 8), (2, 4, 2),
        (3, 5, 6), (4, 5, 5)
    ]
    add_test_case(doc, 2, "Equal Cost Paths — Tie-Breaking",
                  tc2_V, tc2_stages, tc2_stage_of, tc2_edges)

    # ---- Test Case 3: Large Graph — 6 Stages, 10 Nodes ----
    # Stage 1: {0}, Stage 2: {1,2}, Stage 3: {3,4}, Stage 4: {5,6}, Stage 5: {7,8}, Stage 6: {9}
    tc3_V = 10
    tc3_stages = 6
    tc3_stage_of = [1, 2, 2, 3, 3, 4, 4, 5, 5, 6]
    tc3_edges = [
        (0, 1, 4), (0, 2, 3),
        (1, 3, 5), (1, 4, 2),
        (2, 3, 8), (2, 4, 4),
        (3, 5, 3), (3, 6, 4),
        (4, 5, 7), (4, 6, 2),
        (5, 7, 2), (5, 8, 6),
        (6, 7, 8), (6, 8, 3),
        (7, 9, 6), (8, 9, 3)
    ]
    add_test_case(doc, 3, "Large Graph — 6 Stages, 10 Nodes",
                  tc3_V, tc3_stages, tc3_stage_of, tc3_edges)

    # ---- Test Case 4: Non-Greedy Path — Greedy Fails Here ----
    tc4_V = 6
    tc4_stages = 4
    tc4_stage_of = [1, 2, 2, 3, 3, 4]
    tc4_edges = [
        (0, 1, 2), (0, 2, 8),
        (1, 3, 10), (1, 4, 14),
        (2, 3, 3), (2, 4, 1),
        (3, 5, 2), (4, 5, 3)
    ]
    add_test_case(doc, 4, "Non-Greedy Path — Greedy Fails Here",
                  tc4_V, tc4_stages, tc4_stage_of, tc4_edges)

    # ===== RESULT =====
    h = doc.add_heading('Result:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    p = doc.add_paragraph(
        'All 4 predefined test cases were executed successfully, accurately finding the shortest path '
        'and minimum cost from the source to the destination node.'
    )

    # ===== CONCLUSION =====
    h = doc.add_heading('Conclusion:', level=1)
    fix_heading(h)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    p = doc.add_paragraph(
        'The multistage graph shortest path algorithm, implemented using the backward dynamic '
        'programming approach, successfully determined the minimum-cost path from source to '
        'destination across all four test cases. By processing vertices from the sink backwards to '
        'the source, the algorithm computed the optimal cost at each vertex by considering all '
        'outgoing edges and selecting the one leading to the minimum total cost. The step-by-step '
        'trace demonstrated how the DP approach avoids the pitfalls of greedy selection — '
        'particularly evident in Test Case 4, where the locally cheapest edge from the source led '
        'to a globally suboptimal path. The algorithm\'s O(V + E) time complexity was confirmed '
        'through efficient single-pass processing of each vertex and edge. The diverse test cases — '
        'including small graphs, tie-breaking scenarios, larger multi-stage configurations, and '
        'non-greedy traps — validated the correctness and robustness of the implementation.'
    )

    # Save
    output_path = r"c:\C++\ADA\multistage_graph\Multistage_Graph_Theory.docx"
    try:
        doc.save(output_path)
        print(f"Document saved to: {output_path}")
    except PermissionError:
        output_path = r"c:\C++\ADA\multistage_graph\Multistage_Graph_Theory_v2.docx"
        doc.save(output_path)
        print(f"Original file locked. Document saved to: {output_path}")


if __name__ == "__main__":
    create_document()
