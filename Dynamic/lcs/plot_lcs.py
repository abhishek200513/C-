"""
Plot LCS benchmark results — Measured Time vs Theoretical O(n^2)
"""

import numpy as np
import matplotlib.pyplot as plt
import os

data_file = "lcs_results.txt"

if not os.path.exists(data_file):
    print(f"Error: {data_file} not found. Run lcs_benchmark first.")
    exit(1)

sizes = []
times = []

with open(data_file, 'r') as f:
    header = f.readline()
    for line in f:
        line = line.strip()
        if line:
            parts = line.split(',')
            sizes.append(int(parts[0]))
            times.append(float(parts[1]))

sizes = np.array(sizes)
times = np.array(times)

# Theoretical O(n^2) curve
n2 = sizes ** 2
scale_factor = np.max(times) / np.max(n2)
theoretical = n2 * scale_factor

plt.figure(figsize=(12, 7))
plt.style.use('seaborn-v0_8-darkgrid')

plt.plot(sizes, times, 'o-', color='#4CAF50', linewidth=2,
         markersize=4, label='Measured Time', alpha=0.9)
plt.plot(sizes, theoretical, '--', color='#FF5722', linewidth=2,
         label='Theoretical O(n²)', alpha=0.8)

plt.xlabel('String Length (n)', fontsize=13, fontweight='bold')
plt.ylabel('Time (microseconds)', fontsize=13, fontweight='bold')
plt.title('Longest Common Subsequence — Time Complexity Analysis\nMeasured vs Theoretical O(n²)',
          fontsize=15, fontweight='bold', pad=15)
plt.legend(fontsize=12, loc='upper left')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('lcs_graph.png', dpi=150, bbox_inches='tight')
plt.show()

print("Graph saved to: lcs_graph.png")
