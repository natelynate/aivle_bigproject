import cv2
import numpy as np

background = cv2.imread('./sample_data/screen.jpg')
heatmap = np.zeros_like(background[:, :, 0], np.float32)  # Use float32 for better precision

# for i in range(1000):
#     heatmap[i, i] += 1

# for i in range(300, 800):
#     heatmap[i, i] += 1

# for i in range(500, 600):
#     heatmap[i, i] += 1

# for i in range(1000):
#     heatmap[1000, i] += 1

x = 100
y = 500
heatmap[y, x] += 1

# 중요: numpy array에서는 y, x로 인덱싱해야 하지만, cv2이미지에서는 x, y순으로 한다! 

image = cv2.imread('./sample_data/screen.jpg')
image = cv2.circle(image, (int(x), int(y)), radius=20, color=(20, 255, 20), thickness=-1) 
# Apply Gaussian blur to the heatmap before normalization
heatmap_blurred = cv2.GaussianBlur(heatmap, (199, 199), 0)  # Use a larger kernel size for more smoothing

# Normalize the blurred heatmap to 8-bit range
heatmap_normalized = cv2.normalize(heatmap_blurred, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
heatmap_img = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)

background = cv2.imread('./sample_data/screen.jpg')
super_imposed_img = cv2.addWeighted(heatmap_img, 0.5, image, 0.5, 0)
# heatmap_vis = cv2.cvtColor(super_imposed_img  , cv2.COLOR_BGR2RGB)
cv2.imwrite('./heatmap.jpg', super_imposed_img)