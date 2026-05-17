def compute_metrics(env):
    # Calculate wait time of cars that haven't passed yet
    pending_wait = 0
    pending_cars = 0
    for d in env.queues:
        for car in env.queues[d]:
            pending_wait += (env.time - car["arrival"])
            pending_cars += 1

    true_total_wait = env.total_wait + pending_wait
    true_total_cars = env.cars_passed + pending_cars

    avg_wait = true_total_wait / true_total_cars if true_total_cars > 0 else 0
    throughput = env.cars_passed / env.time if env.time > 0 else 0

    return {
        "total_wait": true_total_wait,
        "average_wait": avg_wait,
        "cars_passed": env.cars_passed,
        "throughput": throughput
    }