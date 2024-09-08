import numpy as np
import cv2

# Image dimensions
width = 1920
height = 1080

# Create a blank white image
image = np.ones((height, width, 3), dtype=np.uint8) * 255

# Vanishing point at the center of the image
vanishing_point = np.array([width // 2, height // 2])

# Draw horizontal lines with perspective spacing
num_lines = 30
max_spacing = 500

for i in range(1, num_lines + 1):
    y_down = int(vanishing_point[1] + (max_spacing * (i / num_lines)**2))
    y_up = int(vanishing_point[1] - (max_spacing * (i / num_lines)**2))
    
    if y_down < height:
        pt1 = (0, y_down)
        pt2 = (width, y_down)
        cv2.line(image, pt1, pt2, (0, 0, 0), 1)
    
    if y_up > 0:
        pt1 = (0, y_up)
        pt2 = (width, y_up)
        cv2.line(image, pt1, pt2, (0, 0, 0), 1)

spacing = 100
for x in range(0, width, spacing):
    pt1_top = (x, 0)
    pt1_bottom = (x, height)
    pt2 = vanishing_point
    cv2.line(image, pt1_top, pt2, (0, 0, 0), 1)
    cv2.line(image, pt1_bottom, pt2, (0, 0, 0), 1)

cv2.line(image, (0, vanishing_point[1]), (width, vanishing_point[1]), (0, 0, 0), 2)

# Function to project 3D points to 2D
def project_point(point, vp, scale=1):
    """ Projects a 3D point onto the 2D plane using a 1-point perspective. """
    x, y, z = point
    factor = scale / (z + scale)
    x_2d = int(vp[0] + x * factor)
    y_2d = int(vp[1] - y * factor)
    return (x_2d, y_2d)

# Function to draw a cube given its center position in 3D
def draw_cube(center, scale, color=(0, 0, 255)):
    x, y, z = center
    cube_points = [
        (x-1, y-1, z-1),  # Bottom-back-left
        (x+1, y-1, z-1),  # Bottom-back-right
        (x+1, y+1, z-1),  # Top-back-right
        (x-1, y+1, z-1),  # Top-back-left
        (x-1, y-1, z+1),  # Bottom-front-left
        (x+1, y-1, z+1),  # Bottom-front-right
        (x+1, y+1, z+1),  # Top-front-right
        (x-1, y+1, z+1)   # Top-front-left
    ]
    
    projected_points = [project_point(p, vanishing_point, scale=scale) for p in cube_points]
    
    cube_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
        (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
    ]
    
    for edge in cube_edges:
        pt1 = projected_points[edge[0]]
        pt2 = projected_points[edge[1]]
        cv2.line(image, pt1, pt2, color, 2)

# Draw a single large cube close to the camera
draw_cube((0, 0, 0.5), scale=1000)

# Draw additional cubes at different positions and distances
cube_positions = [
    (-2, -2, 1.5),
    (2, -2, 2),
    (-3, 2, 2.5),
    (3, 3, 3),
    (0, 0, 1)
]

# Draw each additional cube
for pos in cube_positions:
    draw_cube(pos, scale=500)

# Show the image
cv2.imshow('Multiple 3D Cubes in 1-Point Perspective', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the image
cv2.imwrite('multiple_3d_cubes_visible.png', image)
