import matplotlib.pyplot as plt
import numpy as np

def plot_knapsack():
    """Visualize Fractional Knapsack - 3 Greedy Strategies Comparison"""

    # -------- Item Data (same as C++ program) --------
    items = [
        {"id": 1, "weight": 2,  "profit": 10},
        {"id": 2, "weight": 3,  "profit": 5},
        {"id": 3, "weight": 5,  "profit": 15},
        {"id": 4, "weight": 7,  "profit": 7},
        {"id": 5, "weight": 1,  "profit": 6},
        {"id": 6, "weight": 4,  "profit": 18},
        {"id": 7, "weight": 1,  "profit": 3},
    ]

    capacity = 15

    # Calculate ratios
    for item in items:
        item["ratio"] = item["profit"] / item["weight"]

    # -------- Solve with 3 strategies --------
    def solve(sorted_items, cap):
        total_profit = 0
        remaining = cap
        taken = []  # list of (item_id, fraction, profit_gained)
        for item in sorted_items:
            if remaining == 0:
                break
            if item["weight"] <= remaining:
                total_profit += item["profit"]
                remaining -= item["weight"]
                taken.append((item["id"], 1.0, item["profit"]))
            else:
                frac = remaining / item["weight"]
                gained = item["profit"] * frac
                total_profit += gained
                taken.append((item["id"], frac, gained))
                remaining = 0
        return total_profit, taken

    # Strategy 1: Least Weight First
    s1 = sorted(items, key=lambda x: x["weight"])
    profit1, taken1 = solve(s1, capacity)

    # Strategy 2: Maximum Profit First
    s2 = sorted(items, key=lambda x: x["profit"], reverse=True)
    profit2, taken2 = solve(s2, capacity)

    # Strategy 3: Best Ratio First
    s3 = sorted(items, key=lambda x: x["ratio"], reverse=True)
    profit3, taken3 = solve(s3, capacity)

    strategies = ["Least Weight\nFirst", "Maximum Profit\nFirst", "Best Ratio\nFirst\n(Optimal)"]
    profits = [profit1, profit2, profit3]
    colors = ["#4285F4", "#EA4335", "#34A853"]

    # ===================== Bar Chart Comparison =====================
    plt.style.use('default')
    fig, ax1 = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('white')
    ax1.set_facecolor('white')

    bars = ax1.bar(strategies, profits, color=colors, width=0.55,
                   edgecolor='white', linewidth=1.5, zorder=3)

    # Add value labels on bars
    for bar, profit in zip(bars, profits):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 f'{profit:.2f}', ha='center', va='bottom',
                 fontsize=14, fontweight='bold', color='#333333')

    ax1.set_ylabel('Total Profit', fontsize=14, fontweight='bold', color='black')
    ax1.set_title('Fractional Knapsack — Greedy Strategy Analysis\n'
                  f'(7 Items, Capacity = {capacity})',
                  fontsize=18, fontweight='bold', color='#1a73e8', pad=15)
    ax1.set_ylim(0, max(profits) * 1.2)
    ax1.grid(True, axis='y', linestyle='--', alpha=0.3, color='gray', zorder=0)
    ax1.tick_params(axis='both', colors='black', labelsize=11)

    # Highlight the best bar
    best_idx = profits.index(max(profits))
    bars[best_idx].set_edgecolor('#34A853')
    bars[best_idx].set_linewidth(3)

    plt.tight_layout()
    plt.savefig('knapsack_graph.png', dpi=150, facecolor='white',
                edgecolor='none', bbox_inches='tight')
    print("Graph saved as: knapsack_graph.png")
    plt.show()

    # Print summary
    print("\n" + "=" * 55)
    print("   FRACTIONAL KNAPSACK — STRATEGY COMPARISON")
    print("=" * 55)
    print(f"  {'Strategy':<30} {'Profit':>10}")
    print("-" * 55)
    print(f"  {'1. Least Weight First':<30} {profit1:>10.2f}")
    print(f"  {'2. Maximum Profit First':<30} {profit2:>10.2f}")
    print(f"  {'3. Best Ratio First (Optimal)':<30} {profit3:>10.2f}")
    print("-" * 55)
    print(f"\n  >> Best: Ratio-based greedy = {max(profits):.2f}")
    print("=" * 55)


if __name__ == "__main__":
    plot_knapsack()
