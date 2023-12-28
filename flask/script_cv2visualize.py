import cv2
import pyautogui

# Get the screen size
screen_width, screen_height = pyautogui.size()

image = cv2.imread('./sample_data/screen.jpg')
image = cv2.circle(image, (100, 100), radius=20, color=(0, 0, 255), thickness=-1)
image = cv2.circle(image, (800, 900), radius=20, color=(0, 0, 255), thickness=-1)
image = cv2.circle(image, (1100, 100), radius=20, color=(0, 0, 255), thickness=-1)
image = cv2.circle(image, (1800, 900), radius=20, color=(0, 0, 255), thickness=-1)
cv2.imshow('dot', image)
cv2.waitKey(0)
cv2.destroyAllWindows()