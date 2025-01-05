# from pynput.mouse import Listener

# def on_move(x, y):
#     """
#     Callback function that gets called whenever the mouse is moved.

#     :param x: The x-coordinate of the mouse pointer.
#     :param y: The y-coordinate of the mouse pointer.
#     """
#     print(f"Mouse moved to ({x}, {y})")

# # Start listening to mouse events
# with Listener(on_move=on_move) as listener:
#     listener.join()

# from screeninfo import get_monitors

# monitors = get_monitors()

# for i, monitor in enumerate(monitors):
#     print(f"Monitor {i}: x={monitor.x}, y={monitor.y}, width={monitor.width}, height={monitor.height}")
# ---------------------------------------------------------------------------------------------------------------------
# import tkinter as tk
# from screeninfo import get_monitors

# def move_to_monitor(window, monitor_id):
#     """
#     Moves a tkinter window to the specified monitor.

#     :param window: The tkinter window to move.
#     :param monitor_id: The monitor index (0 for primary, 1 for secondary, etc.).
#     """
#     monitors = get_monitors()
#     if monitor_id < len(monitors):
#         monitor = monitors[monitor_id]
#         # Get the top-left corner of the target monitor
#         x_offset = monitor.x
#         y_offset = monitor.y
#         # Move the window to the monitor's position
#         print(f"Moving window to monitor {monitor_id} at position ({x_offset}, {y_offset})")
#         window.geometry(f"+{x_offset + 100}+{-y_offset}")  # Add padding
#     else:
#         print(f"Monitor {monitor_id} does not exist.")

# # Create tkinter application
# root = tk.Tk()
# root.title("Move Between Monitors")
# root.geometry("400x300")  # Set initial size

# # Label to display instructions
# label = tk.Label(root, text="Click a button to move the window to a monitor.")
# label.pack(pady=20)

# # Buttons to move the app between monitors
# for i in range(len(get_monitors())):
#     tk.Button(root, text=f"Move to Monitor {i}", command=lambda i=i: move_to_monitor(root, i)).pack(pady=10)

# root.mainloop()

import tkinter as tk

def on_focus(event=None):
    root.deiconify()  # Ensure the window is restored when focused

root = tk.Tk()
root.title("Tkinter App")

# Bind the focus event to restore the window
root.bind("<FocusIn>", on_focus)

label = tk.Label(root, text="Minimize and restore the window using Cmd+Tab.")
label.pack(pady=20)

root.mainloop()
