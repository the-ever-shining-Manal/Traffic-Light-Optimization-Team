last_direction = None


class SmartAlgorithm:
    def __init__(self):
        global last_direction
        last_direction = None

    def __call__(self, queues, time):
        global last_direction
        score = {}
        for d in queues:
            queue_len = len(queues[d])
            # cars are dicts: {"arrival": step} — compute wait correctly
            total_wait = sum(time - car["arrival"] for car in queues[d])

            score[d] = queue_len + 0.5 * total_wait

            # bonus to avoid unnecessary direction flips
            if d == last_direction:
                score[d] += 2

            # urgency boost when someone has been waiting a long time
            if total_wait > 20:
                score[d] += 10

        best = max(score, key=score.get)
        last_direction = best
        return best


smart_algorithm = SmartAlgorithm()