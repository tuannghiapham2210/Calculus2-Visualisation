import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. Define the cost function (A simple paraboloid bowl) and its gradient
def cost_function(x, y):
    return x**2 + y**2

def gradient(x, y):
    # Partial derivative with respect to x is 2x, and to y is 2y
    return np.array([2*x, 2*y])

# --- SIMULATION PARAMETERS ---
# alpha/eta is the learning rate that controls the step size
LEARNING_RATE = 0.1 
ITERATIONS = 30
START_POS = np.array([8.0, 6.0])

# 2. Pre-calculate the entire Gradient Descent trajectory
history = []
current_pos = START_POS.copy()

for _ in range(ITERATIONS + 1):
    z = cost_function(current_pos[0], current_pos[1])
    history.append([current_pos[0], current_pos[1], z])
    
    # Calculate the gradient vector at the current position
    grad = gradient(current_pos[0], current_pos[1])
    
    # Update rule: Move in the OPPOSITE direction of the gradient
    current_pos = current_pos - LEARNING_RATE * grad

# Convert history to a numpy array for easier slicing
history = np.array(history)

# 3. Setup the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Create a meshgrid for the 3D surface
X = np.arange(-10, 10, 0.5)
Y = np.arange(-10, 10, 0.5)
X, Y = np.meshgrid(X, Y)
Z = cost_function(X, Y)

# Plot the surface (semi-transparent so we can see the path clearly)
ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.5, edgecolor='none')

# Initialize the empty line (trajectory) and point (current position) for animation
trajectory_line, = ax.plot([], [], [], color='red', linewidth=2, label='Path')
current_point, = ax.plot([], [], [], color='black', marker='o', markersize=8, label='Current Pos')

# Configure axes and labels
ax.set_title(f'3D Gradient Descent Animation\nLearning Rate (eta) = {LEARNING_RATE}')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Cost Function (Z-axis)')
ax.legend()

# 4. Define the animation update function
def update_frame(frame):
    # Slice the history array up to the current frame to draw the trail
    x_data = history[:frame+1, 0]
    y_data = history[:frame+1, 1]
    z_data = history[:frame+1, 2]
    
    # Update the trajectory line
    trajectory_line.set_data(x_data, y_data)
    trajectory_line.set_3d_properties(z_data)
    
    # Update the position of the moving dot
    current_point.set_data([history[frame, 0]], [history[frame, 1]])
    current_point.set_3d_properties([history[frame, 2]])
    
    return trajectory_line, current_point

# 5. Create and run the animation
# interval=200 means 200 milliseconds between frames
ani = FuncAnimation(fig, update_frame, frames=len(history), interval=500, blit=False)

plt.show()