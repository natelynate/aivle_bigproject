# This is a script file for testing the RESTful API Functionalities of the project

import json
import requests
import cv2
import base64
from logic.db import *
from logic.process import decode_image
from models.pupil_tracker import GazeTracking
import random


headers = {'content-type':'application/json'}

def check_conn():
    url = 'http://3.35.220.17:5000/base'
    payload = {}
    response = requests.get(url, headers=headers, data=json.dumps(payload))     
    print("For ref point task", response.text)


def api_test(task, test_id, test_taker_id):
    coords = [(1920//2, 1080//2), (0, 1080//2), (1920, 1080//2), (1920//2, 0), (1920//2, 1080)]
    locs = ['center', 'left', 'right', 'up', 'down'] 
    URL_BASE = 'http://3.35.220.17:5000/api/'
    SRC_BASE = './sample_data/eyetracking_src/'

    if task == 'ref':
        url = URL_BASE + 'eyetrack/reference'
        print(url)
        for idx, loc_tag in enumerate(locs):
            coord = coords[idx]
            image = cv2.imread(SRC_BASE + f'{loc_tag}.jpg')
            encoded_image = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
            payload =  {'frames':[encoded_image for _ in range(24)], 
                        'test_id':test_id,
                        'test_taker_id':test_taker_id,
                        'pixel_x':coord[0],
                        'pixel_y':coord[1],
                        'location_tag':loc_tag}
            response = requests.post(url, headers=headers, data=json.dumps(payload))           
            print("For ref point task", loc_tag, response.text)
            print("=====================================================")
            
    if task == 'ab':
        url = URL_BASE + 'eyetrack/ab'
        cap = cv2.VideoCapture(SRC_BASE + 'gaze.mp4')
        seconds = 4
        FRAME_PER_SEC = 24
        frames = []
        for _ in range(FRAME_PER_SEC * seconds):
            ret, frame = cap.read() # frame is an numpy array
            if not ret:
                break
            encoded_frame = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()
            frames.append(encoded_frame)
            payload =  {'frames':frames,
                        'test_id':test_id,
                        'test_taker_id':test_taker_id,
                        'boundingbox':{'object1':((100, 100), (900, 1600)), 'object2':((1100, 100), (1900, 1600))}} 
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))      
        print("For a/b test task", response.text)     

    if task =='heatmap':
        url = URL_BASE + 'dashboard/visualize/heatmap'
        screen = cv2.imread('./sample_data/eyetracking_src/screen.jpg')
        encoded_frame = base64.b64encode(cv2.imencode('.jpg', screen)[1]).decode()
        test_id = test_id
        test_taker_id = test_taker_id
        payload = {'test_id':'sample_test1',
                   'test_taker_id':'yoonkihwa',
                   'screen':encoded_frame}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            heatmap = response.json()['result_image']
            heatmap = decode_image(heatmap)
            save_location = f'./sample_data/{test_id}_{test_taker_id}_{task}.jpg'
            cv2.imwrite(save_location, heatmap)
            print(f"image returned as jpg as {save_location}")

    if task =='trajectory':
        url = URL_BASE + 'dashboard/visualize/trajectory'
        screen = cv2.imread(SRC_BASE + 'screen.jpg')
        encoded_screen = base64.b64encode(cv2.imencode('.jpg', screen)[1]).decode()
        payload = {'test_id':test_id,
                   'test_taker_id':test_taker_id,
                   'screen':encoded_screen}
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        # print(response.text)
        if response.status_code == 200:
            frames = response.json()['frames']
            save_location = './sample_data/trajectory_tracks/'
            encoded_frames = []
            for idx, frame in enumerate(frames):
                encoded_frame =  decode_image(frame)
                cv2.imwrite(save_location + f'{idx}.jpg', encoded_frame)
                encoded_frames.append(encoded_frame)
                print(f"image returned as jpg as {save_location+ f'{idx}.jpg'}")
                # Create a video file
                output_video_path = f'./sample_data/{test_id}_{test_taker_id}_{task}.avi'
                last_image = encoded_frame
                height, width, layers = last_image.shape
                fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs like 'MJPG' or 'MP4V'
                video_writer = cv2.VideoWriter(output_video_path, fourcc, 24, (width, height))
                for image_file in encoded_frames:
                        video_writer.write(image_file)
                print("video file saved at ", output_video_path)

    if task == 'microexpression/baseline':
        url = URL_BASE + 'microexpression/baseline'
        cap = cv2.VideoCapture('./sample_data/eyetracking_src/gaze.mp4')
        seconds = 1
        FRAME_PER_SEC = 24
        frames = []
        for _ in range(FRAME_PER_SEC * seconds):
                ret, frame = cap.read() # frame is an numpy array
                if not ret:
                        break
                encoded_frame = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()
                # print(encoded_frame[:10])
                frames.append(encoded_frame)
        payload =  {'frames':frames,
                    'test_id':test_id,
                    'test_taker_id':test_taker_id}
        response = requests.post(url, headers=headers, data=json.dumps(payload))      
        print("Microexpression baseline", response.text)     

    if task == 'microexpression/analysis':
        url = URL_BASE + 'microexpression/analysis'
        cap = cv2.VideoCapture('./sample_data/eyetracking_src/gaze.mp4')
        seconds = 3
        FRAME_PER_SEC = 24
        frames = []
        for _ in range(FRAME_PER_SEC * seconds):
            ret, frame = cap.read() # frame is an numpy array
            if not ret:
                break
            encoded_frame = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()
            frames.append(encoded_frame)
        payload =  {'frames':frames,
                'test_id':test_id,
                'test_taker_id':test_taker_id,
                'obj_id':'OBJECT_TEXT'
                }
        response = requests.post(url, headers=headers, data=json.dumps(payload))      
        print("Microexpression analysis", response.text)  
        pass
    

if __name__ == '__main__':
    test_id = '11433'
    test_taker_id = 'a041209'
    print("Starting...")
    # check_conn()
    api_test(task='microexpression/baseline', test_id=test_id, test_taker_id=test_taker_id)
    # print("=====")
    api_test(task='microexpression/analysis', test_id=test_id, test_taker_id=test_taker_id)
    # print("=====")
    api_test(task='ref', test_id=test_id, test_taker_id=test_taker_id)
    # print("=====")
    api_test(task='ab', test_id=test_id, test_taker_id=test_taker_id)

    # #########
    # api_test(task='heatmap', test_id=test_id, test_taker_id=test_taker_id)
    # print("=====")
    # api_test(task='trajectory', test_id=test_id, test_taker_id=test_taker_id)