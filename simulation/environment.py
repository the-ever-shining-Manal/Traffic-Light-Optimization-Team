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
        if self.queues[green]:
            car = self.queues[green].pop(0)

            wait_time = self.time - car["arrival"]

            self.total_wait += wait_time
            self.cars_passed += 1

    def step(self, algorithm_func):
        self.generate_cars()

        green = algorithm_func(self.queues, self.time)

        self.move_cars(green)

        self.time += 1