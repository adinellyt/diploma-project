class Grid:
    source_x = 0
    source_y = 0
    start_source_x = 0
    start_source_y = 0
    destination_x = 0
    destination_y = 0
    grid = [
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*'],
        ['*', '*', '*', '*', '*', '*', '*', '*']
    ]

    def __init__(self, source_x, source_y, destination_x, destination_y):
        self.source_x = source_x
        self.source_y = source_y
        self.start_source_x = source_x
        self.start_source_y = source_y
        self.destination_x = destination_x
        self.destination_y = destination_y

    def set_grid(self):
        self.grid[self.source_y][self.source_x] = 's'
        self.grid[self.destination_y][self.destination_x] = 'd'

    def set_obstructing_grid(self, x, y):
        self.grid[y][x] = '0'

    def print_grid(self):
        for i in self.grid:
            print(i)

    def update_source(self):
        self.grid[self.start_source_y][self.start_source_x] = '*'
        self.grid[self.source_y][self.source_x] = 's'
