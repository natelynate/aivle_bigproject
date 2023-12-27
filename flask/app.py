from flask import Flask, request
import tempfile
import os
import pymysql
import base64
from pathlib import Path
from logic.db import * # import db setup functions
from logic.process_img import * # import image processing functions
from models.pupil_tracker import GazeTracking

app = Flask(__name__)

# import sentiment inference model
model_dir = 'models/sentiment_analyzer'
model = tf.keras.models.load_model(model_dir)

"""POST action for submitting media files from FE to Flask"""
# Submitting Individual image
@app.route('/api/image_upload', methods=['POST'])
def upload_image():
    jpg_original = base64.b64decode(request.get_json()['baseline_img'])
    img_binary = preprocess_image(jpg_original)
    sentiment_probs = model.predict(img_binary)[0]
    return {'data':{'anger':float(sentiment_probs[0]),
                'disgust':float(sentiment_probs[1]),
                'fear':float(sentiment_probs[2]),
                'sadness':float(sentiment_probs[3]),
                'surprise':float(sentiment_probs[4])}}

# Submitting webm video clip
@app.route('/api/video_upload/test', methods=['POST'])
def test():
        return None

@app.route('/api/process_video', methods=['POST'])
def process_video():
    # video_data = request.get_data()
    video = request.files['video']
    with tempfile.TemporaryDirectory() as td:
        temp_filename = Path(td) / 'uploaded_video'
        video.save(temp_filename)

    vidCapObj = cv2.VideoCapture(str(temp_filename) + '.mp4')    
    while True: 
        ret, frame = vidCapObj.read()
        print(frame)
        if not ret:
            break
        cv2.imshow("Demo", frame)

    vidCapObj.release()
    cv2.destroyAllWindows()

    # for frame in video_stream:
    #     frames.append(frame)
    # return {'msg':'Video processed successfully',
    #         'frame':frames}
    return {'data':None}

# Submitting video clip frames for eyetracking
@app.route('/api/eyetrack', methods=['POST'])
def eyetrack():
    """input = 1) frames (24)
                2) tasktype ('get_ref', 'perget_json()_AB')
                3) project_id 
                4) testtaker_id
                5) image_id (if tasktype is 'perget_json()_AB') 
                6) pixel_x (if tasktype is 'get_ref')
                7) pixel_y (if tasktype is 'get_ref')
                8) object_locations (if tasktype is 'perget_json()_AB')"""
    try:
        project_id = request.get_json()['project_id']
        testtaker_id = request.get_json()['testtaker_id']
    except:
        return {'error_message':'unclear project_id and testtaker_id'}
    
    try:
        gaze = GazeTracking()
        PUPILS = []
        FRAMES = request.get_json()['frames'] #base64 encoded frames
        for frame_num, frame in enumerate(FRAMES):
            img = decode_image(frame)
            gaze.refresh(img)
            if gaze.pupil_left_coords() and gaze.pupil_right_coords():
                left_pupil, right_pupil = gaze.pupil_left_coords(), gaze.pupil_right_coords()
                entry = [[int(left_pupil[0]), int(left_pupil[1])],
                         [int(right_pupil[0]), int(right_pupil[1])],
                         ]
                PUPILS.append(entry)
            else:
                print(f"No pupil detected for frame {frame_num}")
                PUPILS.append((None, None))
    except:
        return {'error_message':'unable to retreive the video file from flask backend.'}
    
    return {'result':PUPILS}

    # Obtain np.array frames and corresponding pupil coordinates
    if request.get_json()['tasktype'] == 'get_ref':
        pixel_x = request.get_json()['pixel_x']
        pixel_y = request.get_json()['pixel_y']

        if check_ref(PUPILS):
            avg_pupil_x, avg_pupil_y = get_avg_pupil(PUPILS) # Get the average pupil coordinates
            ref = calculate_ref(pixel_x, pixel_y, avg_pupil_x, avg_pupil_y)
            # save the ref point information in the DB
            ### DB logging with testtaker_id, project_id
            return {'result':True}
        else:
            return {'result':False}
        
    elif request.get_json()['tasktype'] == 'perget_json()_AB':
        # perget_json() A/B task
        object_locs = request.get_json()['object_locations']
        ref = None # Load ref point from DB by keying with test_taker_id and 
        pixel_coords = transform_to_pixel(PUPILS, ref)
        pixel_coords = interpolate_gazetrack(pixel_coords)
        gazehits = deduce_object_of_interest(pixel_coords, object_locs)
        return {'result':True, 'state_message':'model ran successfully'}

        ### DB Logging
        # pixel_coords
        # gazehits
    else:
        return {'error_message':'unclear request type. Check if the tasktype value is one of "get_ref" or "perget_json()_AB".'}
    

"""POST actions for DB manipulation tasks"""
@app.route('/api/db/login', methods=['GET'])
def login():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return {'resp':users}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105) 
    