import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Initialize 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.25)

# 1. Create a paraboloid surface (the hill): z = 4 - x^2 - y^2
X = np.arange(-2, 2.1, 0.1)
Y = np.arange(-2, 2.1, 0.1)
X, Y = np.meshgrid(X, Y)
Z = 4 - X**2 - Y**2

# Plot the surface
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6, edgecolor='none')

# 2. Select a point P on the hillside
x0, y0 = 0.5, 0.5
z0 = 4 - x0**2 - y0**2
ax.scatter([x0], [y0], [z0], color='red', s=100, label='Point P(0.5, 0.5, 3.5)', zorder=5)

# Initialize the tangent vector (will be updated continuously)
quiver = None

# 3. Create a slider to change the rotation angle
ax_theta = plt.axes([0.2, 0.1, 0.65, 0.03])
s_theta = Slider(ax_theta, 'Angle (degrees)', 0, 360, valinit=45, valstep=1)

# Partial derivatives at P
fx = -2 * x0
fy = -2 * y0

# Update function when the slider is moved
def update(val):
    global quiver
    theta_rad = np.radians(s_theta.val)
    
    # Direction vector u = (a, b)
    u_x = np.cos(theta_rad)
    u_y = np.sin(theta_rad)
    
    # DIRECTIONAL DERIVATIVE: Du f = fx*u_x + fy*u_y
    dz = fx * u_x + fy * u_y
    
    # Remove the old vector and draw the new tangent vector
    if quiver is not None:
        quiver.remove()
        
    # Draw a red arrow representing the slope at point P
    quiver = ax.quiver(x0, y0, z0, u_x, u_y, dz, 
                       color='red', length=1.5, normalize=False, arrow_length_ratio=0.1, linewidth=3)
    
    ax.set_title(f"Directional Derivative (Slope): $D_u f$ = {dz:.2f}\n(Angle $\\theta$ = {s_theta.val:.0f}°)")
    fig.canvas.draw_idle()

# Attach the slider drag event to the update function
s_theta.on_changed(update)
update(0) # Run initially to draw

# Adjust display settings
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis (Height)')
ax.legend()
plt.show()