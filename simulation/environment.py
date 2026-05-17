import random

DIRECTIONS = ["N", "S", "E", "W"]

class Environment:
    def __init__(self):
        self.queues = {d: [] for d in DIRECTIONS}
        self.total_wait = 0
        self.cars_passed = 0
        self.time = 0

    def generate_cars(self):
        for d in DIRECTIONS:
            if random.random() < 0.3:
                self.queues[d].append({"arrival": self.time})

    def move_cars(self, green):
        cars_to_pass = min(1, len(self.queues[green]))

        for _ in range(cars_to_pass):
            car = self.queues[green].pop(0)

            wait_time = self.time - car["arrival"]

            self.total_wait += wait_time
            self.cars_passed += 1

    def pre_step(self, algorithm_func):
        self.generate_cars()
        self.current_green = algorithm_func(self.queues, self.time)
        return self.current_green

    def post_step(self):
        self.move_cars(self.current_green)
        self.time += 1

    def step(self, algorithm_func):
        green = self.pre_step(algorithm_func)
        self.post_step()
        return green


