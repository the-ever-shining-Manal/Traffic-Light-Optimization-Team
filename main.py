from simulation.environment import Environment
from utils.visualization import run_animation
from algorithms.greedy import greedy_light as greedy
from algorithms.fixed import fixed_light as fixed
from algorithms.smart import smart_algorithm as smart
from utils.metrics import compute_metrics
import json
import math
from utils.plot import plot_results, plot_statistical_report
SIM_STEPS = 1000
def run_simulation(algorithm, animate=False):
    if animate:
        env = run_animation(algorithm,SIM_STEPS)
        return compute_metrics(env)

    env = Environment()

    for _ in range(SIM_STEPS):
        env.step(algorithm)

    return compute_metrics(env)




def main():
    print("1. Greedy")
    print("2. Fixed")
    print("3. Smart")
    print("4. Run ALL (Report)")

    choice = input("Choose algorithm: ")

    if choice == "1":
        env = run_animation(greedy,SIM_STEPS)
        result = compute_metrics(env)

        print("\n===== GREEDY METRICS =====")
        print(result)

    elif choice == "2":
        env = run_animation(fixed,SIM_STEPS)
        result = compute_metrics(env)

        print("\n===== FIXED METRICS =====")
        print(result)

    elif choice == "3":
        env = run_animation(smart,SIM_STEPS)
        result = compute_metrics(env)

        print("\n===== smart METRICS =====")
        print(result)

    elif choice == "4":
        run_full_report()

def run_full_report():
    algorithms = {
        "Greedy": greedy,
        "Fixed": fixed,
        "Smart": smart
    }

    TRIALS = 30
    results = {}
    agg_stats = {}

    for name, algo in algorithms.items():
        print(f"\nRunning {name} ({TRIALS} trials)...")
        trial_results = []
        for _ in range(TRIALS):
            trial_results.append(run_simulation(algo, animate=False))

        avg_wait_data = [r["average_wait"] for r in trial_results]
        mean_wait = sum(avg_wait_data) / TRIALS
        std_wait = math.sqrt(sum((x - mean_wait)**2 for x in avg_wait_data) / TRIALS) if TRIALS > 1 else 0
        ci95_wait = 1.96 * std_wait / math.sqrt(TRIALS) if TRIALS > 0 else 0

        results[name] = {
            "total_wait": sum(r["total_wait"] for r in trial_results) / TRIALS,
            "average_wait": mean_wait,
            "cars_passed": sum(r["cars_passed"] for r in trial_results) / TRIALS,
            "throughput": sum(r["throughput"] for r in trial_results) / TRIALS,
        }

        agg_stats[name] = {
            "average_wait": {"mean": mean_wait, "ci95": ci95_wait}
        }

    print("\n\n================ FULL REPORT ================\n")

    for name, data in results.items():
        print(f"{name.upper()}")
        print(f"Total Wait: {data['total_wait']:.2f} (avg over {TRIALS} trials)")
        print(f"Average Wait: {data['average_wait']:.2f}")
        print(f"Cars Passed: {data['cars_passed']:.2f}")
        print(f"Throughput: {data['throughput']:.2f}")
        print("------------------------------------")

    #  SAVE RESULTS
    with open("results.json", "w") as f:
        json.dump({"averages": results, "stats": agg_stats}, f, indent=4)

    #  PLOT RESULTS
    plot_results(results)
    plot_statistical_report(agg_stats)

if __name__ == "__main__": main()