import random

class TrafficEnvironment:
    def __init__(self):
        self.queues = {"N": 0, "S": 0, "E": 0, "W": 0}
        self.total_wait_time = 0
        self.cars_passed = 0

    def generate_cars(self):
        for direction in self.queues:
            self.queues[direction] += random.randint(0, 2)

    def move_cars(self, green_direction):
        # number of cars that can pass in one step
        cars_to_move = min(3, self.queues[green_direction])

        self.queues[green_direction] -= cars_to_move
        self.cars_passed += cars_to_move

    def update_waiting_time(self):
        # every car waiting adds to total wait time
        self.total_wait_time += sum(self.queues.values())