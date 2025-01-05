import tkinter as tk
from pynput.keyboard import Key, Listener
import screeninfo
import threading
import pyautogui
from pynput import keyboard

def get_active_monitor(): #TODO: Add support to more monitors
    mouse_x, mouse_y = pyautogui.position()
    monitors = screeninfo.get_monitors()
    for monitor in monitors:
        if monitor.x <= mouse_x < monitor.x + monitor.width and \
           monitor.y <= mouse_y < monitor.y + monitor.height:
            return monitor

    return monitors[-1]

monitor = get_active_monitor()
monitors = screeninfo.get_monitors()

all_monitors = {}
all_monitors['primary'] = monitors[0]
all_monitors['secondary'] = monitors[1]

window_width = monitor.width
window_height = monitor.height

grid_size = 6
grid_selection = [2, 1]

values = ['Q', 'W', 'E', 'R', 'T', '1',
          'Y', 'U', 'I', 'O', 'P', '2',
          'A', 'S', 'D', 'F', 'G', '3',
          'H', 'J', 'K', 'L', '4', '5',
          'X', 'C', 'V', 'B', '6', '7' ]

value_positions = {}

def on_press(key):
    global grid_selection, grid_size
    try:
        if key == Key.up and grid_selection[1] > 0:
            grid_selection[1] -= 1

        elif key == Key.down and grid_selection[1] < grid_size - 1:
            grid_selection[1] += 1

        elif key == Key.left and grid_selection[0] > 0:
            grid_selection[0] -= 1

        elif key == Key.right and grid_selection[0] < grid_size - 1:
            grid_selection[0] += 1

        elif key == Key.enter:
            move_mouse_to_grid_center()
            draw_inner_grid()

        elif key == Key.esc:  # and root.state() == "normal":
            root.iconify()

        elif key == Key.f5:   # and root.state() == "iconic":
            root.deiconify()

        elif key == Key.f6:   # and root.state() == "normal":
            switch_monitor()

        elif key.char == '-':
            grid_size = max(1, grid_size - 1)  # Decrease grid size but not below 1

        elif key.char == '+':  # '+' key is usually shifted '='
            grid_size += 1  # Increase grid size

        elif hasattr(key, 'char') and key.char and key.char.upper() in value_positions:
            move_mouse_to_subgrid(value_positions[key.char.upper()])
            root.iconify()

        update_highlight()

    except AttributeError:
        pass

def move_mouse_to_grid_center():

    x = grid_selection[0] * (window_width // grid_size) + (window_width // grid_size) // 2
    y = grid_selection[1] * (window_height // grid_size) + (window_height // grid_size) // 2

    pyautogui.moveTo(x+580, y-1080)

def move_mouse_to_subgrid(position):
    if root.state() == "iconic":
        return

    subgrid_col, subgrid_row = position

    # Coordinates of the top-left corner of the selected outer grid box
    outer_x = grid_selection[0] * (window_width // grid_size)
    outer_y = grid_selection[1] * (window_height // grid_size)

    # Dimensions of the outer grid box
    box_width = (window_width // grid_size)
    box_height = (window_height // grid_size)

    # Each subgrid has 6 columns and 5 rows
    cell_width = box_width // 6
    cell_height = box_height // 5

    # Move to the center of the subgrid cell
    x = (outer_x + subgrid_col * cell_width + cell_width // 2) + 60
    y = (outer_y + subgrid_row * cell_height + cell_height // 2) + 50
    if current_monitor == 'secondary':
        pyautogui.moveTo(x + 580, y-1080)

    else:
        pyautogui.moveTo(x, y)

def switch_monitor():
    if root.state() == "iconic":
        return

    global current_monitor
    global all_monitors
    global window_height
    global window_width
    if current_monitor == 'primary':
        current_monitor = 'secondary'
        window_height = all_monitors['secondary'].height
        window_width = all_monitors['secondary'].width
        root.geometry(f"+{580}+{-window_height}")

    else:
        window_height = all_monitors['primary'].height
        window_width = all_monitors['primary'].width
        current_monitor = 'primary'
        root.geometry(f"{window_width-100}x{window_height}+0+0")

def update_highlight():
    if root.state() == "iconic":
        return

    canvas.delete("highlight")
    x = grid_selection[0] * (window_width // grid_size)
    y = grid_selection[1] * (window_height // grid_size)
    corner_radius = 20
    canvas.create_line(x + corner_radius, y, x + (window_width // grid_size) - corner_radius, y, fill="white", width=3, tags="highlight")
    canvas.create_line(x + corner_radius, y + (window_height // grid_size), x + (window_width // grid_size) - corner_radius, y + (window_height // grid_size), fill="white", width=3, tags="highlight")
    canvas.create_line(x, y + corner_radius, x, y + (window_height // grid_size) - corner_radius, fill="white", width=3, tags="highlight")
    canvas.create_line(x + (window_width // grid_size), y + corner_radius, x + (window_width // grid_size), y + (window_height // grid_size) - corner_radius, fill="white", width=3, tags="highlight")
    canvas.create_arc(x, y, x + 2 * corner_radius, y + 2 * corner_radius, start=90, extent=90, style=tk.ARC, outline="white", width=3, tags="highlight")
    canvas.create_arc(x + (window_width // grid_size) - 2 * corner_radius, y, x + (window_width // grid_size), y + 2 * corner_radius, start=0, extent=90, style=tk.ARC, outline="white", width=3, tags="highlight")
    canvas.create_arc(x, y + (window_height // grid_size) - 2 * corner_radius, x + 2 * corner_radius, y + (window_height // grid_size), start=180, extent=90, style=tk.ARC, outline="white", width=3, tags="highlight")
    canvas.create_arc(x + (window_width // grid_size) - 2 * corner_radius, y + (window_height // grid_size) - 2 * corner_radius, x + (window_width // grid_size), y + (window_height // grid_size), start=270, extent=90, style=tk.ARC, outline="white", width=3, tags="highlight")

def draw_inner_grid():
    if root.state() == "iconic":
        return

    canvas.delete("inner_grid")
    x = grid_selection[0] * (window_width // grid_size)
    y = grid_selection[1] * (window_height // grid_size)
    box_width = window_width // grid_size
    box_height = window_height // grid_size

    rows = 5
    cols = 6
    cell_width = box_width // cols
    cell_height = box_height // rows

    value_index = 0

    for i in range(1, cols):
        canvas.create_line(x + i * cell_width, y, x + i * cell_width, y + box_height, fill="white",
                           width=1, tags="inner_grid")
    for i in range(1, rows):
        canvas.create_line(x, y + i * cell_height, x + box_width, y + i * cell_height, fill="white",
                           width=1, tags="inner_grid")

    for row in range(rows):
        for col in range(cols):
            cell_x = x + col * cell_width
            cell_y = y + row * cell_height
            canvas.create_text(cell_x + cell_width // 2, cell_y + cell_height // 2, text=values[value_index],
                               fill="white", activefill="Blue", font=("Helvetica", 20, "bold"),
                               tags="inner_grid")
            value_positions[values[value_index]] = (col, row)
            value_index += 1

root = tk.Tk()
root.title("Transparent Grid")
print(window_width, window_height)


current_monitor = 'primary'
root.geometry(f"{window_width-100}x{window_height}+0+0")
root.wm_attributes("-alpha", 0.6)

canvas = tk.Canvas(root, width=window_width, bg='systemTransparent', height=window_height, highlightthickness=0)
canvas.pack()

update_highlight()

def start_listener():
    while root.state() == "normal":
        with Listener(on_press=on_press) as listener:
            listener.join()

# Start the pynput listener in a separate thread
listener_thread = threading.Thread(target=start_listener, daemon=True)
listener_thread.start()

root.mainloop()
