"""
Plot MCM benchmark results — Measured Time vs Theoretical O(n^3)
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ---- Read data ----
data_file = "mcm_results.txt"

if not os.path.exists(data_file):
    print(f"Error: {data_file} not found. Run mcm_benchmark first.")
    exit(1)

sizes = []
times = []

with open(data_file, 'r') as f:
    header = f.readline()  # skip header
    for line in f:
        line = line.strip()
        if line:
            parts = line.split(',')
            sizes.append(int(parts[0]))
            times.append(float(parts[1]))

sizes = np.array(sizes)
times = np.array(times)

# ---- Compute theoretical O(n^3) curve ----
n3 = sizes ** 3
# Scale theoretical curve to match measured data range
scale_factor = np.max(times) / np.max(n3)
theoretical = n3 * scale_factor

# ---- Plot ----
plt.figure(figsize=(12, 7))
plt.style.use('seaborn-v0_8-darkgrid')

plt.plot(sizes, times, 'o-', color='#2196F3', linewidth=2,
         markersize=4, label='Measured Time', alpha=0.9)
plt.plot(sizes, theoretical, '--', color='#FF5722', linewidth=2,
         label='Theoretical O(n³)', alpha=0.8)

plt.xlabel('Number of Matrices (n)', fontsize=13, fontweight='bold')
plt.ylabel('Time (microseconds)', fontsize=13, fontweight='bold')
plt.title('Matrix Chain Multiplication — Time Complexity Analysis\nMeasured vs Theoretical O(n³)',
          fontsize=15, fontweight='bold', pad=15)
plt.legend(fontsize=12, loc='upper left')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('mcm_graph.png', dpi=150, bbox_inches='tight')
plt.show()

print("Graph saved to: mcm_graph.png")
