class Robot:
    def __init__(self, environment):
        self.env = environment
        self.position = (0, 0)
        self.direction = 'EAST'
        self.battery = 100
        self.plan = []
        self.plan_step = 0
    
    def set_plan(self, action_list):
        self.plan = action_list
        self.plan_step = 0
    
    def execute_next_action(self):
        if self.plan_step >= len(self.plan):
            return
        
        action = self.plan[self.plan_step]
        if action == "move_forward":
            self.move_forward()
        elif action == "turn_left":
            self.turn_left()
        elif action == "turn_right":
            self.turn_right()
        elif action == "dock":
            print("Docking...")
        self.plan_step += 1

    def move_forward(self):
        x, y = self.position
        dx, dy = 0, 0
        if self.direction == 'NORTH':
            dy = -1
        elif self.direction == 'SOUTH':
            dy = 1
        elif self.direction == 'EAST':
            dx = 1
        elif self.direction == 'WEST':
            dx = -1

        new_pos = (x + dx, y + dy)
        if (0 <= new_pos[0] < self.env.width and 
            0 <= new_pos[1] < self.env.height and
            not self.env.is_obstacle(new_pos)):
            self.position = new_pos
            self.battery = max(0, self.battery - 1)

    def turn_left(self):
        directions = ['NORTH', 'WEST', 'SOUTH', 'EAST']
        idx = directions.index(self.direction)
        self.direction = directions[(idx + 1) % 4]

    def turn_right(self):
        directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']
        idx = directions.index(self.direction)
        self.direction = directions[(idx + 1) % 4]
