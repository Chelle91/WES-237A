import time
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# CPU Frequency in Hz (CHANGE this based on your system)
CPU_FREQUENCY_HZ = 6500000000  # Example: 2.4 GHz = 2,400,000,000 Hz

# Function to get cycle count
def get_cycle_count():
    try:
        with open("/proc/self/stat", "r") as f:
            return int(f.readline().split()[19])  # 'voluntary_ctxt_switches'
    except:
        return 0  # If unsupported, return 0

# Recursive Fibonacci function
def recur_fibo(n):
    if n <= 1:
        return n
    else:
        return recur_fibo(n - 1) + recur_fibo(n - 2)

# Set CPU affinity to CPU 1 (if supported)
try:
    os.sched_setaffinity(0, {1})
except AttributeError:
    print("CPU affinity not supported on this system.")

# Experiment parameters
n_values = [1, 5, 10, 15, 20, 25, 30]  # Adjust as needed
num_trials = 3  # Number of trials per n

results = []

for n in n_values:
    cycle_counts = []
    time_durations = []
    pmu_times = []

    for _ in range(num_trials):
        before_cycles = get_cycle_count()
        before_time = time.time()

        recur_fibo(n)

        after_cycles = get_cycle_count()
        after_time = time.time()

        cycles = after_cycles - before_cycles
        elapsed_time = after_time - before_time
        pmu_time = cycles / CPU_FREQUENCY_HZ  # Convert cycles to time

        cycle_counts.append(cycles)
        time_durations.append(elapsed_time)
        pmu_times.append(pmu_time)

    # Compute mean and standard deviation error
    avg_cycles = np.mean(cycle_counts)
    avg_time = np.mean(time_durations)
    avg_pmu_time = np.mean(pmu_times)

    stddev_cycles = np.std(cycle_counts) / np.sqrt(num_trials)
    stddev_time = np.std(time_durations) / np.sqrt(num_trials)
    stddev_pmu_time = np.std(pmu_times) / np.sqrt(num_trials)

    results.append((n, avg_cycles, stddev_cycles, avg_time, stddev_time, avg_pmu_time, stddev_pmu_time))

# Extract values for plotting
(n_values, avg_cycles, std_cycles_err, avg_time, std_time_err, avg_pmu_time, std_pmu_time_err) = zip(*results)

# Create the plots
fig, ax1 = plt.subplots()

# Plot execution time from time module
ax1.errorbar(n_values, avg_time, yerr=std_time_err, fmt='-o', color='b', label="Execution Time (s) - time module")
ax1.errorbar(n_values, avg_pmu_time, yerr=std_pmu_time_err, fmt='--x', color='g', label="Execution Time (s) - PMU")

ax1.set_xlabel("Fibonacci Term (n)")
ax1.set_ylabel("Execution Time (seconds)")
ax1.legend()
plt.title("Execution Time: time module vs PMU")
fig.tight_layout()

# Save the plot
plt.savefig("time_vs_pmu.png")
print("Comparison plot saved as 'time_vs_pmu.png'. Open it manually to view.")