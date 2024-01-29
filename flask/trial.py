from logic.process import *
from logic.db import * 
import math
import cv2
import pyautogui
import random
from models.pupil_tracker import GazeTracking

# load data saved as text file
xs, ys = [], []
with open('./sample_data/pixels.txt', 'r') as r:
    rr = r.readlines()
    for coord in rr:
        x, y = coord.split(',')
        
        xs.append(int(math.ceil(float(x))))
        ys.append(int(math.ceil(float(y))))


# Get the screen size
screen_width, screen_height = pyautogui.size()
screen = cv2.imread('./sample_data/eyetracking_src/single_stimulus_2.jpg')
# for x, y in zip(xs, ys):
#     image = cv2.circle(image, (x, y), radius=20,
#                        color=(0, 0, 255), thickness=-1)

# cv2.imshow('dot', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def get_heatmap(xs, ys):                                 
    # Create empty np.array 
    heatmap = np.ones_like(screen[:, :, 0], np.float32)  # Use float32 for better precision
    
    # for i in range(heatmap.shape[0]):
    #     for j in range(heatmap.shape[1]):
    #         heatmap[j][i] += 1

    # Interpolate between points
    addNoise = True
    for idx in range(len(xs)):
        if idx > 0:
            x, y = xs[idx], ys[idx]
            prev_x, prev_y = int(xs[idx-1]), int(ys[idx-1]) 
            num_points = np.hypot(x - prev_x, y - prev_y) // 4 # Number of points to interpolate based on the Euclidean distance between the points
            x_values = np.linspace(prev_x, x, int(num_points), endpoint=True)
            y_values = np.linspace(prev_y, y, int(num_points), endpoint=True)
            for px, py in zip(x_values, y_values):
                if addNoise:
                    npx = addWhiteNoise(px, mean=3, std_dev=2)
                    npy = addWhiteNoise(py, mean=3, std_dev=2)
                    try:
                        heatmap[int(npy), int(npx)] += 3
                        heatmap[int(npy)+random.choice([-1, -2, 0, 1, 2, 3]), int(npx)] += 1
                        heatmap[int(npy)+random.choice([-1, -2, 0, 1, 2, 3]), int(npx)] += 1
                        heatmap[int(npy), int(npx)+random.choice([-1, -2, 0, 1, 2, 3])] += 1
                        heatmap[int(npy), int(npx)+random.choice([-1, -2, 0, 1, 2, 3])] += 1
                    except:
                        pass
            heatmap[int(y), int(x)] += 1
    # Apply Gaussian blur to the heatmap
    heatmap_blurred = cv2.GaussianBlur(heatmap, (401, 401), 0)  # Use a larger kernel size for more smoothing
    # Normalize the blurred heatmap to 8-bit range
    heatmap_normalized = cv2.normalize(heatmap_blurred, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # Superimpose heatmap to the uploaded screen image
    # Apply the colormap
    heatmap_img = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)
    super_imposed_img = cv2.addWeighted(heatmap_img, 0.5, screen, 0.5, 0)
    cv2.imshow('super_imposed_img', super_imposed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('./sample_data/heatmap.jpg', super_imposed_img)

def get_trajectory(xs, ys):
    test_id = 'SAMPLE1'
    test_taker_id = 'SAMPLE100'
    save_location = './sample_data/videoframes/'
    output_video_path = f'./sample_data/{test_id}_{test_taker_id}.avi'
    screen = cv2.imread('./sample_data/eyetracking_src/single_stimulus_2.jpg')
    trajectory = []
    frames = []
    for idx in range(len(xs)):
        x, y = int(xs[idx]), int(ys[idx])
        trajectory.append((x, y)) # add it to trajectory
        screen = cv2.circle(screen, (int(x), int(y)), radius=5, color=(20, 255, 20), thickness=-1) 
        if len(trajectory) > 1:
            for j in range(1, len(trajectory)):
                color = max(0, 255 - j * 10)  
                screen = cv2.line(screen, trajectory[j - 1], trajectory[j], (0, 0, color), thickness=1)
        cv2.imwrite(save_location + f'{idx}.jpg', screen)
        print("saved at ", save_location + f'{idx}.jpg')
        frames.append(screen.copy())
        
     
    last_image = frames[0]
    height, width, layers = last_image.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs like 'MJPG' or 'MP4V'
    video_writer = cv2.VideoWriter(output_video_path, fourcc, 24, (width, height))
    for frame in frames:
        video_writer.write(frame)
    print("video file saved at ", output_video_path)


def get_labeled_video():
    cap = cv2.VideoCapture('./sample_data/eyetracking_src/gaze2.mp4')
    gaze = GazeTracking()
    output_video_path = f'./sample_data/pupiltracking.avi'
    frames = []
    for _ in range(24 * 4):
        ret, frame = cap.read()
        gaze.refresh(frame)
        if not ret:
            break
        frame = gaze.annotated_frame()
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        frames.append(frame)

    # Save as video clip
    last_image = frames[0]
    height, width, layers = last_image.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs like 'MJPG' or 'MP4V'
    video_writer = cv2.VideoWriter(output_video_path, fourcc, 24, (width, height))
    for frame in frames:
        video_writer.write(frame)
    print("video file saved at ", output_video_path)

get_heatmap(xs, ys)
get_trajectory(xs, ys)
get_labeled_video()