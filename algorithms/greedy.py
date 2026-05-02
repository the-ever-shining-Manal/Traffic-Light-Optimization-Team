def greedy_light(queues):
    # Selects direction with the highest number of cars
    return max(queues, key=queues.get)