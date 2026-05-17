from simulation.environment import DIRECTIONS


def fixed_light(queues:None, time: int):
    """Baseline: rotate through directions every 10 steps."""
    index = (time // 10) % len(DIRECTIONS)
    return DIRECTIONS[index]