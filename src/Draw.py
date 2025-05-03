import math
from OpenGL.GL import *
from OpenGL.GLU import *

# Cell states
WALL = 0
PATH = 1

def draw_maze(maze, agent):
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Calculate cell size based on screen dimensions
    cell_width = 2.0 / maze.width
    cell_height = 2.0 / maze.height
    
    for y in range(maze.height):
        for x in range(maze.width):
            # Skip start, end, and agent positions as they'll be colored differently later
            if (x == 0 and y == 0) or (x == maze.width-1 and y == maze.height-1) or (x == agent.x and y == agent.y):
                continue
                
            if maze.grid[y][x] == WALL:
                # Draw wall
                glColor3f(0.2, 0.2, 0.8)  # Blue walls
            else:
                # Draw path
                glColor3f(1.0, 1.0, 1.0)  # White path
            
            # Calculate cell position
            pos_x = -1.0 + x * cell_width
            pos_y = 1.0 - y * cell_height
            
            # Draw cell as a quad
            glBegin(GL_QUADS)
            glVertex2f(pos_x, pos_y)
            glVertex2f(pos_x + cell_width, pos_y)
            glVertex2f(pos_x + cell_width, pos_y - cell_height)
            glVertex2f(pos_x, pos_y - cell_height)
            glEnd()
            
            # Add a small border
            glColor3f(0.0, 0.0, 0.0)  # Black border
            glLineWidth(1.0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(pos_x, pos_y)
            glVertex2f(pos_x + cell_width, pos_y)
            glVertex2f(pos_x + cell_width, pos_y - cell_height)
            glVertex2f(pos_x, pos_y - cell_height)
            glEnd()

def draw_cell(x, y, maze, cell_width, cell_height, agent, color):
    if not (agent.x == x and agent.y == y):
        glColor3f(*color)
        pos_x = -1.0 + x * cell_width
        pos_y = 1.0 - y * cell_height
        glBegin(GL_QUADS)
        glVertex2f(pos_x, pos_y)
        glVertex2f(pos_x + cell_width, pos_y)
        glVertex2f(pos_x + cell_width, pos_y - cell_height)
        glVertex2f(pos_x, pos_y - cell_height)
        glEnd()

def draw_agent(agent, cell_width, cell_height):
    glColor3f(1.0, 1.0, 0.0)
    pos_x = -1.0 + agent.x * cell_width
    pos_y = 1.0 - agent.y * cell_height
    glBegin(GL_QUADS)
    glVertex2f(pos_x, pos_y)
    glVertex2f(pos_x + cell_width, pos_y)
    glVertex2f(pos_x + cell_width, pos_y - cell_height)
    glVertex2f(pos_x, pos_y - cell_height)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(pos_x, pos_y)
    glVertex2f(pos_x + cell_width, pos_y)
    glVertex2f(pos_x + cell_width, pos_y - cell_height)
    glVertex2f(pos_x, pos_y - cell_height)
    glEnd()

def draw_children(maze, agent, cell_width, cell_height):
    for child_x, child_y in agent.child_positions:
        glColor3f(1.0, 0.0, 1.0)  # Pink color for children
        pos_x = -1.0 + child_x * cell_width
        pos_y = 1.0 - child_y * cell_height
        
        glBegin(GL_QUADS)
        glVertex2f(pos_x + cell_width*0.2, pos_y - cell_height*0.2)
        glVertex2f(pos_x + cell_width*0.8, pos_y - cell_height*0.2)
        glVertex2f(pos_x + cell_width*0.8, pos_y - cell_height*0.8)
        glVertex2f(pos_x + cell_width*0.2, pos_y - cell_height*0.8)
        glEnd()
        
def render_scene(maze, agent, has_won, success_message_time, current_time):
    draw_maze(maze, agent)
    cell_width = 2.0 / maze.width
    cell_height = 2.0 / maze.height

    draw_cell(0, 0, maze, cell_width, cell_height, agent, (0.0, 1.0, 0.0))  # Start
    draw_cell(maze.width-1, maze.height-1, maze, cell_width, cell_height, agent, (1.0, 0.0, 0.0))  # End
    draw_children(maze, agent, cell_width, cell_height)  # Draw children
    draw_agent(agent, cell_width, cell_height)

    if has_won and current_time - success_message_time < 2000:
        pulse = (1 + math.sin((current_time - success_message_time) / 100)) / 2
        draw_cell(maze.width-1, maze.height-1, maze, cell_width, cell_height, agent, (pulse, 1.0-pulse, 0.0))
