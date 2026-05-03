def compute_metrics(env):
    avg_wait = env.total_wait / env.cars_passed if env.cars_passed > 0 else 0

    return {
        "total_wait": env.total_wait,
        "average_wait": avg_wait,
        "cars_passed": env.cars_passed
    }