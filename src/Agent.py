# Cell states
WALL = 0
PATH = 1
CHILD = 3

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
            
    def check_goal(self, maze):
       # return self.x == maze.width-1 and self.y == maze.height-1
        return (self.x == maze.width-1 and self.y == maze.height-1 and len(self.child_positions) == 0)
