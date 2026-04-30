import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ==========================================
# LAGRANGE MULTIPLIER 2D INTERACTIVE PLOT
# Objective: Minimize f(x,y) = x^2 + y^2
# Constraint: g(x,y) = x + y = 2
# ==========================================

# 1. Setup the figure and axis
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.25)
ax.set_aspect('equal') # CRITICAL: Ensures circles look like circles and angles are true
ax.grid(True, linestyle=':', alpha=0.6)

# 2. Draw the static constraint line: x + y = 2  =>  y = 2 - x
x_line = np.linspace(-2, 4, 100)
y_line = 2 - x_line
ax.plot(x_line, y_line, 'b-', linewidth=2, label='Constraint: $g(x,y) = x + y = 2$')

# 3. Initialize dynamic plot elements (Point P, Level Curve, Vectors)
point_p, = ax.plot([], [], 'ko', markersize=8, label='Point P', zorder=5)

# The level curve of f(x,y) = x^2 + y^2 is a circle centered at origin
theta = np.linspace(0, 2*np.pi, 100)
level_curve, = ax.plot([], [], 'r--', linewidth=2, label='Level Curve: $f(x,y) = c$')

# Quiver objects for vectors (initialized as None to handle updates)
grad_f_quiver = None
grad_g_quiver = None

# 4. Create a slider to move Point P along the x-axis
ax_x = plt.axes([0.15, 0.1, 0.7, 0.03])
# Point P will move from x = -1.5 to x = 3.5
s_x = Slider(ax_x, 'x-coordinate', -1.5, 3.5, valinit=3.0, valstep=0.1)

# 5. Update function triggered by slider
def update(val):
    global grad_f_quiver, grad_g_quiver
    
    # Calculate current coordinates of P on the constraint line
    x0 = s_x.val
    y0 = 2 - x0
    
    # Update Point P position
    point_p.set_data([x0], [y0])
    
    # Calculate objective function value c = f(x0, y0)
    c = x0**2 + y0**2
    radius = np.sqrt(c)
    
    # Update the level curve (circle passing through P)
    level_curve.set_data(radius * np.cos(theta), radius * np.sin(theta))
    
    # Calculate gradients at P
    # f(x,y) = x^2 + y^2  =>  Gradient f = [2x, 2y]
    # g(x,y) = x + y      =>  Gradient g = [1, 1]
    grad_f_x, grad_f_y = 2*x0, 2*y0
    grad_g_x, grad_g_y = 1, 1
    
    # Remove old vectors if they exist
    if grad_f_quiver is not None:
        grad_f_quiver.remove()
    if grad_g_quiver is not None:
        grad_g_quiver.remove()
        
    # Draw new gradient vectors
    # scale=1, scale_units='xy', angles='xy' ensures the vectors are drawn to exact scale
    grad_f_quiver = ax.quiver(x0, y0, grad_f_x, grad_f_y, color='red', 
                              angles='xy', scale_units='xy', scale=1, width=0.005, label=r'$\nabla f$')
    grad_g_quiver = ax.quiver(x0, y0, grad_g_x, grad_g_y, color='green', 
                              angles='xy', scale_units='xy', scale=1, width=0.005, label=r'$\nabla g$')
    
    # Check if they are parallel (cross product is 0)
    # cross_prod = x1*y2 - x2*y1
    cross_prod = grad_f_x * grad_g_y - grad_f_y * grad_g_x
    if abs(cross_prod) < 1e-5:
        # Calculate lambda: grad_f = lambda * grad_g
        lambda_val = grad_f_x / grad_g_x
        status = f"EUREKA! Vectors are PARALLEL.\n$\\nabla f = {lambda_val:.1f} \\nabla g$"
    else:
        status = "Vectors are NOT parallel."
        
    # Update title
    ax.set_title(f"Point P({x0:.1f}, {y0:.1f}) | $f(P) = {c:.2f}$\n{status}")
    
    fig.canvas.draw_idle()

# Attach the update function to the slider
s_x.on_changed(update)

# Initial setup limits and draw
ax.set_xlim(-4, 6)
ax.set_ylim(-4, 6)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

# Fix duplicate labels in legend caused by quiver updates
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='upper right')

# Run initial frame
update(3.0)

plt.show()