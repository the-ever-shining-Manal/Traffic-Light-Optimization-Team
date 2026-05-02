from simulation.environment import TrafficEnvironment
from algorithms.greedy import greedy_light

def run_simulation(steps=100):
    env = TrafficEnvironment()

    for t in range(steps):
        env.generate_cars()

        green = greedy_light(env.queues)

        env.move_cars(green)
        env.update_waiting_time()

    avg_wait = env.total_wait_time / (env.cars_passed + 1)

    return {
        "total_wait_time": env.total_wait_time,
        "cars_passed": env.cars_passed,
        "average_wait_time": avg_wait
    }

if __name__ == "__main__":
    result = run_simulation()
    print(result)