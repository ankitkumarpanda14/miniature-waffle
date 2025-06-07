class Environment:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.obstacles = set()
        self.dock = (width - 1, height - 1)

    def add_obstacle(self, x, y):
        self.obstacles.add((x, y))

    def set_dock(self, pos):
        self.dock = pos

    def is_obstacle(self, pos):
        return pos in self.obstacles
