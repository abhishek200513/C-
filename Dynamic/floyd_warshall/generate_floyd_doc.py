import copy
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

INF = float('inf')

def print_matrix_to_doc(doc, matrix, V):
    tbl = doc.add_table(rows=V + 1, cols=V + 1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    cell = tbl.cell(0, 0)
    cell.text = "v"
    set_cell_shading(cell, "D9E2F3")
    for pp in cell.paragraphs:
        pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in pp.runs: r.bold = True; r.font.name = 'Times New Roman'

    for j in range(V):
        cell = tbl.cell(0, j + 1)
        cell.text = str(j)
        set_cell_shading(cell, "D9E2F3")
        for pp in cell.paragraphs:
            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in pp.runs: r.bold = True; r.font.name = 'Times New Roman'

    for i in range(V):
        cell = tbl.cell(i + 1, 0)
        cell.text = str(i)
        set_cell_shading(cell, "D9E2F3")
        for pp in cell.paragraphs:
            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in pp.runs: r.bold = True; r.font.name = 'Times New Roman'

        for j in range(V):
            cell = tbl.cell(i + 1, j + 1)
            val = matrix[i][j]
            cell.text = "INF" if val == INF else str(val)
            for pp in cell.paragraphs:
                pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in pp.runs: r.font.name = 'Times New Roman'
    doc.add_paragraph()

def run_floyd_for_doc(doc, case_num, label, n, raw_matrix):
    mat = [[INF]*n for _ in range(n)]
    idx = 0
    for i in range(n):
        for j in range(n):
            val = raw_matrix[idx]
            idx += 1
            if val != -1:
                mat[i][j] = val

    heading = doc.add_heading(f'Test Case {case_num}: {label}', level=2)
    fix_heading(heading)
    for run in heading.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)

    add_styled_para(doc, "Input:", bold=True, size=11)
    add_styled_para(doc, f"n = {n}", size=11)
    add_styled_para(doc, " ".join(map(str, raw_matrix)), size=11)
    
    add_styled_para(doc, "Initial Matrix:", bold=True, size=11)
    print_matrix_to_doc(doc, mat, n)

    for k in range(n):
        add_styled_para(doc, f"Iteration k={k} (Intermediate Vertex = {k})", bold=True, size=11)
        updates = []
        for i in range(n):
            for j in range(n):
                if mat[i][k] != INF and mat[k][j] != INF and mat[i][k] + mat[k][j] < mat[i][j]:
                    oldVal = mat[i][j]
                    newVal = mat[i][k] + mat[k][j]
                    updates.append((i, j, oldVal, newVal, mat[i][k], mat[k][j]))
        
        if not updates:
            add_styled_para(doc, "Why change/no change: No update in this iteration.", size=11)
        else:
            for u in updates:
                i, j, oldVal, newVal, ik, kj = u
                oldStr = "INF" if oldVal == INF else str(oldVal)
                add_styled_para(doc, f"● dist[{i}][{j}] changed from {oldStr} to {newVal} because dist[{i}][{k}] + dist[{k}][{j}] = {ik} + {kj} = {newVal} < {oldStr}.", size=11)
                mat[i][j] = newVal
        
        add_styled_para(doc, f"Resulting Matrix (After k={k}):", bold=True, size=11)
        print_matrix_to_doc(doc, mat, n)
    
    add_styled_para(doc, "Output:", bold=True, size=11)
    print_matrix_to_doc(doc, mat, n)
    doc.add_page_break()

def create_floyd_doc():
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

    title = doc.add_heading('Experiment 12', level=0)
    fix_heading(title)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(22)
        run.font.color.rgb = RGBColor(0, 0, 0)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('All-Pairs Shortest Path (APSP) using Floyd-Warshall Algorithm')
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'
    doc.add_paragraph()

    # Aim
    h = doc.add_heading('Aim:', level=1)
    fix_heading(h)
    for run in h.runs: run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph('To find the shortest path distances between every pair of vertices in a weighted directed graph using Dynamic Programming.')

    # Problem Statement
    h = doc.add_heading('Problem Statement:', level=1)
    fix_heading(h)
    for run in h.runs: run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph('Given a weighted directed graph in adjacency matrix form, compute the minimum distance between every pair of vertices. If there exists a negative weight cycle, paths may be undefined but the algorithm provides distances under standard constraints.')

    # Theory (Expanded)
    h = doc.add_heading('Theory:', level=1)
    fix_heading(h)
    for run in h.runs: run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    
    doc.add_paragraph(
        'The Floyd-Warshall algorithm is a dynamic programming formulation to solve the All-Pairs Shortest Path problem on a directed graph with edge weights. '
        'Unlike Dijkstra’s algorithm, which requires non-negative edge weights and finds paths randomly iteratively from a single source, '
        'Floyd-Warshall can handle negative weights (as long as there are no negative weight cycles). It works efficiently by evaluating all possible paths '
        'systematically between pairs using intermediate vertices.'
    )
    doc.add_paragraph(
        'The algorithm operates by progressively allowing vertices to act as intermediate nodes in paths. '
        'Initially, the shortest path between any two nodes i and j without using any intermediate nodes is simply the weight of the direct edge connecting them. '
        'Then, for each node k from 0 to n-1, the algorithm examines whether traversing through node k offers a shorter path than the previously known shortest path.'
    )
    doc.add_paragraph(
        'Formally, the recurrence relation is given by:'
    )
    add_styled_para(doc, "dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])", bold=True, size=12, font='Consolas')
    doc.add_paragraph(
        'This means that at iteration k, the shortest path from i to j using nodes {0, 1, ..., k} as intermediate nodes '
        'is the minimum of the shortest path using only {0, ... k-1} and the path going from i to k and then k to j. '
        'Because of the triple nested loop structure over k, i, and j (each ranging from 0 to n-1), the algorithm exhibits a clear time complexity of O(V³), where V is the number of vertices. '
        'The spatial complexity is O(V²) which is identical to the space required to store the adjacency matrix itself.'
    )

    # Algorithm
    h = doc.add_heading('Algorithm:', level=1)
    fix_heading(h)
    for run in h.runs: run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    alg_text = [
        'Initialize the dist[][] matrix from the given input graph matrix where dist[i][j] equals edge weight (INF if no entry, 0 for i=j).',
        'For intermediate vertex k = 0 to n-1:',
        '    For source vertex i = 0 to n-1:',
        '        For destination vertex j = 0 to n-1:',
        '            If dist[i][k] + dist[k][j] < dist[i][j]:',
        '                Update dist[i][j] = dist[i][k] + dist[k][j]',
        'The final matrix provides the shortest paths between all pairs.'
    ]
    for step in alg_text:
        pp = doc.add_paragraph(step, style='List Bullet')
        for r in pp.runs: r.font.name = 'Times New Roman'

    # Input section
    h = doc.add_heading('Input:', level=1)
    fix_heading(h)
    for run in h.runs: run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph('Using predefined 5 test cases covering varying constraints.')

    doc.add_page_break()

    # Test Cases (Changed fully)
    h = doc.add_heading('Test Cases:', level=1)
    fix_heading(h)
    for run in h.runs: run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)

    # Case 1: Standard 4 nodes
    run_floyd_for_doc(doc, 1, "Standard 4 Nodes Case", 4, [
        0, 3, -1, 7,
        8, 0, 2, -1,
        5, -1, 0, 1,
        2, -1, -1, 0
    ])

    # Case 2: Negative Weight Path 3 nodes
    run_floyd_for_doc(doc, 2, "Negative Edge Standard", 3, [
        0, 4, -1,
        -1, 0, -2,
        3, -1, 0
    ])

    # Case 3: Disconnected components
    run_floyd_for_doc(doc, 3, "Disconnected Components", 4, [
        0, 2, -1, -1,
        -1, 0, -1, -1,
        -1, -1, 0, 5,
        -1, -1, -1, 0
    ])

    # Case 4: Complete Small Graph
    run_floyd_for_doc(doc, 4, "Complete Graph 3x3", 3, [
        0, 4, 11,
        6, 0, 2,
        3, 8, 0
    ])

    # Case 5: 5 Node Complex
    run_floyd_for_doc(doc, 5, "5 Node Dense Graph", 5, [
        0, 2, -1, 1, 8,
        6, 0, 3, 2, -1,
        -1, -1, 0, 4, -1,
        -1, -1, 2, 0, 3,
        3, -1, -1, -1, 0
    ])

    # Result & Conclusion
    h = doc.add_heading('Output:', level=1)
    fix_heading(h)
    for run in h.runs: run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    add_styled_para(doc, "Result:")
    add_styled_para(doc, "All predefined test cases were executed with full iteration-wise updates showcasing how shortest paths stabilize over iterations.")

    h = doc.add_heading('Conclusion:', level=1)
    fix_heading(h)
    for run in h.runs: run.font.name = 'Times New Roman'; run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph(
        'The Floyd-Warshall algorithm successfully computed the shortest path distance for all vertex pairs across the suite of test cases. '
        'Through progressive consideration of each node as an intermediate step, the algorithm efficiently converged to globally minimum distance paths. '
        'Various instances like standard cases, disconnected components, and graphs involving negative edges were effectively handled, validating the dynamic programming recurrence.'
    )

    doc.save(r"c:\C++\ADA\floyd_warshall\Floyd_Warshall_Theory.docx")
    print("Floyd Word Doc generated successfully.")

if __name__ == "__main__":
    create_floyd_doc()
