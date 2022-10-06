class QItem:
    def __init__(self, row, col, dist, path):
        self.row = row
        self.col = col
        self.dist = dist
        self.path = path

    def __repr__(self):
        return f"QItem({self.row}, {self.col}, {self.dist}, {self.path})"


def min_distance(grid):
    source = QItem(0, 0, 0, "")

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 's':
                source.row = row
                source.col = col
                break

    visited = [[False for _ in range(len(grid[0]))]
               for _ in range(len(grid))]

    queue = [source]
    visited[source.row][source.col] = True

    while len(queue) != 0:
        source = queue.pop(0)

        if grid[source.row][source.col] == 'd':
            return source.path

        # moving up
        if is_valid(source.row - 1, source.col, grid, visited):
            queue.append(QItem(source.row - 1, source.col, source.dist + 1, source.path + "U"))
            visited[source.row - 1][source.col] = True

        # moving down
        if is_valid(source.row + 1, source.col, grid, visited):
            queue.append(QItem(source.row + 1, source.col, source.dist + 1, source.path + "D"))
            visited[source.row + 1][source.col] = True

        # moving left
        if is_valid(source.row, source.col - 1, grid, visited):
            queue.append(QItem(source.row, source.col - 1, source.dist + 1, source.path + "L"))
            visited[source.row][source.col - 1] = True

        # moving right
        if is_valid(source.row, source.col + 1, grid, visited):
            queue.append(QItem(source.row, source.col + 1, source.dist + 1, source.path + "R"))
            visited[source.row][source.col + 1] = True

    return ""


def is_valid(x, y, grid, visited):
    if ((x >= 0 and y >= 0) and
            (x < len(grid) and y < len(grid[0])) and
            (grid[x][y] != '0') and (visited[x][y] is False)):
        return True
    return False
