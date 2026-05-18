import random
import csv
import time
import matplotlib.pyplot as plt
import math

def merge_sort(activity, start, end):
    if len(activity) <= 1:
        return activity, start, end

    mid = len(activity) // 2

    a1, s1, e1 = merge_sort(activity[:mid], start[:mid], end[:mid])
    a2, s2, e2 = merge_sort(activity[mid:], start[mid:], end[mid:])

    return merge(a1, s1, e1, a2, s2, e2)

def merge(a1, s1, e1, a2, s2, e2):
    i = j = 0
    a = []
    s = []
    e = []

    while i < len(a1) and j < len(a2):
        if e1[i] < e2[j]:
            a.append(a1[i])
            s.append(s1[i])
            e.append(e1[i])
            i += 1
        else:
            a.append(a2[j])
            s.append(s2[j])
            e.append(e2[j])
            j += 1

    while i < len(a1):
        a.append(a1[i])
        s.append(s1[i])
        e.append(e1[i])
        i += 1

    while j < len(a2):
        a.append(a2[j])
        s.append(s2[j])
        e.append(e2[j])
        j += 1

    return a, s, e

def activity_selection(activity, start, end):
    activity, start, end = merge_sort(activity, start, end)

    selected = [activity[0]]
    last_end = end[0]

    for i in range(1, len(activity)):
        if start[i] >= last_end:
            selected.append(activity[i])
            last_end = end[i]

    return selected

def best_case(n):
    activity = []
    start = []
    end = []
    curr = 0

    for i in range(n):
        s = curr
        e = s + 2
        curr = e + 1

        activity.append("A" + str(i))
        start.append(s)
        end.append(e)

    return activity, start, end

def average_case(n):
    activity = []
    start = []
    end = []

    for i in range(n):
        s = random.randint(0, n)
        e = s + random.randint(1, 10)

        activity.append("A" + str(i))
        start.append(s)
        end.append(e)

    return activity, start, end

def worst_case(n):
    activity = []
    start = []
    end = []

    base = random.randint(1, 50)

    for i in range(n):
        s = base + random.randint(0, 5)
        e = s + random.randint(50, 200)

        activity.append("A" + str(i))
        start.append(s)
        end.append(e)

    return activity, start, end


# 🔥 UPDATED FUNCTION (using perf_counter)
def measure_time(activity, start, end):
    total = 0

    for _ in range(100):
        t1 = time.perf_counter()
        activity_selection(activity, start, end)
        t2 = time.perf_counter()
        total += (t2 - t1)

    return total / 100


# Write to CSV
f = open("activity_selection.csv", "w", newline="")
writer = csv.writer(f)

writer.writerow(["n", "Best", "Average", "Worst"])

for n in range(100, 10001, 500):
    a, s, e = best_case(n)
    best_t = measure_time(a, s, e)

    a, s, e = average_case(n)
    avg_t = measure_time(a, s, e)

    a, s, e = worst_case(n)
    worst_t = measure_time(a, s, e)

    writer.writerow([n, best_t, avg_t, worst_t])

f.close()


# Read data from CSV
n_vals = []
best = []
avg = []
worst = []

with open("activity_selection.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        n_vals.append(int(row[0]))
        best.append(float(row[1]))
        avg.append(float(row[2]))
        worst.append(float(row[3]))

# Ideal time complexity: O(n log n)
ideal = [n * math.log2(n) for n in n_vals]

# Normalize ideal curve to match scale
scale = max(worst) / max(ideal)
ideal_scaled = [x * scale for x in ideal]


# -------- Graph 1: Best Case --------
plt.figure()
plt.plot(n_vals, best, label="Best Case")
plt.plot(n_vals, ideal_scaled, linestyle='--', label="O(n log n)")
plt.xlabel("n")
plt.ylabel("Time")
plt.title("Best Case Time Complexity")
plt.legend()
plt.grid()
plt.show()


# -------- Graph 2: Average Case --------
plt.figure()
plt.plot(n_vals, avg, label="Average Case")
plt.plot(n_vals, ideal_scaled, linestyle='--', label="O(n log n)")
plt.xlabel("n")
plt.ylabel("Time")
plt.title("Average Case Time Complexity")
plt.legend()
plt.grid()
plt.show()


# -------- Graph 3: Worst Case --------
plt.figure()
plt.plot(n_vals, worst, label="Worst Case")
plt.plot(n_vals, ideal_scaled, linestyle='--', label="O(n log n)")
plt.xlabel("n")
plt.ylabel("Time")
plt.title("Worst Case Time Complexity")
plt.legend()
plt.grid()
plt.show()


# -------- Graph 4: Comparison --------
plt.figure()
plt.plot(n_vals, best, label="Best")
plt.plot(n_vals, avg, label="Average")
plt.plot(n_vals, worst, label="Worst")
plt.plot(n_vals, ideal_scaled, linestyle='--', label="O(n log n)")
plt.xlabel("n")
plt.ylabel("Time")
plt.title("Comparison of Cases")
plt.legend()
plt.grid()
plt.show()