def greedy_light(queues, time):
    # Selects direction with the highest number of cars
    return max(queues, key=lambda d: len(queues[d]))