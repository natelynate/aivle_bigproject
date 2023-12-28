from flask import Flask, request
import tempfile
import os
import pymysql
import base64
from pathlib import Path
from logic.db import * # import db setup functions
from logic.process import *


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
    """Deprecated"""
    return None
        

# Submitting video clip frames for eyetracking
@app.route('/api/eyetrack/reference', methods=['POST'])
def get_eyetrack_ref():
    """ input = 
        1) frames(binary encoded) (24)
        2) project_id 
        3) testtaker_id
        4) pixel_x 
        5) pixel_y 
        6) location_tag (one of 'center', 'left', 'right', 'up', 'down')   
    Description: Receives Json payload containing information listed above. Calculates the reference point and scale factors and saves
                 the result at the DB table. Returns True if the above operations were performed successfully and returns False 
                 to trigger another request. 
    """ 
    table_name = 'Test_taker_information'
    if request.method == 'POST':
        try:
            frames = request.get_json()['frames'] #base64 encoded frames
            test_id = request.get_json()['test_id']
            test_taker_id = request.get_json()['test_taker_id']
            pixel_x = request.get_json()['pixel_x']
            pixel_y = request.get_json()['pixel_y']
            loc_tag = request.get_json()['location_tag']
        except:
            return {'error_message':'unclear or incomplete payload information in the request json'}
        
        pupil_movement = record_pupil_movements(frames)
        
        # If recording for center reference point, 
        if loc_tag == 'center':
            ref = pupil_movement[0]
            delete(f"""DELETE FROM {table_name} WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""")
            insert(f"""INSERT INTO {table_name} 
                       VALUES ('{test_id}', '{test_taker_id}', {ref[0][0]}, {ref[0][1]}, {ref[1][0]}, {ref[1][1]}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);""")
            return {'sucess':f"True. {loc_tag}={ref}'s been saved to the database"}  
        else:
            # Load central reference point at the center
            center_ref = read(f"""SELECT center_left_x, center_left_x, center_right_x, center_right_y
                                  FROM {table_name}
                                  WHERE test_id = '{test_id}' AND test_taker_id = '{test_taker_id}';
                              """)[0]
            center_ref = ((center_ref[0], center_ref[1]), (center_ref[2], center_ref[3]))
            
            new_ref = pupil_movement[0]
            if ref_is_valid(new_ref, center_ref, loc_tag):
                
                update(f"""UPDATE {table_name} SET {loc_tag+'_left_x'}={new_ref[0][0]},
                                                   {loc_tag+'_left_y'}={new_ref[0][1]},
                                                   {loc_tag+'_right_x'}={new_ref[1][0]},
                                                   {loc_tag+'_right_y'}={new_ref[1][1]}
                                               WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""")  
                # save new reference point
                return {'result':True, 'location_tag':loc_tag, 'new_ref':new_ref} 
            else:
                return {'result':False, 'location_tag':loc_tag, 'new_ref':new_ref}
            
    
@app.route('/api/eyetrack/ab', methods=['POST'])
def get_eyetrack_ab():
    """ input = 
        1) frames(binary encoded) (24)
        2) project_id 
        3) testtaker_id
        4) screen stillframe
        5) boundingbox coords 
    Saves = Trajectory Logs, Gazehit counts for correspondiong bounding boxes
    Returns = StateResponse
    """
    if request.method == 'POST':
        try:
            frames = request.get_json()['frames'] # base64 encoded frames
            project_id = request.get_json()['project_id']
            testtaker_id = request.get_json()['testtaker_id']
            screen = request.get_json()['screen']
            boundingbox = request.get_json()['boundingbox']
            
        except:
            return {'error_message':'unclear or incomplete payload information in the request json'}
        try:
            pupil_movements = record_pupil_movements(frames) # record pupil movements
            pixel_movements = process_pupil_movements(pupil_movements)
            
            OOI_analysis_result = deduce_object_of_interest(pixel_movements, boundingbox)
            
            # Save analysis results to DB
            insert() # save trajectory info
            insert() # save OOI analysis result 
            return {'success':True}
        except:
            return {'success':False}
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105) 
    