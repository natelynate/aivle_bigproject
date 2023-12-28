import cv2
import numpy as np

# Define the points in the original system
x1_orig, y1_orig = 0, 0
x2_orig, y2_orig = 1920, 1080

def addWhiteNoise(x, y, mean=10, std_dev=5):
    """Add white noise to the pixel coordinates"""
    noise_x = np.random.normal(loc=mean, scale=std_dev)
    noise_y = np.random.normal(loc=mean, scale=std_dev)
    return x+noise_x, y+noise_y

def findScaleFactor(minX, minY, maxX, maxY):
    # Compute the scale factors
    x_scale_factor = (maxX - minX) / (x2_orig - x1_orig)
    y_scale_factor = (maxY - minY) / (y2_orig - y1_orig)
    return x_scale_factor, y_scale_factor
 

def translatePoint(x, y, x_scale_factor, y_scale_factor):
    # Compute the offsets
    x_offset = abs(minX) - abs(x) / x_scale_factor
    y_offset = abs(minY) - abs(y) / y_scale_factor
    # Map the coordinates
    x_mapped = x1_orig + x_offset
    y_mapped = y1_orig + y_offset
    return x_mapped, y_mapped



"""Resize the pupil coordinates"""
movement_history = movement_history = [(2310.0, 1326.0), (1922.0, 941.0), (1930.0, 941.0), (1154.0, 942.0), (1162.0, 1326.0), (1156.0, 1327.0), (1157.0, 1326.0), (770.0, 937.0), (771.0, 1322.0), (773.0, 1322.0), (777.0, 943.0), (393.0, 749.0), (387.0, 1065.0), (394.0, 1069.0), (772.0, 938.0), (389.0, 753.0), (388.0, 1071.0), (1162.0, 937.0), (772.0, 937.0), (1161.0, 1324.0), (1539.0, 941.0), (1543.0, 940.0), (1546.0, 942.0), (1546.0, 558.0), (1546.0, 554.0), (1542.0, 942.0), (1538.0, 553.0), (1545.0, 558.0), (1545.0, 937.0), (1539.0, 938.0), (2690.0, 556.0), (2694.0, 560.0), (2690.0, 561.0), (2693.0, 554.0), (2692.0, 556.0), (2693.0, 171.0), (2690.0, 170.0), (3076.0, 176.0), (3464.0, 172.0), (3465.0, 173.0), (3461.0, 173.0), (3464.0, 174.0), (3076.0, 169.0), (3076.0, 218.0), (3459.0, 177.0), (3074.0, 173.0), (1924.0, 218.0), (1154.0, 218.0), (1544.0, 219.0), (1154.0, 219.0), (1544.0, 224.0), (1538.0, 221.0), (1546.0, 224.0), (1542.0, 225.0), (1538.0, 174.0), (1158.0, 219.0), (1159.0, 173.0), (2693.0, 558.0), (2313.0, 554.0), (2306.0, 553.0), (2306.0, 560.0), (2312.0, 560.0), (2314.0, 561.0), (2691.0, 940.0), (2690.0, 944.0), (2692.0, 943.0), (2697.0, 943.0), (3076.0, 938.0), (3082.0, 937.0), (2695.0, 940.0), (2691.0, 940.0), (2692.0, 937.0), (2691.0, 942.0), (3074.0, 943.0), (2690.0, 942.0), (3463.0, 169.0), (3460.0, 176.0), (3463.0, 175.0), (3463.0, 177.0), (3458.0, 169.0), (3462.0, 173.0), (3460.0, 176.0), (3082.0, 177.0), (1928.0, 177.0), (1925.0, 173.0), (1929.0, 169.0), (1538.0, 173.0), (1542.0, 174.0), (1546.0, 170.0), (1538.0, 172.0), (1160.0, 175.0), (1156.0, 175.0), (1545.0, 172.0), (774.0, 170.0), (773.0, 169.0), (778.0, 177.0), (773.0, 169.0), (394.0, 110.0), (773.0, 941.0), (1154.0, 1326.0), (1158.0, 1710.0), (1158.0, 1327.0), (1160.0, 1326.0), (770.0, 1327.0), (1156.0, 1328.0), (1162.0, 1328.0), (1161.0, 1707.0), (1157.0, 1713.0), (1159.0, 1325.0), (1539.0, 1324.0), (1157.0, 1326.0), (1154.0, 1713.0), (1161.0, 1710.0), (1923.0, 1326.0), (2306.0, 1326.0), (2314.0, 1323.0), (2309.0, 1325.0), (2309.0, 1322.0), (2696.0, 938.0), (2695.0, 942.0), (2698.0, 938.0), (2694.0, 941.0), (2694.0, 557.0), (2693.0, 942.0), (2697.0, 938.0), (2690.0, 944.0), (2690.0, 945.0), (2698.0, 559.0), (2310.0, 556.0), (2310.0, 554.0), (2310.0, 177.0), (2309.0, 173.0), (2306.0, 556.0), (2311.0, 555.0), (2309.0, 561.0), (1155.0, 170.0), (1156.0, 169.0), (1159.0, 176.0), (1159.0, 176.0), (1157.0, 170.0), (1162.0, 174.0), (1155.0, 176.0), (770.0, 176.0), (392.0, 112.0), (386.0, 106.0), (389.0, 112.0), (392.0, 110.0), (389.0, 105.0), (388.0, 427.0), (391.0, 432.0), (1540.0, 556.0), (1544.0, 554.0), (2310.0, 937.0), (1929.0, 941.0), (2310.0, 1326.0), (1922.0, 945.0), (1928.0, 940.0), (1928.0, 943.0), (1924.0, 1321.0), (1924.0, 1328.0), (1540.0, 1326.0), (1924.0, 1329.0), (1928.0, 1327.0), (2691.0, 940.0), (3081.0, 937.0), (3462.0, 945.0), (3462.0, 555.0), (3460.0, 943.0), (3460.0, 940.0), (3459.0, 941.0), (3460.0, 561.0), (3465.0, 944.0), (3460.0, 941.0), (3074.0, 942.0), (1926.0, 558.0), (1160.0, 559.0), (1156.0, 561.0), (1157.0, 558.0), (1543.0, 559.0), (1158.0, 553.0), (1539.0, 557.0), (1541.0, 556.0), (1154.0, 172.0), (1162.0, 170.0), (1154.0, 177.0), (1160.0, 561.0), (1162.0, 561.0), (772.0, 560.0), (392.0, 426.0), (776.0, 561.0), (394.0, 425.0), (393.0, 430.0), (391.0, 110.0), (393.0, 429.0), (388.0, 751.0), (389.0, 426.0), (771.0, 559.0), (390.0, 427.0), (393.0, 426.0), (391.0, 747.0), (772.0, 554.0), (770.0, 554.0), (394.0, 426.0), (389.0, 433.0), (1159.0, 944.0), (1157.0, 939.0), (2306.0, 937.0), (2698.0, 1322.0), (2694.0, 1323.0), (2691.0, 1323.0), (3082.0, 937.0), (2698.0, 1325.0), (2695.0, 1323.0), (2691.0, 1323.0), (3079.0, 1327.0), (3076.0, 1329.0), (3464.0, 1328.0), (3848.0, 1325.0), (3850.0, 1329.0), (3845.0, 937.0), (3845.0, 940.0), (3842.0, 1327.0), (3845.0, 938.0), (3844.0, 554.0), (4229.0, 559.0), (3847.0, 557.0), (4234.0, 938.0), (4228.0, 561.0), (2314.0, 555.0), (2313.0, 557.0), (2312.0, 557.0), (2306.0, 174.0), (2310.0, 554.0), (2311.0, 553.0), (2306.0, 557.0), (2310.0, 556.0), (2310.0, 557.0), (2306.0, 173.0), (1543.0, 558.0), (1160.0, 560.0), (1156.0, 559.0), (1159.0, 556.0), (773.0, 556.0), (774.0, 559.0), (1155.0, 941.0), (778.0, 940.0), (776.0, 554.0), (772.0, 558.0), (777.0, 942.0), (776.0, 942.0), (770.0, 557.0), (774.0, 941.0), (773.0, 943.0), (774.0, 939.0), (770.0, 561.0), (775.0, 938.0), (1155.0, 560.0), (773.0, 938.0), (1160.0, 941.0), (2693.0, 938.0), (3458.0, 1329.0), (3466.0, 1323.0), (3459.0, 1328.0), (3464.0, 1321.0), (3459.0, 1326.0), (3849.0, 1710.0), (3464.0, 1708.0), (2694.0, 1711.0), (2693.0, 1709.0), (2696.0, 1705.0), (2692.0, 2481.0)]
# Initial Values
minX = 1e99
minY = 1e99
maxX = -1e99
maxY = -1e99
for frame in movement_history:
    minX = min(frame[0], minX)
    minY = min(frame[1], minY)
    maxX = max(frame[0], maxX)
    maxY = max(frame[1], maxY)
print("MinMax", minX, minY, maxX, maxY)

# Calculate Scalefactors
x_scale_factor, y_scale_factor = findScaleFactor(minX, minY, maxX, maxY)
print("x and y scale factors: ", x_scale_factor, y_scale_factor)
# AddingWhiteNoise option flag
ADD_RANDOM_NOISE = True

"""Perform coordinate Adjustments according to the current resolution"""
background = cv2.imread('./sample_data/sampleBackground.jpg')
trajectory_points = []
heatmap = np.zeros_like(background[:, :, 0], np.float32)  # Use float32 for better precision

for idx, frame in enumerate(movement_history):
    x, y = translatePoint(frame[0], frame[1], x_scale_factor, y_scale_factor)
    if ADD_RANDOM_NOISE:
        x, y = addWhiteNoise(x, y)

    # # Deal with out-of-bound values
    # if x > 1920:
    #     x = 1910
    # if y > 1080:
    #     y = 1070
    # if x < 0:
    #     x = 1
    # if y < 1:
    #     y = 1
    
    
    x = int(x)
    y = int(y)

    print(x, y)
    # Update the heatmap
    heatmap[y, x] += 1

    # Update trajectory paths
    trajectory_points.append((x, y)) # add it to trajectory

    """Interpolate between points"""
    if idx > 0:
        prev_x, prev_y = trajectory_points[idx - 1]
        num_points = int(np.hypot(x - prev_x, y - prev_y)) // 4 # Number of points to interpolate based on the Euclidean distance between the points
        x_values = np.linspace(prev_x, x, num_points)
        y_values = np.linspace(prev_y, y, num_points)
        for px, py in zip(x_values, y_values):
            heatmap[int(py), int(px)] += 1

# Apply Gaussian blur to the heatmap
heatmap_blurred = cv2.GaussianBlur(heatmap, (201, 201), 0)  # Use a larger kernel size for more smoothing

# Normalize the blurred heatmap to 8-bit range
heatmap_normalized = cv2.normalize(heatmap_blurred, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# Apply the colormap
heatmap_img = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)

image_dir = './sample_data/heatmaptracks/'
image_urls = []
for idx, frame in enumerate(movement_history):
    if frame == (None, None):
        continue
    image = background.copy()
    print(f"processing image {idx}")
    super_imposed_img = cv2.addWeighted(heatmap_img, 0.5, image, 0.5, 0)
    # Save the image
    img_url = image_dir + f'{idx}.jpg'
    cv2.imwrite(img_url, super_imposed_img)
    image_urls.append(img_url)


"""Read and save as Video"""

# Specify the output video file name
output_video_path = './sample_data/output_video_heatmap.avi'

# # Get the first image to initialize the video writer
first_image = cv2.imread(image_urls[0])
height, width, layers = first_image.shape
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs like 'MJPG' or 'MP4V'
video_writer = cv2.VideoWriter(output_video_path, fourcc, 30, (width, height))

# Loop through the image files and write each frame to the video
for image_file in image_urls:
    frame = cv2.imread(image_file)
    video_writer.write(frame)

# Release the video writer
video_writer.release()

print(f"Video saved to: {output_video_path}")

