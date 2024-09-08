import numpy as np
import cv2

# Image dimensions
width = 1920
height = 1080

# Create a blank white image
image = np.ones((height, width, 3), dtype=np.uint8) * 255

# Vanishing point at the center of the image
vanishing_point = (width // 2, height // 2)

# Draw horizontal lines
num_lines = 20
spacing = height // num_lines
for i in range(num_lines):
    y = i * spacing
    # Only draw lines above and below the horizon
    if y != vanishing_point[1]:
        pt1 = (0, y)
        pt2 = (width, y)
        cv2.line(image, pt1, pt2, (0, 0, 0), 1)

# Draw vertical lines converging to the vanishing point
for x in range(0, width, spacing):
    pt1 = (x, 0)
    pt2 = vanishing_point
    cv2.line(image, pt1, pt2, (0, 0, 0), 1)

# Draw the horizon line
cv2.line(image, (0, vanishing_point[1]), (width, vanishing_point[1]), (0, 0, 0), 2)

# Show the image
cv2.imshow('1-Point Perspective Grid', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the image
cv2.imwrite('1_point_perspective_grid.png', image)
