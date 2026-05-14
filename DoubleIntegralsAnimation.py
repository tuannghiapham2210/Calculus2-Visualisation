import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the mathematical surface z = f(x, y)
# Using a wavy function here to make the 3D visualization more interesting
def f(x, y):
    return np.sin(x) + np.cos(y) + 2

# Set up the domain boundaries
a, b = 0.0, 5.0  # x-axis limits
c, d = 0.0, 5.0  # y-axis limits

# Define grid resolution (10x10 = 100 boxes total)
# Keeping it relatively small ensures the animation runs smoothly
n_steps = 10 
dx = (b - a) / n_steps
dy = (d - c) / n_steps

# Calculate the center coordinates for each grid cell
x_coords = np.linspace(a + dx/2, b - dx/2, n_steps)
y_coords = np.linspace(c + dy/2, d - dy/2, n_steps)

# Initialize the figure and the 3D axis
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Draw a faint, smooth surface as a reference guide
# This represents the "true" analytical integral
X_smooth, Y_smooth = np.meshgrid(np.linspace(a, b, 50), np.linspace(c, d, 50))
Z_smooth = f(X_smooth, Y_smooth)
ax.plot_surface(X_smooth, Y_smooth, Z_smooth, color='blue', alpha=0.1)

# Fix the axis limits so the plot doesn't rescale dynamically during animation
ax.set_xlim([a, b])
ax.set_ylim([c, d])
ax.set_zlim([0, np.max(Z_smooth) + 1])
ax.set_xlabel('X Axis (Outer Loop)')
ax.set_ylabel('Y Axis (Inner Loop)')
ax.set_zlabel('Z Axis (Height)')

# Global variable to accumulate the Riemann sum volume step-by-step
total_volume = 0.0

# The animation update function, called once per frame
def update(frame):
    global total_volume
    
    # MAGIC HAPPENS HERE: Map the 1D frame counter to 2D nested loop indices
    # ix (outer loop) increments only when iy (inner loop) finishes a full cycle
    # This perfectly simulates the "Iterated Integral / Slicing" logic
    ix = frame // n_steps  
    iy = frame % n_steps   
    
    # Extract current coordinates and calculate height
    x_val = x_coords[ix]
    y_val = y_coords[iy]
    z_val = f(x_val, y_val)
    
    # Calculate the volume of this specific tiny box and accumulate it
    tiny_box_volume = z_val * dx * dy
    total_volume += tiny_box_volume
    
    # Draw the new 3D bar (box)
    # Note: bar3d takes the starting coordinates (bottom-left corner), 
    # so we subtract half the width/depth from the center point
    ax.bar3d(x_val - dx/2, y_val - dy/2, 0, dx, dy, z_val, 
             color='cyan', edgecolor='black', alpha=0.8)
    
    # Update the title dynamically to show the variables' states
    title_text = (f"Simulating Nested Loops (Iterated Integral)\n"
                  f"Outer Loop x = {x_val:.2f} | Inner Loop y = {y_val:.2f}\n"
                  f"Accumulated Volume = {total_volume:.2f}")
    ax.set_title(title_text)

# Create the animation object
# frames: Total number of iterations (n_steps * n_steps)
# interval: Delay between frames in milliseconds (100ms = 10fps)
ani = FuncAnimation(fig, update, frames=n_steps * n_steps, interval=100, repeat=False)

# Display the plot
plt.show()