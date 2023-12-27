import cv2
import pyautogui

# Get the screen size
screen_width, screen_height = pyautogui.size()

# Calculate the coordinates of the center pixel
center_x = screen_width // 2
center_y = screen_height // 2
print(center_x, center_y)
print(f"Center coordinates: ({center_x}, {center_y})")


image = cv2.imread('./sample_data/screen.jpg')
image = cv2.circle(image, (center_x, center_y), radius=3, color=(0, 0, 255), thickness=-1)
cv2.imshow('dot', image)
cv2.waitKey(0)
cv2.destroyAllWindows()