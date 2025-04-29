import pygame
import tkinter as tk
from tkinter import messagebox, filedialog
import sys
from datetime import datetime
import os
import time
import threading
import keyboard
from threading import Event
pygame.init()

px = 0
py = 0
ox = [0] * 30  # Default size: 30 elements
oy = [0] * 30

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
ORANGE = (255,128,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

GRID_SIZE = 24
CELL_SIZE = 20  # Size of each cell in pixels
GRID = [[(255, 255, 255) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Default color: white

WINDOW_WIDTH = GRID_SIZE * CELL_SIZE  # The width matches the grid width
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + 100  # Add 100px for buttons

def update_grid(x, y, rgbcolor):
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:  # Ensure x and y are within bounds
        GRID[y][x] = rgbcolor  # Update the grid with the new color

def render_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, GRID[row][col],
                             pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0),
                             pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def clear_grid():
    global GRID
    GRID = [[(255, 255, 255) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def fill_grid(rgbcolor):
    global GRID
    GRID = [[rgbcolor for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

code = ""
run = False
duration = 1  # Default duration for each execution (seconds)
loops = 1  # Default number of loops

class Window:
    def __init__(self):
        global px, py, ox, oy, duration, loops
        root = tk.Tk()
        root.title("Code Input")
        
        # Code Input Textbox
        tk.Label(root, text="Enter Code:").pack()
        text_box = tk.Text(root, height=5, width=40)
        text_box.pack()

        # Duration Textbox
        tk.Label(root, text="Enter Duration (Seconds):").pack()
        duration_entry = tk.Entry(root, width=20)
        duration_entry.pack()
        duration_entry.insert(0, str(duration))

        # Loops Textbox
        tk.Label(root, text="Enter Number of Loops:").pack()
        loop_entry = tk.Entry(root, width=20)
        loop_entry.pack()
        loop_entry.insert(0, str(loops))

        # px Textbox
        tk.Label(root, text="Enter px Value:").pack()
        px_entry = tk.Entry(root, width=20)
        px_entry.pack()
        px_entry.insert(0, str(px))

        # py Textbox
        tk.Label(root, text="Enter py Value:").pack()
        py_entry = tk.Entry(root, width=20)
        py_entry.pack()
        py_entry.insert(0, str(py))

        # ox Array Textbox
        tk.Label(root, text="Enter ox Array (comma-separated):").pack()
        ox_textbox = tk.Text(root, height=5, width=40)
        ox_textbox.pack()
        ox_textbox.insert("1.0", ",".join(map(str, ox)))

        # oy Array Textbox
        tk.Label(root, text="Enter oy Array (comma-separated):").pack()
        oy_textbox = tk.Text(root, height=5, width=40)
        oy_textbox.pack()
        oy_textbox.insert("1.0", ",".join(map(str, oy)))

        # Save Button
        tk.Button(root, text="Save", command=lambda: save_variables(text_box, duration_entry, loop_entry, px_entry, py_entry, ox_textbox, oy_textbox)).pack()

        # Save As Button
        tk.Button(root, text="Save As", command=lambda: save_variables_as(text_box, duration_entry, loop_entry, px_entry, py_entry, ox_textbox, oy_textbox)).pack()

        # Load Button
        tk.Button(root, text="Load", command=lambda: load_variables(text_box, duration_entry, loop_entry, px_entry, py_entry, ox_textbox, oy_textbox)).pack()

        def on_window_open():
            text_box.insert(tk.END, code)
        
        root.after(100, on_window_open)

        def disable_close():
            pass

        def ccode():
            global code, duration, loops, px, py, ox, oy
            code = text_box.get("1.0", "end").strip()
            try:
                duration = float(duration_entry.get())
                loops = int(loop_entry.get())
                px = int(px_entry.get())
                py = int(py_entry.get())
                ox = list(map(int, ox_textbox.get("1.0", "end").strip().split(",")))
                oy = list(map(int, oy_textbox.get("1.0", "end").strip().split(",")))
            except ValueError:
                messagebox.showinfo("Invalid Input", "Please enter valid integers and comma-separated values.")
                duration = 1
                loops = 1
                px = 0
                py = 0
                ox = [0] * 30
                oy = [0] * 30

        def code_toclose():
            ccode()
            root.destroy()
        
        def button_callback():
            ccode()
            messagebox.showinfo("Hello and attention", "Settings saved and Code Updated!")

        root.protocol("WM_DELETE_WINDOW", code_toclose)
        root.mainloop()

# Functions to save/load variables
def save_variables(text_box, duration_entry, loop_entry, px_entry, py_entry, ox_textbox, oy_textbox):
    data = {
        "code": text_box.get("1.0", "end").strip(),
        #"duration": duration_entry.get().strip(),
        "duration": duration_entry.get().strip(),
        "loops": loop_entry.get().strip(),
        "px": px_entry.get().strip(),
        "py": py_entry.get().strip(),
        "ox": ox_textbox.get("1.0", "end").strip(),
        "oy": oy_textbox.get("1.0", "end").strip()
    }
    with open("variables.txt", "w") as file:
        file.write(str(data))
    messagebox.showinfo("Save", "Variables saved successfully.")

def save_variables_as(text_box, duration_entry, loop_entry, px_entry, py_entry, ox_textbox, oy_textbox):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        data = {
            "code": text_box.get("1.0", "end").strip(),
            "duration": duration_entry.get().strip(),
            "loops": loop_entry.get().strip(),
            "px": px_entry.get().strip(),
            "py": py_entry.get().strip(),
            "ox": ox_textbox.get("1.0", "end").strip(),
            "oy": oy_textbox.get("1.0", "end").strip()
        }
        with open(file_path, "w") as file:
            file.write(str(data))
        messagebox.showinfo("Save As", "Variables saved successfully.")

def load_variables(text_box, duration_entry, loop_entry, px_entry, py_entry, ox_textbox, oy_textbox):
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            data = eval(file.read())  # Note: Ensure file integrity before using eval
        text_box.delete("1.0", tk.END)
        text_box.insert("1.0", data["code"])
        duration_entry.delete(0, tk.END)
        #duration_entry.insert(0, data["duration"])
        duration_entry.insert(0, data["duration"])
        loop_entry.delete(0, tk.END)
        loop_entry.insert(0, data["loops"])
        px_entry.delete(0, tk.END)
        px_entry.insert(0, data["px"])
        py_entry.delete(0, tk.END)
        py_entry.insert(0, data["py"])
        ox_textbox.delete("1.0", tk.END)
        ox_textbox.insert("1.0", data["ox"])
        oy_textbox.delete("1.0", tk.END)
        oy_textbox.insert("1.0", data["oy"])
        messagebox.showinfo("Load", "Variables loaded successfully.")

# Remaining code is unchanged (run_code, stop_function, Pygame loop)

stop_event = Event()  # Create an event to manage stopping the loop

def stop_function(stop_window=None):
    global run
    run = False
    stop_event.set()  # Signal to stop the loop
    clear_grid()  # Clear the grid back to its default state
    if stop_window:
        stop_window.destroy()  # Close the stop window when "Stop" is clicked

def open_stop_window():
    stop_window = tk.Tk()
    stop_window.title("Stop Execution")
    tk.Button(stop_window, text="Stop", command=lambda: stop_function(stop_window)).pack()
    return stop_window

def run_code():
    global run, code, duration, loops
    run = True  # Allow the code to execute
    stop_event.clear()  # Reset the stop event
    stop_window = open_stop_window()  # Open the Stop Window and get its reference

    try:
        for i in range(loops):
            if stop_event.is_set():  # Check if the stop event has been triggered
                break
            if code.strip():  # Execute code only if it's not empty
                try:
                    exec(code)
                except Exception as e:
                    messagebox.showinfo("Execution Error", f"An error occurred on iteration {i + 1}: {str(e)}")
                    break
            else:
                messagebox.showinfo("Error", "Code is blank. Please enter valid Python code.")
                break
            time.sleep(duration)  # Wait for the specified duration before the next loop
    except Exception as e:
        messagebox.showinfo("Error", f"Unexpected error: {str(e)}")
    finally:
        run = False
        stop_event.set()  # Ensure the stop event is set
        stop_function(stop_window)  # Automatically close the stop window when loops finish

#screen = pygame.display.set_mode((400, 300))
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simple-8")

img = pygame.image.load('./assets/S8_logo.png')
pygame.display.set_icon(img)

color = (255, 255, 255)
screen.fill(color)
pygame.display.flip()

clock = pygame.time.Clock()
#rect = pygame.Rect(300, 100, 100, 50)
#rect2 = pygame.Rect(300, 150, 100, 50)
#rect3 = pygame.Rect(300, 200, 100, 50)
#rect4 = pygame.Rect(300, 250, 100, 50)
rect = pygame.Rect(20, GRID_SIZE * CELL_SIZE + 10, 100, 30)  # Offset by grid height
rect2 = pygame.Rect(140, GRID_SIZE * CELL_SIZE + 10, 100, 30)
rect3 = pygame.Rect(260, GRID_SIZE * CELL_SIZE + 10, 100, 30)
rect4 = pygame.Rect(380, GRID_SIZE * CELL_SIZE + 10, 100, 30)
font = pygame.font.SysFont("Arial", 20)
click = font.render("Click me", 1, (0, 0, 0))
click2 = font.render("View Code", 1, (0, 0, 0))
click3 = font.render("Run", 1, (0, 0, 0))
click4 = font.render("Stop", 1, (0, 0, 0))

while True:
    screen.fill((255, 255, 255))  # Fill the screen with white
    render_grid()  # Render the grid
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            clear_grid()  # Reset the grid
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if rect.collidepoint(pygame.mouse.get_pos()):
                Window()
            if rect2.collidepoint(pygame.mouse.get_pos()):
                time1 = datetime.now().strftime("%H-%M-%S-%f")
                file_path = os.path.join(os.getenv("TEMP"), f"temp_{time1}.txt")

                with open(str(file_path), "w") as file:
                    file.write(str(code))

                os.system(f"notepad.exe {file_path}")
            if rect3.collidepoint(pygame.mouse.get_pos()):
                threading.Thread(target=run_code).start()
            if rect4.collidepoint(pygame.mouse.get_pos()):
                stop_function()
    pygame.draw.rect(screen, (255, 255, 255), rect)
    screen.blit(click, rect)
    pygame.display.flip()
    clock.tick(60)
    pygame.draw.rect(screen, (255, 255, 255), rect2)
    screen.blit(click2, rect2)
    pygame.display.flip()
    clock.tick(60)
    pygame.draw.rect(screen, (255, 255, 255), rect3)
    screen.blit(click3, rect3)
    pygame.display.flip()
    clock.tick(60)
    pygame.draw.rect(screen, (255, 255, 255), rect4)
    screen.blit(click4, rect4)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
