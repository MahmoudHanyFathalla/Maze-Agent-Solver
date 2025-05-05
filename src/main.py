import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Maze import Maze
from Agent import Agent
from Draw import *
from setup import *
from control_window import ControlPanel

MAZE_WIDTH = 10
MAZE_HEIGHT = 10


def game_loop(maze, agent, control_panel):
    move_delay = 200
    last_move_time = pygame.time.get_ticks()
    success_message_time = 0
    has_won = False
    total_moves = blocked_moves = non_blocked_moves = 0
    key_states = {"up": False, "down": False, "left": False, "right": False}
    running = True

    while running:
        current_time = pygame.time.get_ticks()
        events = handle_events()

        control_panel.update()

        if events["quit"]:
            running = False
            continue

        if events["solution"]:
            agent.get_solution_paths(maze)
            continue

        if events["paths"]:
            agent.get_all_paths(maze)
            continue

        if events["restart"]:
            maze.generate_random_maze()
            agent = Agent(0, 0)
            agent.generate_children(maze)
            has_won = False
            total_moves = blocked_moves = non_blocked_moves = 0
            print("New maze generated! Rescue all children and navigate to the exit!")
            print("Moves: 0, Blocked: 0, Children remaining: 3")
            continue

        for key in ["up", "down", "left", "right"]:
            if events[key]:
                key_states[key] = True

        if current_time - last_move_time > move_delay:
            moved, was_blocked = process_movement(agent, maze, key_states)
            if moved or was_blocked:
                total_moves += 1
                if moved:
                    non_blocked_moves += 1
                else:
                    blocked_moves += 1
                last_move_time = current_time
                print(f"Total Moves: {total_moves}, Not Blocked: {non_blocked_moves}, Blocked: {blocked_moves}")

            if agent.check_goal(maze) and not has_won:
                print("Congratulations! All children rescued and exit reached!")
                print(f"Final stats - Moves: {total_moves}, Not Blocked: {non_blocked_moves}, Blocked: {blocked_moves}")
                success_message_time = current_time
                has_won = True

        render_scene(maze, agent, has_won, success_message_time, current_time)
        pygame.display.flip()
        pygame.time.wait(10)

def main():
    setup_pygame()
    setup_opengl()
    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
    agent = Agent(0, 0)
    agent.generate_children(maze)
    control_panel = ControlPanel(maze, agent)
    try:
            game_loop(maze, agent, control_panel)
    finally:
            control_panel.cleanup()
            pygame.quit()

if __name__ == "__main__":
    main()
