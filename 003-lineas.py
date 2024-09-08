import numpy as np
import cv2

# Image dimensions
width = 1920
height = 1080

# Create a blank white image
image = np.ones((height, width, 3), dtype=np.uint8) * 255

# Vanishing point at the center of the image
vanishing_point = (width // 2, height // 2)

# Draw horizontal lines with perspective spacing
num_lines = 30  # Increase the number of lines for better coverage
max_spacing = 500  # Adjust the spacing for a more realistic effect

for i in range(1, num_lines + 1):
    # Calculate y positions for the lines above and below the horizon
    y_down = int(vanishing_point[1] + (max_spacing * (i / num_lines)**2))
    y_up = int(vanishing_point[1] - (max_spacing * (i / num_lines)**2))
    
    # Draw lines below the vanishing point down to the bottom of the image
    if y_down < height:
        pt1 = (0, y_down)
        pt2 = (width, y_down)
        cv2.line(image, pt1, pt2, (0, 0, 0), 1)
    
    # Draw lines above the vanishing point up to the top of the image
    if y_up > 0:
        pt1 = (0, y_up)
        pt2 = (width, y_up)
        cv2.line(image, pt1, pt2, (0, 0, 0), 1)

# Draw vertical lines converging to the vanishing point from top to bottom
spacing = 100  # Adjusted for better visual effect
for x in range(0, width, spacing):
    pt1_top = (x, 0)
    pt1_bottom = (x, height)
    pt2 = vanishing_point
    # Draw from the top of the image to the vanishing point
    cv2.line(image, pt1_top, pt2, (0, 0, 0), 1)
    # Draw from the bottom of the image to the vanishing point
    cv2.line(image, pt1_bottom, pt2, (0, 0, 0), 1)

# Draw the horizon line
cv2.line(image, (0, vanishing_point[1]), (width, vanishing_point[1]), (0, 0, 0), 2)

# Show the image
cv2.imshow('1-Point Perspective Grid', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the image
cv2.imwrite('1_point_perspective_grid_full_floor_ceiling.png', image)
