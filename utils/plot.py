import matplotlib.pyplot as plt

def plot_results(results):
    algorithms = list(results.keys())

    total_wait = [results[a]["total_wait"] for a in algorithms]
    avg_wait = [results[a]["average_wait"] for a in algorithms]
    cars_passed = [results[a]["cars_passed"] for a in algorithms]

    # 1. Average Wait
    plt.figure()
    plt.bar(algorithms, avg_wait)
    plt.title("Average Waiting Time vs Algorithm")
    plt.ylabel("Time")
    plt.show()

    # 2. Total Wait
    plt.figure()
    plt.bar(algorithms, total_wait)
    plt.title("Total Waiting Time vs Algorithm")
    plt.ylabel("Time")
    plt.show()

    # 3. Cars Passed
    plt.figure()
    plt.bar(algorithms, cars_passed)
    plt.title("Cars Passed vs Algorithm")
    plt.ylabel("Cars")
    plt.show()