import random

WALL = 0
PATH = 1

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Cardinal
DIAGONALS = [(-1, -1), (1, -1), (1, 1), (-1, 1)]  # Diagonal

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[WALL for _ in range(width)] for _ in range(height)]
        self.generate()

    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_valid_maze(self):
        if self.grid[0][0] != PATH or self.grid[self.height-1][self.width-1] != PATH:
            return False
        visited = [[False]*self.width for _ in range(self.height)]
        queue = [(0, 0)]
        visited[0][0] = True
        while queue:
            x, y = queue.pop(0)
            if (x, y) == (self.width-1, self.height-1):
                return True
            for dx, dy in DIRECTIONS + DIAGONALS:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny) and self.grid[ny][nx] == PATH and not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((nx, ny))
        return False

    def generate_random_maze(self):
        self.grid = [[WALL for _ in range(self.width)] for _ in range(self.height)]
        self.generate()

    def generate(self):
        start_x, start_y = 0, 0
        self.grid[start_y][start_x] = PATH
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx*2, y + dy*2
                if self.is_valid(nx, ny) and self.grid[ny][nx] == WALL:
                    neighbors.append((nx, ny, dx, dy))
            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                self.grid[y + dy][x + dx] = PATH
                self.grid[ny][nx] = PATH
                stack.append((nx, ny))
            else:
                stack.pop()

        # Add occasional diagonal paths
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                if self.grid[y][x] == WALL and random.random() < 0.05:
                    dx, dy = random.choice(DIAGONALS)
                    if self.is_valid(x+dx, y+dy) and self.grid[y+dy][x+dx] == PATH:
                        self.grid[y][x] = PATH

        # Add cycles by knocking down some walls
        for _ in range((self.width * self.height) // 20):  # tune number of cycles
            x = random.randint(1, self.width-2)
            y = random.randint(1, self.height-2)
            if self.grid[y][x] == WALL:
                neighbors = sum(
                    1 for dx, dy in DIRECTIONS if self.grid[y+dy][x+dx] == PATH
                )
                if neighbors >= 2:
                    self.grid[y][x] = PATH

        # Ensure the end is reachable
        self.grid[self.height-1][self.width-1] = PATH
        if not any(self.grid[self.height-2][self.width-1:self.width]) and self.width > 1:
            self.grid[self.height-2][self.width-1] = PATH
        if not any(row[self.width-2] for row in self.grid[-2:]) and self.height > 1:
            self.grid[self.height-1][self.width-2] = PATH

        while not self.is_valid_maze():
            self.generate()
