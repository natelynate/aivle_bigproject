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
        seconds = 3
        FRAME_PER_SEC = 24
        frames = []
        for _ in range(24 * 4):
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
