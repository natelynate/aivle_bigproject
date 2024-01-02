from flask import Flask, request
import tempfile
import os
import pymysql
import base64
import random
import json
from pathlib import Path
from logic.db import * # import db setup functions
from logic.process import *


app = Flask(__name__)

# import sentiment inference model
model_dir = 'models/sentiment_analyzer'
model = tf.keras.models.load_model(model_dir)

"""POST action for submitting media files from FE to Flask"""
# Submitting Individual image
@app.route('/api/microexpression/baseline', methods=['POST'])
def get_microexpression_baseline():
    if request.method == 'POST':
        table_name = 'Microexpression_Baseline'
        try: 
            test_id = request.get_json()['test_id']
            test_taker_id = request.get_json()['test_taker_id']
            frames = request.get_json()['frames']
        except: 
             return {'error_message':'unclear or incomplete payload information in the request json'}
        
        delete(f"""DELETE FROM {table_name} WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""") # delete previous record
        
        class_probs = [0, 0, 0, 0, 0, 0]
        class_names = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']
        for frame in frames:
            frame = decode_image(frame)
            processed_binary = preprocess_image(frame)
            for idx, sentiment in enumerate(model.predict(processed_binary)[0]):
                class_probs[idx] += float(sentiment)

        insert(f"""INSERT INTO {table_name} VALUES ('{test_id}', '{test_taker_id}', 
                                                     {class_probs[0]}, {class_probs[1]}, {class_probs[2]},
                                                     {class_probs[3]}, {class_probs[4]}, {class_probs[5]});""")  
        return {'result':class_probs}
    
@app.route('/api/microexpression/analysis', methods=['POST'])
def get_microexpression_analysis():
    if request.method == 'POST':
        table_name = 'Sentiment_Scores'
        try: 
            test_id = request.get_json()['test_id']
            test_taker_id = request.get_json()['test_taker_id']
            frames = request.get_json()['frames']
            obj_id = request.get_json()['obj_id']
        except: 
             return {'error_message':'unclear or incomplete payload information in the request json'}
        
        # Delete previous record if present
        delete(f"""DELETE FROM {table_name} WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""") # delete previous record
        
        class_probs = [0, 0, 0, 0, 0, 0]
        for frame in frames:
            frame = decode_image(frame)
            processed_binary = preprocess_image(frame)
            for idx, sentiment in enumerate(model.predict(processed_binary)[0]):
                class_probs[idx] += float(sentiment)

        # Add new record
        insert(f"""INSERT INTO {table_name} VALUES ('{test_id}', '{test_taker_id}', '{obj_id}', 
                                                     {class_probs[0]}, {class_probs[1]}, {class_probs[2]},
                                                     {class_probs[3]}, {class_probs[4]}, {class_probs[5]});""")  
        return {'result':class_probs}                                
     

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
        table_name = 'Pupil_ReferencePoints'
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
        table_name = 'Pupil_ReferencePoints'
        try:
            frames = request.get_json()['frames'] # base64 encoded frames
            test_id = request.get_json()['test_id']
            test_taker_id = request.get_json()['test_taker_id']
            boundingbox = request.get_json()['boundingbox']
        except:
            return {'error_message':'unclear or incomplete payload information in the request json'}
        try:
            pupil_movements = record_pupil_movements(frames) # record pupil movements after performing decoding
            displacement_ratios = read(f"""SELECT displacement_ratio_left, displacement_ratio_right, displacement_ratio_up, displacement_ratio_down
                                           FROM {table_name}
                                           WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""")[0]
            displacement_ratios = {loc:ratio for loc, ratio in zip(['left', 'right', 'up', 'down'], displacement_ratios)}        
            center = read(f"""SELECT center_right_x, center_right_y
                              FROM {table_name}
                              WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""")[0]
            pixel_trajectory_x, pixel_trajectory_y = process_pupil_movements(pupil_movements, center, displacement_ratios) # translate pupil coordinates to pixels
            OOI_analysis_result = deduce_object_of_interest(pixel_trajectory_x, pixel_trajectory_y, boundingbox)
      
            # Save analysis results to DB
            target_table = 'TrajectoryResult'
            insert(f"""INSERT INTO {target_table} 
                   VALUES ('{test_id}', '{test_taker_id}', '[{', '.join(map(str, pixel_trajectory_x))}]', '[{', '.join(map(str, pixel_trajectory_y))}]');""")
            
            target_table = 'OOIResult'
            for obj_id in boundingbox:
                insert(f"""INSERT INTO {target_table} 
                           VALUES ('{test_id}', '{test_taker_id}', '{obj_id}', {OOI_analysis_result[obj_id]})""") # save OOI analysis result    
            return {'success':True, 'result':OOI_analysis_result}
        except:
            return {'success':False, 'result':0}


@app.route('/api/dashboard/visualize/heatmap', methods=['POST'])
def get_heatmap():
    if request.method == 'POST':
        try:
            test_id = request.get_json()['test_id']
            test_taker_id = request.get_json()['test_taker_id']
            screen = request.get_json()['screen']
            screen = decode_image(screen)
        except:
            return {'error_message':'unclear or incomplete payload information in the request json'}
        
        table_name = 'TrajectoryResult'
        try:
            pixel_movements_x, pixel_movements_y = read(f"""SELECT x_trajectory, y_trajectory
                                                            FROM {table_name} 
                                                            WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""")[0]
            pixel_movements_x = json.loads(pixel_movements_x)
            pixel_movements_y = json.loads(pixel_movements_y)
        except:
            return {'error_message':'Unable to retrieve the user gaze trajectory for given test set.'}                                           

        # Create empty np.array 
        heatmap = np.zeros_like(screen[:, :, 0], np.float32)  # Use float32 for better precision
        
        # Interpolate between points
        addNoise = True
        for idx in range(len(pixel_movements_x)):
            x, y = int(pixel_movements_x[idx]), int(pixel_movements_y[idx])
            if idx > 0:
                prev_x, prev_y = int(pixel_movements_x[idx-1]), int(pixel_movements_y[idx-1]) 
                num_points = np.hypot(x - prev_x, y - prev_y) // 4 # Number of points to interpolate based on the Euclidean distance between the points
                x_values = np.linspace(prev_x, x, int(num_points), endpoint=True)
                y_values = np.linspace(prev_y, y, int(num_points), endpoint=True)
                for px, py in zip(x_values, y_values):
                    if addNoise:
                        npx = addWhiteNoise(px, mean=3, std_dev=2)
                        npy = addWhiteNoise(py, mean=3, std_dev=2)
                        try:
                            # heatmap[int(py), int(px)] += 1
                            heatmap[int(npy), int(npx)] += 1
                            heatmap[int(npy)+random.choice([-1, -2, 0, 1, 2, 3]), int(npx)] += 1
                            heatmap[int(npy)+random.choice([-1, -2, 0, 1, 2, 3]), int(npx)] += 1
                            heatmap[int(npy), int(npx)+random.choice([-1, -2, 0, 1, 2, 3])] += 1
                            heatmap[int(npy), int(npx)+random.choice([-1, -2, 0, 1, 2, 3])] += 1
                        except:
                            pass
        # Apply Gaussian blur to the heatmap
        heatmap_blurred = cv2.GaussianBlur(heatmap, (201, 201), 0)  # Use a larger kernel size for more smoothing
        # Normalize the blurred heatmap to 8-bit range
        heatmap_normalized = cv2.normalize(heatmap_blurred, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        # Superimpose heatmap to the uploaded screen image
        # Apply the colormap
        heatmap_img = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)
        super_imposed_img = cv2.addWeighted(heatmap_img, 0.5, screen, 0.5, 0)
        return {'result_image':base64.b64encode(cv2.imencode('.jpg', super_imposed_img)[1]).decode()}


@app.route('/api/dashboard/visualize/trajectory', methods=['POST'])
def get_trajectory():
    if request.method == 'POST':
        try:
            test_id = request.get_json()['test_id']
            test_taker_id = request.get_json()['test_taker_id']
            screen = request.get_json()['screen']
            
        except:
            return {'error_message':'unclear or incomplete payload information in the request json'}
        
        table_name = 'TrajectoryResult'
        try:
            pixel_movements_x, pixel_movements_y = read(f"""SELECT x_trajectory, y_trajectory
                                                            FROM {table_name} 
                                                            WHERE test_id='{test_id}' AND test_taker_id='{test_taker_id}';""")[0]
            pixel_movements_x = json.loads(pixel_movements_x)
            pixel_movements_y = json.loads(pixel_movements_y)
        except:
            return {'error_message':'Unable to retrieve the user gaze trajectory for given test set.'}       
        
        screen = decode_image(screen)
        trajectory = []
        frames = []
        for idx in range(len(pixel_movements_x)):
            x, y = int(pixel_movements_x[idx]), int(pixel_movements_y[idx])
            trajectory.append((x, y)) # add it to trajectory
            screen = cv2.circle(screen, (int(x), int(y)), radius=5, color=(20, 255, 20), thickness=-1) 
            if len(trajectory) > 1:
                for j in range(1, len(trajectory)):
                    color = max(0, 255 - j * 10)  
                    screen = cv2.line(screen, trajectory[j - 1], trajectory[j], (0, 0, color), thickness=1)
            frames.append(base64.b64encode(cv2.imencode('.jpg', screen)[1]).decode()) 
        return {'frames':frames}
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
     
    