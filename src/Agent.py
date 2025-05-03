# Cell states
WALL = 0
PATH = 1
CHILD = 3
ALL_PATHS_MAX_NUMBER = 100
SOLUTION_PATHS_MAX_NUMBER = 50

class Agent:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
   
    def generate_children(self, maze, num_children=CHILD):
        import random
        self.child_positions = []
        while len(self.child_positions) < num_children:
            x = random.randint(0, maze.width-1)
            y = random.randint(0, maze.height-1)
            # Don't place children on walls, start position, end position or existing child positions
            if (maze.grid[y][x] == PATH and 
                (x, y) != (0, 0) and 
                (x, y) != (maze.width-1, maze.height-1) and
                (x, y) not in self.child_positions):
                self.child_positions.append((x, y))
    
    def manhattan_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)            

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check if the new position is valid and not a wall
        if maze.is_valid(new_x, new_y) and maze.grid[new_y][new_x] == PATH:
            self.x = new_x
            self.y = new_y
            print(f"Agent moved to ({self.x}, {self.y})")

            # Check if we reached a child position
            current_pos = (self.x, self.y)
            if current_pos in self.child_positions:
                self.child_positions.remove(current_pos)
                print(f"Child rescued! Remaining children: {len(self.child_positions)}")
            
            # Print Manhattan distance to remaining children
            for i, (child_x, child_y) in enumerate(self.child_positions):
                distance = self.manhattan_distance(self.x, self.y, child_x, child_y)
                print(f"Distance to Child {i+1}: {distance}")

            return True
        else:
            # Only print the blocked message once per attempt
            direction_name = ""
            if dx == 0 and dy == -1:
                direction_name = "UP"
            elif dx == 0 and dy == 1:
                direction_name = "DOWN"
            elif dx == -1 and dy == 0:
                direction_name = "LEFT"
            elif dx == 1 and dy == 0:
                direction_name = "RIGHT"
                
            print(f"Blocked: Cannot move {direction_name}!")
            return False
            
    
    def get_solution_paths(self, maze, max_paths=SOLUTION_PATHS_MAX_NUMBER, max_samples=5):
        for i, (child_x, child_y) in enumerate(self.child_positions):
            print(f"\nChild {i+1} at ({child_x}, {child_y}):")
            # BFS to find shortest paths only, up to max_paths
            reachable_paths = []
            queue = [[(self.x, self.y)]]

            while queue and len(reachable_paths) < max_paths:
                path = queue.pop(0)
                current = path[-1]

                if current == (child_x, child_y):
                    reachable_paths.append(path)
                    continue

                for dx_step, dy_step in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    next_x = current[0] + dx_step
                    next_y = current[1] + dy_step

                    if (maze.is_valid(next_x, next_y) and
                        maze.grid[next_y][next_x] == PATH and
                        (next_x, next_y) not in path):
                        queue.append(path + [(next_x, next_y)])

            print(f"  Actually reachable paths (limited to {max_paths}): {len(reachable_paths)}")

            if reachable_paths:
                print(f"  Example reachable paths (up to {max_samples} shown):")
                for j, path in enumerate(reachable_paths[:max_samples], 1):
                    print(f"    Path {j}: " + " -> ".join(f"({x},{y})" for x, y in path))
                if len(reachable_paths) > max_samples:
                    print(f"    ... and {len(reachable_paths) - max_samples} more")
            else:
                print("  No valid paths found to this child.")

        return len(self.child_positions) > 0


    def get_all_paths(self, maze, max_paths=ALL_PATHS_MAX_NUMBER, max_samples=5):
        from collections import deque

        def is_valid_pos(x, y):
            return 0 <= x < maze.width and 0 <= y < maze.height

        for i, (child_x, child_y) in enumerate(self.child_positions):
            print(f"\nChild {i+1} at ({child_x}, {child_y}):")

            queue = deque([[(self.x, self.y)]])
            all_shortest_paths = []
            visited = set()

            shortest_length = None

            while queue and len(all_shortest_paths) < max_paths:
                path = queue.popleft()
                current = path[-1]

                if shortest_length is not None and len(path) > shortest_length:
                    continue  # Don't consider longer paths

                if current == (child_x, child_y):
                    if shortest_length is None:
                        shortest_length = len(path)
                    all_shortest_paths.append(path)
                    continue

                for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                    nx, ny = current[0] + dx, current[1] + dy
                    next_pos = (nx, ny)

                    if (is_valid_pos(nx, ny) and
                        next_pos not in path):  # prevent cycles
                        queue.append(path + [next_pos])

            print(f"  Total shortest paths found: {len(all_shortest_paths)}")
            print(f"  Showing up to {min(max_samples, len(all_shortest_paths))} example paths:")

            for j, path in enumerate(all_shortest_paths[:max_samples], 1):
                print(f"    Path {j}: " + " -> ".join(f"({x},{y})" for x, y in path))

            if len(all_shortest_paths) > max_samples:
                print(f"    ... and {len(all_shortest_paths) - max_samples} more")

    def check_goal(self, maze):
        # return self.x == maze.width-1 and self.y == maze.height-1
        return (self.x == maze.width-1 and self.y == maze.height-1 and len(self.child_positions) == 0)
