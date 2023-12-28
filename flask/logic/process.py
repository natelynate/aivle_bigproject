import numpy as np
import cv2
import tensorflow as tf
import base64
from models.pupil_tracker import GazeTracking

def binarypattern(im):         
    """Convert the image into a Binary Pattern"""                      
    img = np.zeros_like(im)
    n=3                                              
    for i in range(0,im.shape[0]-n):                 
        for j in range(0,im.shape[1]-n):              
            x  = im[i:i+n,j:j+n]                    
            center       = x[1,1]                   
            img1        = (x >= center)*1.0          
            img1_vector = img1.T.flatten()           
            img1_vector = np.delete(img1_vector,4)
            digit = np.where(img1_vector)[0]
            if len(digit) >= 1:                    
                num = np.sum(2**digit)             
            else:                                    
                num = 0
            img[i+1,j+1] = num
    return(img)

def decode_image(frame):
    """Receives a single b64 encoded string and return as a cv2 image"""
    jpg_original = base64.b64decode(frame)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img

def preprocess_image(img_jpg_original):
    """Apply preprocessing steps to the jpg image.
       Resized to (48, 48), applied regularization and expanded dim into (1, 48, 48, 1)"""
    img = decode_image(img_jpg_original)

    # preprocessing
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 흑백 변환
    img_reshaped = cv2.resize(img, (48, 48))
    img_normalized = img_reshaped / 255
    img_binary = binarypattern(img_normalized)
    img_binary = tf.expand_dims(img_binary, axis=-1)
    img_binary = tf.expand_dims(img_binary, axis=0)
    return img_binary


def record_pupil_movements(frames, excludeNone=True):
    """Receive frames, after decoding return the list of pupils movements. if excludeNone=True, discard frames with no detected pupils"""
    decoded_frames = [decode_image(frame) for frame in frames]
    pupil_movements = []
    gaze = GazeTracking()
    for f in decoded_frames:
        gaze.refresh(f)
        if gaze.pupil_left_coords() and gaze.pupil_right_coords():
            left_pupil, right_pupil = gaze.pupil_left_coords(), gaze.pupil_right_coords()
            pupil_movements.append([(int(left_pupil[0]), int(left_pupil[1])), (int(right_pupil[0]), int(right_pupil[1]))])
    return pupil_movements


def get_displacement_ratios(ref_point, center_ref, loc_tag):
    """"""
    # Calculate displacement ratios relative to the center point
    if loc_tag in ['left', 'right']:
        return round(960 / abs(center_ref[0] - ref_point[0]), 2)
    elif loc_tag in ['up', 'down']:
        return round(540 / abs(center_ref[1] - ref_point[1]), 2)
    
    
    
def ref_is_valid(new_ref, center_ref, loc_tag) -> bool:
    """Compare the reference point coordinates and check if it is valid depending on the reference point location tag"""
    referencing_eye = 1 # 0 for left, 1 for right (임시)
    if loc_tag == 'left':
        if new_ref[referencing_eye][0] >= center_ref[referencing_eye][0]:
            return False
    if loc_tag == 'right':
        if new_ref[referencing_eye][0] <= center_ref[referencing_eye][0]:
            return False
    if loc_tag == 'up':
        if new_ref[referencing_eye][1] >= center_ref[referencing_eye][1]:
            return False
    if loc_tag == 'down':
        if new_ref[referencing_eye][1] <= center_ref[referencing_eye][1]:
            return False
    return True
        

def process_pupil_movements(pupil_movement, addNoise=True):
    """Convert pupil displacements into corresponding pixel coordinates"""
    def addWhiteNoise(x, y, mean=10, std_dev=5):
        """Add white noise to the pixel coordinates"""
        noise_x = np.random.normal(loc=mean, scale=std_dev)
        noise_y = np.random.normal(loc=mean, scale=std_dev)
        return x+noise_x, y+noise_y
    
    def findScaleFactor(pupil_movement):
        """Description Text"""
        minX, minY, maxX, maxY = 1e99, 1e99, -1e99, -1e99
                
        for frame in pupil_movement:
            right_pupil = frame[1]
            minX = min(right_pupil[0], minX)
            minY = min(right_pupil[1], minY)
            maxX = max(right_pupil[0], maxX)
            maxY = max(right_pupil[1], maxY)
        x_scale_factor, y_scale_factor = (maxX - minX) / 1920, (maxY - minY) / 1080
        return x_scale_factor, y_scale_factor
    
    def convert2pixel(x, y, x_scale_factor, y_scale_factor):
        """Convert pupil coordination to pixel coordination"""
        x /= x_scale_factor
        y /= y_scale_factor
        if addNoise:
            x, y = addWhiteNoise(x, y)
        if x > 1920:
            x = 1900
        if y > 1080:
            y = 1060
        return int(x), int(y)
    
    pixel_movements = []
    x_scale_factor, y_scale_factor = findScaleFactor(pupil_movement)
    print("scale_factors: ", x_scale_factor, y_scale_factor)
    
    for coord in pupil_movement:
        pixel_x, pixel_y = convert2pixel(coord[1][0], coord[1][1], x_scale_factor, y_scale_factor)
        pixel_movements.append((pixel_x, pixel_y))
    return pixel_movements


def deduce_object_of_interest(pixel_coords, object_regions):
    """Deduce which object of interest each pixel coordinates are on and return dictionary"""
    result = {key:0 for key in object_regions} # dict for recording hitcounts 
    for pixel_coord in pixel_coords:
        x, y = pixel_coord
        for obj_id in object_regions:
            boundingbox = object_regions[obj_id] # access the bounding box coordinates of each object
            if (boundingbox[0][0] <= x <= boundingbox[1][0]) and (boundingbox[0][1] <= y <= boundingbox[1][1]):
                result[obj_id] += 1
    return result
                

