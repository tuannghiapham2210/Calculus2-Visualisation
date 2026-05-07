import numpy as np
import matplotlib.pyplot as plt

# Initialize 3D space
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# ==========================================
# 1. PLOT THE TWO SURFACES
# ==========================================
# Create a coordinate grid (Meshgrid)
x = np.linspace(-2.5, 1.5, 100)
y = np.linspace(-1, 3, 100)
X, Y = np.meshgrid(x, y)

# Surface S1: Paraboloid z = x^2 + y^2
Z1 = X**2 + Y**2

# Surface S2: Ellipsoid 4x^2 + y^2 + z^2 = 9 
# (Solve for z, take the z > 0 part because point P(-1, 1, 2) is in the upper half)
Z2_squared = 9 - 4*X**2 - Y**2
# np.maximum is used to avoid negative square root errors outside the ellipsoid's domain
Z2 = np.sqrt(np.maximum(Z2_squared, 0)) 

# Plot both surfaces (reduce alpha for transparency)
ax.plot_surface(X, Y, Z1, alpha=0.4, color='cyan', edgecolor='none')
ax.plot_surface(X, Y, Z2, alpha=0.4, color='orange', edgecolor='none')

# ==========================================
# 2. DEFINE POINT P AND NORMAL VECTORS
# ==========================================
P = np.array([-1, 1, 2])
ax.scatter(*P, color='black', s=100, label='Point of tangency P(-1, 1, 2)')

# Gradient vectors at P (calculated previously)
n1 = np.array([-2, 2, -1])  # Gradient of the Paraboloid
n2 = np.array([-8, 2, 4])   # Gradient of the Ellipsoid

# Visualize vectors n1 and n2 using the quiver function
# Scale down to make the plot less cluttered
scale = 0.15 
ax.quiver(*P, *(n1 * scale), color='blue', linewidth=2.5, label='Gradient S1 (n1)')
ax.quiver(*P, *(n2 * scale), color='green', linewidth=2.5, label='Gradient S2 (n2)')

# ==========================================
# 3. CROSS PRODUCT AND TANGENT LINE
# ==========================================
# Logical core: Calculate the cross product directly in numpy
u_cross = np.cross(n1, n2) 
# Simplify the vector [10, 16, 12] to [5, 8, 6] as solved manually
v_dir = u_cross / 2 

# Plot the tangent vector (cross product) at P
ax.quiver(*P, *(v_dir * scale), color='red', linewidth=3, label='Cross product (n1 x n2)')

# Plot the extended tangent line
t = np.linspace(-0.3, 0.3, 100)
line_x = P[0] + v_dir[0] * t
line_y = P[1] + v_dir[1] * t
line_z = P[2] + v_dir[2] * t
ax.plot(line_x, line_y, line_z, color='red', linestyle='--', linewidth=2, label='Tangent line')

# ==========================================
# 4. VIEWING ANGLE AND DISPLAY CUSTOMIZATION
# ==========================================
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_xlim([-3, 2])
ax.set_ylim([-1, 3])
ax.set_zlim([0, 5])

# Viewing angle (Elevation and Azimuth) - You can rotate with your mouse when the figure appears
ax.view_init(elev=20, azim=45) 

plt.title('Geometric Concept: Tangent via Cross Product of Gradients', fontweight='bold')
ax.legend(loc='upper left')
plt.show()