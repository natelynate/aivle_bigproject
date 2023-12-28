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
    if request.method == 'POST':
        table_name = 'Test_taker_information'
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
            insert(f"""INSERT INTO {table_name} (test_id, test_taker_id, center_left_x, center_left_y, center_right_x, center_right_y) 
                       VALUES ('{test_id}', '{test_taker_id}', {ref[0][0]}, {ref[0][1]}, {ref[1][0]}, {ref[1][1]});""")
            return {'sucess':f"True. {loc_tag}={ref}'s been saved to the database"}
          
        else:
            # Load central reference point at the center
            center_ref = read(f"""SELECT center_left_x, center_left_x, center_right_x, center_right_y
                                  FROM {table_name}
                                  WHERE test_id = '{test_id}' AND test_taker_id = '{test_taker_id}';""")[0]
                              
            center_ref = ((center_ref[0], center_ref[1]), (center_ref[2], center_ref[3]))
            
            new_ref = pupil_movement[0]
            if ref_is_valid(new_ref, center_ref, loc_tag):
                # save new reference point and displacement_ratio
                update(f"""UPDATE {table_name} SET {loc_tag+'_left_x'}={new_ref[0][0]},
                                                   {loc_tag+'_left_y'}={new_ref[0][1]},
                                                   {loc_tag+'_right_x'}={new_ref[1][0]},
                                                   {loc_tag+'_right_y'}={new_ref[1][1]}
                                               WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""")  
                
                displacement_ratio = get_displacement_ratios((new_ref[1][0], new_ref[1][1]), (center_ref[1][0], center_ref[1][1]), loc_tag)

                update(f"""UPDATE {table_name} SET {'displacement_ratio_'+loc_tag} = {displacement_ratio}
                                               WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""")  
                
                print("new_ref: ", new_ref, "displacementRatio: ", displacement_ratio)
                return {'result':True, 'location_tag':loc_tag, 'new_ref':new_ref, 'displacement':displacement_ratio} 
            else:
                return {'result':False, 'location_tag':loc_tag}
            
    
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
        table_name = 'Test_taker_information'
        try:
            frames = request.get_json()['frames'] # base64 encoded frames
            test_id = request.get_json()['test_id']
            test_taker_id = request.get_json()['test_taker_id']
            screen = request.get_json()['screen']
            boundingbox = request.get_json()['boundingbox']
            
            print(test_id)
            print(test_taker_id)
            print(boundingbox)
        except:
            return {'error_message':'unclear or incomplete payload information in the request json'}
        try:
            pupil_movements = record_pupil_movements(frames) # record pupil movements after performing decoding
            print("Decoding successfull")
            print(pupil_movements)
           
            
            displacement_ratios = read(f"""SELECT displacement_ratio_left, displacement_ratio_right, displacement_ratio_up, displacement_ratio_down
                                           FROM {table_name}
                                           WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""")[0]
            displacement_ratios = {loc:ratio for loc, ratio in zip(['center', 'left', 'right', 'up', 'down'], displacement_ratios)}  
            print("displacement_ratios: ", displacement_ratios)                         
            
            pixel_movements = process_pupil_movements(pupil_movements, displacement_ratios) # translate pupil coordinates to pixels
            print(pixel_movements)
            print("finished translation to pixel")
            print(pixel_movements[0], pixel_movements[1])
            OOI_analysis_result = deduce_object_of_interest(pixel_movements, boundingbox)
            print()
            # Save analysis results to DB
            # insert() # save trajectory info
            # insert() # save OOI analysis result 
            return {'success':True, 'result':OOI_analysis_result}
        except:
            return {'success':False, 'result':0}
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105) 
    