from simulation.environment import Environment
from utils.visualization import run_animation
from algorithms.greedy import greedy_light as greedy
from algorithms.fixed import fixed_light as fixed
#from algorithms.smart import """(name of your function)""" as smart
from utils.metrics import compute_metrics

def run_simulation(algorithm, animate=False):
    if animate:
        from utils.visualization import run_animation
        env = run_animation(algorithm)
        return compute_metrics(env)

    env = Environment()

    for _ in range(100):
        env.step(algorithm)

    return compute_metrics(env)




def main():
    print("1. Greedy")
    print("2. Fixed")
    print("3. Smart")
    print("4. Run ALL (Report)")

    choice = input("Choose algorithm: ")

    if choice == "1":
        env = run_animation(greedy)
        result = compute_metrics(env)

        print("\n===== GREEDY METRICS =====")
        print(result)

    elif choice == "2":
        env = run_animation(fixed)
        result = compute_metrics(env)

        print("\n===== FIXED METRICS =====")
        print(result)

#    elif choice == "3":
#        env = run_animation(smart)
#        result = compute_metrics(env)

#        print("\n===== smart METRICS =====")
#        print(result)

    elif choice == "4":
        run_full_report()

def run_full_report():
    algorithms = {
        "Greedy": greedy,
        "Fixed": fixed,
        # "Smart": smart
    }

    results = {}

    for name, algo in algorithms.items():
        print(f"\nRunning {name}...")

        env = run_animation(algo)
        results[name] = compute_metrics(env)

    print("\n\n================ FULL REPORT ================\n")

    for name, data in results.items():
        print(f"{name.upper()}")
        print(f"Total Wait: {data['total_wait']}")
        print(f"Average Wait: {data['average_wait']}")
        print(f"Cars Passed: {data['cars_passed']}")
        print("------------------------------------")
if __name__ == "__main__": main()