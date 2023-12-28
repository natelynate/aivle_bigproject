"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import cv2
from models.pupil_tracker import GazeTracking
import random
import numpy as np

def waitForInput(ref):
    print("=" * 30)
    print(f"Getting baseline for {ref}")
    if input("continue?(Y/N): ") == 'Y':
        return
    else:
        raise ValueError("Forced Quit")

def capturePoint(webcam, gaze, vector, baseline_coords):
    """referencing eye=right"""
    while True:
        _, frame = webcam.read()
        gaze.refresh(frame)
        try:
            pupil_baseline_x, pupil_baseline_y = gaze.pupil_right_coords()
            center_x, center_y = baseline_coords['center']

            if vector != 'center':
                if vector == 'left':
                    if pupil_baseline_x >= center_x:
                        print(f"baseline recording for left = {pupil_baseline_x}, {pupil_baseline_y} is not a viable recording compared to center ref {center_x}, {center_y}")
                        if input("Press Y to retake: "):
                            continue
                if vector == 'right':
                    if pupil_baseline_x <= center_x:
                        print(f"baseline recording for right = {pupil_baseline_x}, {pupil_baseline_y} is not a viable recording compared to center ref {center_x}, {center_y}")
                        if input("Press Y to retake: "):
                            continue
                if vector == 'up':
                    if pupil_baseline_y >= center_y:
                        print(f"baseline recording for up = {pupil_baseline_x}, {pupil_baseline_y} is not a viable recording compared to center ref {center_x}, {center_y}")
                        if input("Press Y to retake: "):
                            continue
                if vector == 'down':
                    if pupil_baseline_y <= center_y:
                        print(f"baseline recording for down = {pupil_baseline_x}, {pupil_baseline_y} is not a viable recording compared to center ref {center_x}, {center_y}")
                        if input("Press Y to retake: "):
                            continue
        except: # 못 잡았으면 반복
            continue
        print(pupil_baseline_x, pupil_baseline_y)
        if input("save the current baseline point?(Y/N): ") == 'Y':
            return pupil_baseline_x, pupil_baseline_y
        else:
            continue

def findQuadrant(x, y):
    center_x, center_y = baseline_coords['center']
    horizontal_ratio, vertical_ratio = 0, 0
    if x < center_x:
        horizontal_ratio = displacement_ratios['left']
    else:
        horizontal_ratio = displacement_ratios['right']
    if y < center_y:
        vertical_ratio = displacement_ratios['up']
    else:
        vertical_ratio = displacement_ratios['down']
    return horizontal_ratio, vertical_ratio

def addWhiteNoise(x, y, mean=20, std_dev=10):
    """Add white noise to the pixel coordinates"""
    noise_x = np.random.normal(loc=mean, scale=std_dev)
    noise_y = np.random.normal(loc=mean, scale=std_dev)
    return x+noise_x, y+noise_y
    
"""Get Baseline points"""
ref_pixel_values = {'center':(960, 540), 'left':(1920, 540), 'right':(0, 540), 'up':(960, 0), 'down':(960, 1080)}
baseline_coords = {'center':[None, None], 'left':None, 'right':None, 'up':None, 'down':None}
displacement_ratios = {'left':None, 'right':None, 'up':None, 'down':None}

"""Get webcam and create cv2.VideoCapture object"""
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

"""Capture reference points for 5 zones"""
for reference_point in ['center', 'left', 'right', 'up', 'down']:
    waitForInput(reference_point) # wait for control input
    baseline_coords[reference_point] = capturePoint(webcam, gaze, reference_point, baseline_coords) # capture pupil coord

"""Calculate displacement ratios for all four directions relative to the center point"""
for reference_point in ['left', 'right']:
    displacement_ratios[reference_point] = 960 / abs(baseline_coords['center'][0] - baseline_coords[reference_point][0])

for reference_point in ['up', 'down']:
    displacement_ratios[reference_point] = 540 / abs(baseline_coords['center'][1] - baseline_coords[reference_point][1])

print("------------------------------------------------------")
print("BASELINE PUPIL COORDINATES")
for ref in baseline_coords:
    print(ref, baseline_coords[ref])
print("------------------------------------------------------")
print("DISPLACEMENT RATIOS FOR ALL DIRECTIONS")
for ratio in displacement_ratios:
    print(ratio, displacement_ratios[ratio])

print("***************************************************************************")
print("***************************************************************************")

if input("Proceed to live recording?") == 'Y':
    pass
else:
    raise ValueError("Script manually terminated")   

movement_history = [] # empty movement history list
ADD_RANDOM_NOISE = True
print("Recording pupil movements")
for _ in range(10):
    print(".")

f = 0
duration = 300 # Number of frames to capture
for frame_num in range(duration):
    # We get a new frame from the webcam
    _, frame = webcam.read()
    gaze.refresh(frame)
    try:
        right_pupil_x, right_pupil_y = gaze.pupil_right_coords()
        # find which displacement ratio to use
        horizontal_ratio, vertical_ratio = findQuadrant(right_pupil_x, right_pupil_y)

        # Compute pupil displacements
        horizontal_displacement = baseline_coords['center'][0] - right_pupil_x
        vertical_displacement = baseline_coords['center'][1] - right_pupil_y

        # Compute the corresponding pixel coordinates
        pixel_x = (horizontal_displacement * horizontal_ratio) + baseline_coords['center'][0]
        pixel_y = (vertical_displacement * vertical_ratio) + baseline_coords['center'][1]
        
        # Deal with negative pixel coords
        # if pixel_x < 0:
        #     pixel_x *= -1 
        # if pixel_y < 0:
        #     pixel_y *= -1
        if ADD_RANDOM_NOISE: 
            pixel_x, pixel_y = addWhiteNoise(pixel_x, pixel_y)

        movement_history.append((pixel_x, pixel_y))
        print(f"new movement history added. {frame_num}th frame")
    except:
        movement_history.append((None, None)) # if no pupil is detected, add (None None) tuple instead. 

print("**************************************")
print("finished trial recording")        

# Save movement_history
movement_history = [frame for frame in movement_history if frame != (None, None)]
print(movement_history)