import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import RectangleSelector

# Sample data for plotting
np.random.seed(0)
x = np.random.rand(100)
y = np.random.rand(100)

# Global scatter plot reference
scatter = None

# Function to remove points inside the rectangle
def remove_selected_points(eclick, erelease):
    global x, y, scatter

    # Get the rectangle boundaries
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    # Determine the selected region
    xmin, xmax = sorted([x1, x2])
    ymin, ymax = sorted([y1, y2])

    # Identify points inside the rectangle
    inside = (x >= xmin) & (x <= xmax) & (y >= ymin) & (y <= ymax)

    # Remove the points inside the rectangle
    x = x[~inside]
    y = y[~inside]

    # Clear the current scatter plot and redraw it
    scatter.set_offsets(np.c_[x, y])
    canvas.draw()

# Function to reset the plot to the original data
def reset_plot():
    global x, y, scatter
    x = np.random.rand(100)
    y = np.random.rand(100)
    scatter.set_offsets(np.c_[x, y])
    canvas.draw()

# Creating the main application window
root = tk.Tk()
root.title("Interactive Plot")

# Create a matplotlib figure and axis
fig, ax = plt.subplots()
scatter = ax.scatter(x, y)
ax.set_title("Select Points to Delete")

# Embed the plot in a tkinter canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Rectangle selector for interactive selection
rect_selector = RectangleSelector(ax, remove_selected_points,
                                  drawtype='box', useblit=True,
                                  button=[1],  # Left mouse button
                                  minspanx=5, minspany=5,
                                  spancoords='pixels',
                                  interactive=True)

# Add a reset button
reset_button = ttk.Button(root, text="Reset", command=reset_plot)
reset_button.pack(side=tk.BOTTOM, pady=10)

# Run the tkinter main loop
root.mainloop()
