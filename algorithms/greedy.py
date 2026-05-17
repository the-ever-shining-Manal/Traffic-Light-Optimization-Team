import random

last_green = None

def greedy_light(queues, time: int) -> str:
    """Selects the direction with the most cars waiting.
    Ties broken by keeping the current light to avoid rapid flickering.
    If another lane becomes strictly longer, it switches immediately."""
    global last_green
    
    max_len = max(len(queues[d]) for d in queues)
    candidates = [d for d in queues if len(queues[d]) == max_len]
    
    if last_green in candidates:
        return last_green
        
    last_green = random.choice(candidates)
    return last_green
