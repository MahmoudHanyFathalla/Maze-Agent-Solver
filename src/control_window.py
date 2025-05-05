import tkinter as tk

class ControlPanel:
    def __init__(self, maze, agent):
        self.root = tk.Tk()
        self.root.title("Maze Control Panel")
        self.root.geometry("200x150")  # Set window size
        self.maze = maze
        self.agent = agent

        # Add size controls
        size_frame = tk.Frame(self.root)
        size_frame.pack(pady=5)
        
        tk.Label(size_frame, text="Width:").pack(side=tk.LEFT)
        self.width_var = tk.StringVar(value=str(maze.width))
        self.width_entry = tk.Entry(size_frame, textvariable=self.width_var, width=5)
        self.width_entry.pack(side=tk.LEFT, padx=2)
        
        tk.Label(size_frame, text="Height:").pack(side=tk.LEFT)
        self.height_var = tk.StringVar(value=str(maze.height))
        self.height_entry = tk.Entry(size_frame, textvariable=self.height_var, width=5)
        self.height_entry.pack(side=tk.LEFT, padx=2)
        
        # Create buttons
        self.size_btn = tk.Button(
            self.root,
            text="Generate Maze",
            command=self.apply_size
        )
        self.size_btn.pack(pady=5)
        
        self.analyze_btn = tk.Button(
            self.root, 
            text="Get Paths", 
            command=self.show_paths
        )
        self.analyze_btn.pack(pady=5)
        
        self.show_solution_btn = tk.Button(
            self.root, 
            text="Show Solutions", 
            command=self.show_solutions
        )
        self.show_solution_btn.pack(pady=5)
        
        # Update the window
        self.root.update()

    def update(self):
        self.root.update_idletasks()
        self.root.update()
        
    def show_paths(self):
        self.agent.get_all_paths(self.maze)
        
    def new_maze(self):
        self.maze.generate_random_maze()
        self.agent.x = 0
        self.agent.y = 0
        self.agent.generate_children(self.maze)
        
    def show_solutions(self):
        self.agent.get_solution_paths(self.maze)

    def cleanup(self):
        if self.root:
            self.root.destroy()
    
    def apply_size(self):
        try:
            new_width = max(3, min(300, int(self.width_var.get())))
            new_height = max(3, min(300, int(self.height_var.get())))
            
            # Update maze size
            self.maze.width = new_width
            self.maze.height = new_height
            
            # Generate new maze with new size
            self.maze.generate_random_maze()
            
            # Reset agent and children
            self.agent.x = 0
            self.agent.y = 0
            self.agent.generate_children(self.maze)
            
            # Update entry fields with clamped values
            self.width_var.set(str(new_width))
            self.height_var.set(str(new_height))
            
            print(f"New maze generated with size {new_width}x{new_height}")
            
        except ValueError:
            print("Please enter valid numbers for width and height")
            # Reset to current size
            self.width_var.set(str(self.maze.width))
            self.height_var.set(str(self.maze.height))