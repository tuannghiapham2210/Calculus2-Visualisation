import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

# ==========================================
# 1. DEFINE THE MATHEMATICAL FUNCTION
# ==========================================
def f(x, y):
    """Returns the z-value (height) for given x and y coordinates."""
    return 16 - x**2 - 2 * y**2

# Domain boundaries
x_start, x_end = 0, 2
y_start, y_end = 0, 2

# Pre-calculate the smooth true surface (this doesn't change, saves CPU)
x_smooth = np.linspace(x_start, x_end, 100)
y_smooth = np.linspace(y_start, y_end, 100)
X_smooth, Y_smooth = np.meshgrid(x_smooth, y_smooth)
Z_smooth = f(X_smooth, Y_smooth)

# ==========================================
# 2. INITIALIZE THE FIGURE
# ==========================================
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Adjust the main plot to make room for the slider at the bottom
plt.subplots_adjust(bottom=0.25)

# ==========================================
# 3. CORE DRAWING FUNCTION
# ==========================================
def draw_plot(grid_size):
    """Clears the axis, recalculates Riemann sum, and redraws everything."""
    ax.cla()  # Clear current axes completely
    
    # Redraw the transparent true surface
    ax.plot_surface(X_smooth, Y_smooth, Z_smooth, 
                    color='red', alpha=0.15, edgecolor='none')
    
    # Cast slider value to integer (can't have 2.5 boxes!)
    m = int(grid_size)
    n = int(grid_size)
    
    # Recalculate dimensions
    dx = (x_end - x_start) / m
    dy = (y_end - y_start) / n
    delta_A = dx * dy
    
    # Vectorized Midpoint generation
    x_mid = np.linspace(x_start + dx/2, x_end - dx/2, m)
    y_mid = np.linspace(y_start + dy/2, y_end - dy/2, n)
    X_mid, Y_mid = np.meshgrid(x_mid, y_mid)
    
    # Calculate heights and volume
    Z_heights = f(X_mid, Y_mid)
    estimated_volume = np.sum(Z_heights * delta_A)
    
    # Flatten arrays for 3D bar plotting
    x_pos = (X_mid - dx/2).flatten()
    y_pos = (Y_mid - dy/2).flatten()
    z_pos = np.zeros_like(x_pos)
    
    x_size = np.full_like(x_pos, dx)
    y_size = np.full_like(y_pos, dy)
    z_size = Z_heights.flatten()
    
    # Draw the new set of 3D bars
    ax.bar3d(x_pos, y_pos, z_pos, x_size, y_size, z_size, 
             shade=True, color='skyblue', edgecolor='black', alpha=0.8)
             
    # Reset labels and titles (since ax.cla() wiped them out)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis (Height)')
    ax.set_title(f'Interactive Riemann Sum\n'
                 f'Grid: {m}x{n} | Est. Volume: {estimated_volume:.4f}', 
                 fontsize=14, fontweight='bold')

# Draw the initial state with 4x4 boxes
initial_grid = 4
draw_plot(initial_grid)

# ==========================================
# 4. SET UP THE UI SLIDER
# ==========================================
# Define the axes for the slider [left, bottom, width, height]
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])

# Create the Slider object
# valstep=1 ensures the slider only snaps to whole numbers
grid_slider = Slider(
    ax=ax_slider,
    label='Grid Size (m=n)',
    valmin=2,
    valmax=30,  # Max 30x30 = 900 boxes (keeps it from lagging)
    valinit=initial_grid,
    valstep=1,
    color='green'
)

# Define the callback function that runs whenever the slider is moved
def update(val):
    draw_plot(grid_slider.val)
    fig.canvas.draw_idle()  # Request a UI redraw

# Attach the callback to the slider
grid_slider.on_changed(update)

# Show the interactive window!
plt.show()