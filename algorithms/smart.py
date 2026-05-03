last_direction = None


def smart_algorithm(queues, time):
    global last_direction

    score = {}

    for d in queues:
        queue_len = len(queues[d])

        try:
            total_wait = sum(car.wait_time for car in queues[d])
        except:
            total_wait = 0

        # core logic
        score[d] = queue_len + 0.5 * total_wait

        # fairness
        if d == last_direction:
            score[d] -= 2

        # anti-starvation
        if total_wait > 20:
            score[d] += 10

    best = max(score, key=score.get)
    last_direction = best

    return best