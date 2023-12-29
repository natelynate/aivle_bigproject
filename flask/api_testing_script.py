# This is a script file for testing the RESTful API Functionalities of the project

import json
import requests
import cv2
import base64
from models.pupil_tracker import GazeTracking

# SET TESTING TARGET
task = 'ab' # ref/AB

if task == 'ref':
        url = 'http://127.0.0.1:105/api/eyetrack/reference'
        coords = [(1920//2, 1080//2), (0, 1080//2), (1920, 1080//2), (1920//2, 0), (1920//2, 1080)]
        locs = ['center', 'left', 'right', 'up', 'down']
        for idx, loc_tag in enumerate(locs):
                coord = coords[idx]
                image = cv2.imread(f'./sample_data/eyetracking_src/{loc_tag}.jpg')
                encoded_image = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
                headers = {'content-type':'application/json'}
                payload =  {'frames':[encoded_image for _ in range(24)], 
                        'test_id':'sample_test1',
                        'test_taker_id':'yoonkihwa',
                        'pixel_x':coord[0],
                        'pixel_y':coord[1],
                        'location_tag':loc_tag}
                response = requests.post(url, headers=headers, data=json.dumps(payload))           
                print("For ref point task", loc_tag, response.text)
                print("=====================================================")

if task == 'ab':
        url = 'http://127.0.0.1:105/api/eyetrack/ab'
        headers = {'content-type':'application/json'}
        cap = cv2.VideoCapture('./sample_data/eyetracking_src/gaze.mp4')
        seconds = 4
        FRAME_PER_SEC = 24
        frames = []
        for _ in range(24 * seconds):
                ret, frame = cap.read() # frame is an numpy array
                if not ret:
                        break
                # encoded_frame = base64.b64encode(frame).decode()
                encoded_frame = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()
                # print(encoded_frame[:10])
                frames.append(encoded_frame)
        screen = cv2.imread(f'./sample_data/eyetracking_src/screen.jpg')
        encoded_screen = base64.b64encode(cv2.imencode('.jpg', screen)[1]).decode()
        headers = {'content-type':'application/json'}
        payload =  {'frames':frames,
                    'test_id':'sample_test1',
                    'test_taker_id':'yoonkihwa',
                    'screen':encoded_screen,
                    'boundingbox':{'object1':((100, 100), (900, 1600)), 'object2':((1100, 100), (1900, 1600))}} 
        response = requests.post(url, headers=headers, data=json.dumps(payload))      
        print("For a/b test task", response.text)     


def findQuadrant(x, y):
        center_x, center_y = center_ref
        horizontal_ratio, vertical_ratio = 0, 0
        if x < center_x:
                horizontal_ratio = displacement_ratio['left']
        else:
                horizontal_ratio = displacement_ratio['right']
        if y < center_y:
                vertical_ratio = displacement_ratio['up']
        else:
                vertical_ratio = displacement_ratio['down']
        return horizontal_ratio, vertical_ratio

def convert2pixel(x, y):
        """Convert pupil coordination to pixel coordination"""
        center_x, center_y = center_ref

        # Get horizontal and Vertical displacement ratio to use
        horizontal_ratio, vertical_ratio = findQuadrant(x, y)
        
        # Calculate Displacements
        if x > center_x: # x is right from center
            horizontal_displacement = x - center_x
        else: # x is left from center 
            horizontal_displacement = center_x - x
        if y < center_y: # y is above center
            vertical_displacement = y - center_y
        else: # y is below center
            vertical_displacement = center_y - y 
        
        # Convert pupil displacements into pixelwise displacement
        pixel_displacement_x = horizontal_displacement * horizontal_ratio
        pixel_displacement_y = vertical_displacement  * vertical_ratio

        new_x, new_y = center_x + pixel_displacement_x, center_y + pixel_displacement_y
        
            
        return int(new_x), int(new_y)


# if __name__ == '__main__':       
#         pixel_movements = []        
#         addNoise=True
#         center_ref = (718, 315)
#         displacement_ratio = {'left': 73.85, 'right': 137.14, 'up': 135.0, 'down': 54.0}
#         pupil_movements = [[(551, 319), (709, 317)], [(550, 320), (708, 317)], [(550, 320), (709, 317)], [(554, 320), (710, 317)], [(552, 320), (709, 317)], [(552, 320), (710, 317)], [(552, 320), (709, 317)], [(552, 320), (710, 317)], [(553, 320), (710, 317)], [(553, 319), (710, 317)], [(555, 320), (712, 318)], [(557, 320), (715, 317)], [(557, 320), (715, 317)], [(558, 321), (715, 318)], [(558, 321), (715, 318)], [(558, 321), (715, 317)], [(558, 321), (715, 318)], [(557, 321), (715, 318)], [(557, 321), (715, 317)], [(557, 321), (715, 319)], [(557, 321), (715, 318)], [(557, 321), (716, 318)], [(557, 321), (715, 318)], [(557, 321), (715, 318)], [(557, 321), (715, 318)], [(556, 321), (714, 318)], [(555, 321), (712, 318)], [(555, 321), (712, 318)], [(554, 321), (712, 319)], [(554, 322), (712, 318)], [(554, 322), (712, 319)], [(555, 322), (712, 318)], [(555, 322), (712, 319)], [(555, 322), (712, 319)], [(554, 322), (712, 319)], [(555, 322), (712, 319)], [(554, 322), (712, 319)], [(554, 322), (712, 320)], [(555, 322), (712, 319)], [(554, 322), (712, 318)], [(555, 321), (713, 318)], [(555, 322), (713, 318)], [(555, 321), (713, 318)], [(555, 322), (712, 319)], [(555, 324), (710, 322)], [(548, 327), (705, 325)], [(546, 325), (701, 324)], [(539, 324), (702, 320)], [(544, 322), (703, 319)], [(544, 321), (703, 317)], [(544, 321), (703, 318)], [(544, 321), (703, 318)], [(544, 321), (703, 318)], [(544, 321), (703, 317)], [(543, 321), (703, 318)], [(544, 322), (703, 318)], [(544, 320), (703, 318)], [(543, 
# 320), (703, 317)], [(544, 320), (703, 317)], [(544, 321), (704, 318)], [(544, 321), (704, 317)], [(544, 321), (703, 317)], [(543, 321), (702, 318)], 
# [(543, 320), (701, 318)], [(543, 320), (701, 318)], [(543, 320), (701, 318)], [(543, 320), (700, 318)], [(542, 320), (700, 318)], [(542, 320), (700, 
# 318)], [(542, 320), (700, 318)], [(542, 320), (700, 318)], [(542, 321), (700, 319)], [(542, 320), (700, 318)], [(542, 320), (700, 318)], [(542, 320), (701, 319)], [(542, 321), (701, 319)], [(542, 321), (700, 319)], [(542, 320), (700, 318)], [(541, 321), (700, 320)], [(541, 321), (699, 319)], [(541, 321), (699, 320)], [(541, 321), (698, 320)], [(541, 321), (698, 320)], [(541, 322), (699, 320)], [(541, 321), (698, 319)], [(540, 321), (699, 319)], [(541, 322), (699, 319)], [(541, 322), (699, 320)], [(540, 322), (698, 320)], [(540, 322), (699, 320)], [(539, 322), (699, 320)], [(540, 322), (699, 320)], [(540, 322), (699, 319)], [(541, 322), (699, 320)], [(540, 322), (699, 320)]]

#         for coord in pupil_movements:
#                 x, y = coord[1][0], coord[1][1]
#                 pixel_x, pixel_y = convert2pixel(x, y)
#                 print(pixel_x, pixel_y)
        