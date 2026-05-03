DIRECTIONS = ["N", "E", "S", "W"]

def fixed_light(queues, time):
    index = (time // 10) % 4  # change every 10 steps
    return DIRECTIONS[index]