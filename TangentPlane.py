import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 1. Ellipsoid parameters based on the equation: x^2/4 + y^2 + z^2/9 = 3
# Dividing by 3 to get standard form: x^2/12 + y^2/3 + z^2/27 = 1
# So, semi-axes are a=sqrt(12), b=sqrt(3), c=sqrt(27)
a = np.sqrt(12)
b = np.sqrt(3)
c = np.sqrt(27)

# Initialize 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.25) # Make room for sliders

# 2. Draw the transparent ellipsoid surface
u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, np.pi, 40)
U, V = np.meshgrid(u, v)

# Parametric equations for the ellipsoid
X = a * np.sin(V) * np.cos(U)
Y = b * np.sin(V) * np.sin(U)
Z = c * np.cos(V)

ax.plot_surface(X, Y, Z, color='cyan', alpha=0.2, edgecolor='none')

# Initialize dynamic plot elements
point_p, = ax.plot([], [], [], 'ro', markersize=8, label='Point P')
normal_vector = None
tangent_plane = None

# 3. Create sliders for Spherical Coordinates (Theta and Phi angles)
# This ensures point P always perfectly constraints to the ellipsoid surface
ax_theta = plt.axes([0.15, 0.1, 0.7, 0.03])
ax_phi = plt.axes([0.15, 0.05, 0.7, 0.03])

s_theta = Slider(ax_theta, 'Longitude (Theta)', 0, 360, valinit=45, valstep=1)
s_phi = Slider(ax_phi, 'Latitude (Phi)', 1, 179, valinit=60, valstep=1)

# 4. Update function triggered by slider movement
def update(val):
    global normal_vector, tangent_plane
    
    theta_rad = np.radians(s_theta.val)
    phi_rad = np.radians(s_phi.val)
    
    # Calculate exact coordinates of Point P
    x0 = a * np.sin(phi_rad) * np.cos(theta_rad)
    y0 = b * np.sin(phi_rad) * np.sin(theta_rad)
    z0 = c * np.cos(phi_rad)
    
    # Update Point P marker
    point_p.set_data([x0], [y0])
    point_p.set_3d_properties([z0])
    
    # ----------------------------------------------------
    # CALCULATE GRADIENT VECTOR (NORMAL)
    # F(x,y,z) = x^2/4 + y^2 + z^2/9 = 3
    # Partial derivatives: Fx = x/2, Fy = 2y, Fz = 2z/9
    # ----------------------------------------------------
    nx = x0 / 2
    ny = 2 * y0
    nz = 2 * z0 / 9
    
    # Normalize the gradient vector to unit length for better visualization
    norm = np.sqrt(nx**2 + ny**2 + nz**2)
    nx_u, ny_u, nz_u = nx/norm, ny/norm, nz/norm 
    
    # Redraw the Gradient Vector (Normal Line)
    if normal_vector is not None:
        normal_vector.remove()
    normal_vector = ax.quiver(x0, y0, z0, nx_u, ny_u, nz_u, 
                              color='red', length=4, linewidth=2.5, label='Gradient / Normal')
    
    # ----------------------------------------------------
    # CALCULATE TANGENT PLANE
    # ----------------------------------------------------
    if tangent_plane is not None:
        tangent_plane.remove()
        
    # Find two orthogonal vectors lying on the tangent plane to draw a local flat grid
    if abs(nz_u) < 0.99:
        v1 = np.array([-ny_u, nx_u, 0])
    else:
        v1 = np.array([1, 0, 0])
        
    v1 = v1 / np.linalg.norm(v1)
    v2 = np.cross(np.array([nx_u, ny_u, nz_u]), v1)
    
    # Generate a local 2D grid for the plane
    plane_size = 3
    pu = np.linspace(-plane_size, plane_size, 10)
    pv = np.linspace(-plane_size, plane_size, 10)
    PU, PV = np.meshgrid(pu, pv)
    
    # Transform local grid points to 3D space anchored at Point P
    PX = x0 + PU * v1[0] + PV * v2[0]
    PY = y0 + PU * v1[1] + PV * v2[1]
    PZ = z0 + PU * v1[2] + PV * v2[2]
    
    tangent_plane = ax.plot_surface(PX, PY, PZ, color='orange', alpha=0.6, edgecolor='none')
    
    # Update title with real-time coordinates
    ax.set_title(f'Tangent Plane and Gradient Vector\n$P({x0:.2f}, {y0:.2f}, {z0:.2f})$')
    fig.canvas.draw_idle()

# Attach events
s_theta.on_changed(update)
s_phi.on_changed(update)

# Initial draw
update(0)

# 5. Aesthetic configurations
# Set strict limits to prevent axis scaling jitter during rotation
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-6, 6)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

plt.show()