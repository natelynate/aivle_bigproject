"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import cv2
from models.pupil_tracker import GazeTracking
import random

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

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
        vertical_ratio = displacement_ratios['up']
    return horizontal_ratio, vertical_ratio

def addWhiteNoise(x, y):
    return x + random.choice([i for i in range(1, 10)]) , y + random.choice([i for i in range(1, 10)])  


"""Get Baseline points"""
ref_pixel_values = {'center':(960, 540), 'left':(1920, 540), 'right':(0, 540), 'up':(960, 0), 'down':(960, 1080)}
baseline_coords = {'center':[None, None], 'left':None, 'right':None, 'up':None, 'down':None}
displacement_ratios = {'left':None, 'right':None, 'up':None, 'down':None}

for reference_point in ['center', 'left', 'right', 'up', 'down']:
    waitForInput(reference_point) # wait for control input
    baseline_coords[reference_point] = capturePoint(webcam, gaze, reference_point, baseline_coords) # capture pupil coord

"""Calculate displacement ratios for all four directions relative to the center point"""
for reference_point in ['left', 'right']:
    displacement_ratios[reference_point] = 1920 / abs(baseline_coords['center'][0] - baseline_coords[reference_point][0])

for reference_point in ['up', 'down']:
    displacement_ratios[reference_point] = 1080 / abs(baseline_coords['center'][1] - baseline_coords[reference_point][1])

print("------------------------------------------------------")
print("BASELINE PUPIL COORDINATES")
for ref in baseline_coords:
    print(ref, baseline_coords[ref])
print("------------------------------------------------------")
for ratio in displacement_ratios:
    print(ratio, displacement_ratios[ratio])

print("***************************************************************************")
print("***************************************************************************")

movement_history = [] # empty movement history list
ADD_RANDOM_NOISE = 0
print("Recording pupil movements")
for _ in range(10):
    print(".")

f = 0
while True:
    f += 1
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
        pixel_x = (horizontal_displacement * horizontal_ratio) + baseline_coords['center'][0]
        pixel_y = (vertical_displacement * horizontal_ratio) + baseline_coords['center'][1]
        
        if pixel_x < 0:
            pixel_x *= -1 
        if pixel_y < 0:
            pixel_y *= -1 
        new_pxl_of_interest_x, new_pxl_of_interest_y = addWhiteNoise(pixel_x, pixel_y)

        movement_history.append((new_pxl_of_interest_x, new_pxl_of_interest_y))
        print(f"new movement history added. {f}th frame")
    except:
        resp = input("continue?(Y/N): ") 
        if resp == 'Y':
            continue
        else:
            break

print("**************************************")
print("finished trial recording")        

print(movement_history)
background = cv2.imread('./sample_data/screen.jpg')

# while True:
for frame in movement_history:
    x, y = int(frame[0]), int(frame[1])
    if not (0 < x < 1920) or not (0 < y < 1080):
        continue
    image = cv2.circle(background, (x, y), radius=5, color=(20, 255, 20), thickness=-1)
    cv2.imshow('dot', image)

cv2.waitKey(0)
cv2.destroyAllWindows()
