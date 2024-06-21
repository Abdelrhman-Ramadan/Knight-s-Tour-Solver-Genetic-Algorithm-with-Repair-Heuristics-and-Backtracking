import random
import time
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from GeneticAlgorithms import Genetic
from knightsTourBackTracking_Warnsdorff import KnightsTour
from KN_Backtracking_RandomizedHeuristic import KnightsTour_1
import tkinter as tk
from functools import partial


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Knight's Tour Solver")
        self.root.resizable(True, True)
        self.root.config(background='#d4a276')
        self.root.iconbitmap('chess-game_6466162.ico')
        # self.root.attributes('-fullscreen', True)  # Maximize the window
        self.root.state('zoomed')
        self.knight_label = None
        self.num = 0
        self.after_id = None
        self.after_id_Knight = None
        self.X = 0
        self.Y = 0
        self.GFS = None  # Generation found solution
        self.start_time = None
        self.end_time = None
        # Center the window on the screen
        self.create_main_window()
        self.root.bind('<Escape>', lambda event: self.exit_program())

    def create_main_window(self):
        # Frame for chessboard
        self.chessboard_frame = tk.Frame(self.root)
        self.chessboard_frame.place(x=100, y=150)

        # Frame for buttons and entry
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.place(x=10, y=10)
        self.controls_frame.config(background='#d4a276')

        self.head_label = tk.Label(self.controls_frame, text="Knight's Tour\nSolver", font=('Bahnschrift SemiBold', 18),
                                   fg='#6f4518', bg='#d4a276')
        self.head_label.grid(row=0, column=0, columnspan=4, pady=(20, 30))

        # Label and Entry for user input
        self.info_label = tk.Label(self.controls_frame, text="Enter size of the chessboard:", font=('courier', 15),
                                   fg='#583101', bg='#d4a276')
        self.info_label.grid(row=1, column=0, columnspan=2, pady=(20, 30), padx=(5, 190))

        self.style = ttk.Style()
        self.style.configure('Custom.TEntry', foreground='#051923', font=('Arial', 9),
                             padding=(1, 1))  # Define the custom style
        self.entry = ttk.Entry(self.controls_frame, style='Custom.TEntry')
        self.entry.grid(row=1, column=1, pady=(1, 10), padx=(50, 10))

        # Label and Entry for user input X & Y
        self.info_labelX = tk.Label(self.controls_frame, text="Start X & Y:", font=('courier', 15), fg='#583101',
                                    bg='#d4a276')
        self.info_labelX.grid(row=2, column=0, columnspan=2, pady=(10, 10), padx=(0, 100))
        #
        self.entryX = ttk.Entry(self.controls_frame, style='Custom.TEntry', width=5)
        self.entryX.grid(row=2, column=0, columnspan=2, padx=(100, 0))
        #####################
        self.entryY = ttk.Entry(self.controls_frame, style='Custom.TEntry', width=5)
        self.entryY.grid(row=2, column=1, padx=(0, 100))

        # choose the algorithm label
        self.Note = tk.Label(self.controls_frame, text="Note: If You Not Insert The X & Y Will Start From (0,0)",
                             font=('Bahnschrift SemiBold', 9), fg='#800000', bg='#d4a276')
        self.Note.grid(row=3, column=0, columnspan=4, pady=(0, 0))

        self.choose_label = tk.Label(self.controls_frame, text="Choose Algorithm\nTo Solve",
                                     font=('Bahnschrift SemiBold', 18), fg='#6f4518', bg='#d4a276')
        self.choose_label.grid(row=4, column=0, columnspan=4, pady=(20, 30))

        algorithm_repair = partial(self.run_function, 'repair')
        self.generate_button = tk.Button(self.controls_frame, text="GA With Repair", command=algorithm_repair,
                                         font=('courier', 10), width=33)
        self.generate_button.grid(row=9, column=0, padx=5)

        algorithm_heuristic = partial(self.run_function, 'heuristic')
        self.generate_button2 = tk.Button(self.controls_frame, text="GA With Heuristic", command=algorithm_heuristic,
                                          font=('courier', 10), width=33)
        self.generate_button2.grid(row=9, column=1, padx=5)

        algorithm_warnsdorff = partial(self.run_function, 'warnsdorff')
        self.generate_button3 = tk.Button(self.controls_frame, text="Backtrack With Warnsdorff's Rule",
                                          command=algorithm_warnsdorff, font=('courier', 10), width=33)
        self.generate_button3.grid(row=11, column=0, pady=5, padx=5)

        algorithm_randomized = partial(self.run_function, 'randomized')
        self.generate_button4 = tk.Button(self.controls_frame, text="Backtrack With Randomized",
                                          command=algorithm_randomized, font=('courier', 10), width=33)
        self.generate_button4.grid(row=11, column=1, pady=5, padx=5)

        # Label to display error messages
        self.result_label = tk.Label(self.controls_frame, text="", fg="red", bg='#d4a276', width=44)
        self.result_label.grid(row=8, column=0, pady=3, columnspan=2)

        self.controls_frame.place(relx=0.5, rely=0.35, anchor="center")

        # Initialize knight_label as None
        self.knight_label = None

    def create_chessboard(self):
        try:
            self.N = int(self.entry.get())
            # check if the x and y is empty
            if len(self.entryY.get()) == 0 and len(self.entryX.get()) == 0:
                self.X = 0
                self.Y = 0
            else:
                self.X = int(self.entryX.get())
                self.Y = int(self.entryY.get())
            if self.N < 1 or (self.X < 0 or self.X >= self.N) or (self.Y < 0 or self.Y >= self.N):
                self.N = 0
                raise ValueError("Please enter a positive integer.")

            # Destroy previous chessboard if exists
            self.destroy_chessboard()
            # Create a new chessboard frame
            self.chessboard_frame = tk.Frame(self.root)
            self.chessboard_frame.place(relx=0.5, rely=0.5, anchor="center")
            # to get height and width for screen
            self.square_size_W = (self.root.winfo_screenwidth() - 300) // self.N
            self.square_size_H = (self.root.winfo_screenheight() - 100) // self.N
            # Create a new chessboard dynamic
            for i in range(self.N):
                for j in range(self.N):
                    color = "#f3d5b5" if (i + j) % 2 == 0 else "#583101"
                    square = tk.Frame(self.chessboard_frame, width=self.square_size_W, height=self.square_size_H,
                                      bg=color)
                    square.grid(row=i, column=j)
            generate_button1 = tk.Button(self.root, text="Reset", command=self.restart_program)
            generate_button1.place(x=0, y=0)
            # Create the knight image
            self.create_knight()
        except ValueError as e:
            self.result_label.config(text=str(e))

    def restart_program(self):
        # Destroy the current main window
        self.root.after_cancel(self.after_id)
        self.root.after_cancel(self.after_id_Knight)
        self.root.destroy()
        self.num = 0
        # Create a new main window
        new_gui = GUI()
        new_gui.run()

    # Function to destroy the chessboard
    def destroy_chessboard(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

    def create_knight(self):
        # Create a knight image
        new_width = ((self.root.winfo_screenwidth() - 300) // self.N) - 5
        new_height = ((self.root.winfo_screenheight() - 100) // self.N) - 5
        with Image.open('knight.png') as im:
            # Resize the image
            resized_im = im.resize((new_width, new_height))
            self.knight_image = ImageTk.PhotoImage(resized_im)
        self.knight_label = tk.Label(self.chessboard_frame, image=self.knight_image, bg="#f3d5b5")
        self.knight_label.image = self.knight_image
        self.knight_label.grid(row=0, column=0)

    def move_knight(self, chessboard_frame, row, col):
        # Move the knight image to the new position
        color = "#f3d5b5" if (row + col) % 2 == 0 else "#583101"
        self.knight_label.configure(bg=color)
        self.knight_label.grid(row=row, column=col)
        self.after_id_Knight = self.root.after(583, self.colorthesquare, row, col)

    def colorthesquare(self, row, col):
        color = "#2c6e49"
        new_width = ((self.root.winfo_screenwidth() - 300) // self.N)
        new_height = ((self.root.winfo_screenheight() - 100) // self.N)
        self.num += 1
        self.square = tk.Frame(self.chessboard_frame, width=new_width, height=new_height, bg=color)
        self.square.grid(row=row, column=col)
        font_size = int(min(new_width, new_height) * 0.3)  # Adjust the font size based on the size of the square
        self.number_label = tk.Label(self.chessboard_frame, text=self.num, background=color, font=("Arial", font_size))
        self.number_label.grid(row=row, column=col)

    def animate_path_with_delay(self, chessboard_frame, best_path, index=0):
        if index < len(best_path):
            self.move_knight(self.chessboard_frame, self.best_path[index][0], self.best_path[index][1])
            self.after_id = self.root.after(500, self.animate_path_with_delay, chessboard_frame, self.best_path,
                                            index + 1)

    # run algorithm
    def genetic_with_repair(self):
        self.obj = Genetic(self.N)
        if self.N > 8:
            self.obj.max_generations = 10000
            self.obj.population_size = 500
        self.obj.start_position = (self.X, self.Y)
        self.start_time = time.time()
        result = self.obj.run_genetic_algorithm()
        if result:
            self.best_path = result[3]
            self.end_time = time.time()
            self.GFS = result[1]
            print(self.best_path)
            self.popup_message('GA')
            self.animate_path_with_delay(self.chessboard_frame, self.best_path)
        else:
            self.popup_message_NFS()

    def genetic_with_heuristic(self):
        self.obj = Genetic(self.N)
        if self.N > 8:
            self.obj.max_generations = 10000
            self.obj.population_size = 500
        self.obj.start_position = (self.X, self.Y)
        self.start_time = time.time()
        result = self.obj.run_genetic_algorithm(use_heuristic=True)
        if result:
            self.best_path = self.obj.run_genetic_algorithm(use_heuristic=True)[3]
            self.end_time = time.time()
            self.GFS = self.obj.run_genetic_algorithm(use_heuristic=True)[1]
            print(self.best_path)
            self.popup_message('GA')
            self.animate_path_with_delay(self.chessboard_frame, self.best_path)
        else:
            self.popup_message_NFS()

    def backtrack_with_warnsdorff(self):
        self.obj = KnightsTour(self.N)
        self.start_time = time.time()
        self.obj.solve(self.X, self.Y)
        self.end_time = time.time()
        self.best_path = self.obj.print_solution()
        print(self.best_path)
        self.popup_message("")
        self.animate_path_with_delay(self.chessboard_frame, self.best_path)

    def backtrack_with_randomized(self):
        self.obj = KnightsTour_1(self.N)
        self.start_time = time.time()
        self.obj.solve(self.X, self.Y)
        self.end_time = time.time()
        self.best_path = self.obj.print_solution()
        print(self.best_path)
        self.popup_message("")
        self.animate_path_with_delay(self.chessboard_frame, self.best_path)

    def run_function(self, type):
        self.create_chessboard()
        if (type == 'repair'):
            self.genetic_with_repair()
        elif (type == 'heuristic'):
            self.genetic_with_heuristic()
        elif (type == 'warnsdorff'):
            self.backtrack_with_warnsdorff()
        elif (type == 'randomized'):
            self.backtrack_with_randomized()

    def popup_message(self, type=""):
        if type == 'GA':
            messagebox.showinfo("Tour information", f"The Solution Found in Number Generation: {self.GFS}"
                                         f"\nTime elapsed To Find Solution: {(self.end_time - self.start_time)} Second")
        else:
            messagebox.showinfo("Tour information",
                                f"Time elapsed To Find Solution: {(self.end_time - self.start_time)} Second")

    def popup_message_NFS(self):
        messagebox.showwarning("Error", f"Not Found Solution")
        self.root.destroy()
        self.num = 0
        # Create a new main window
        new_gui = GUI()
        new_gui.run()

    def exit_program(self):
        # self.root.destroy()
        self.root.iconify()

    def run(self):
        self.root.mainloop()


# Create an instance of the GUI class and run the GUI
gui = GUI()
gui.run()
