from bfs_algoritm import min_distance


def return_robot_path(grid, current_direction="up"):
    path = min_distance(grid)
    robot_path = []
    direction_map = {
        "UR": ["right"],
        "UL": ["left"],
        "UD": ["left", "left"],
        "LU": ["right"],
        "LD": ["left"],
        "LR": ["left", "left"],
        "RU": ["left"],
        "RD": ["right"],
        "RL": ["left", "left"],
        "DR": ["left"],
        "DL": ["right"],
        "DU": ["left", "left"],
    }

    current_direction_map = {
        'up': 'U',
        'down': 'D',
        'left': 'L',
        'right': 'R'
    }
    current_direction = current_direction_map[current_direction]

    for direction in path:
        if direction != current_direction:
            robot_path = robot_path + direction_map[current_direction+direction]
            current_direction = direction

        robot_path.append("forward")

    return robot_path
