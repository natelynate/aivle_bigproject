import numpy as np
import cv2
import tensorflow as tf
import base64

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


def check_ref(pupils):
    """Return True/False depending on the ratio of total frames with identificable pupul coordinates"""
    pass

def get_avg_pupil(pupils):
    """Calculate the average coordinates of the popul from an array of frames"""
    """당장은 귀찮으니까 첫 번째 중간 프레임 기준으로 보냅니다"""
    length = len(pupils)
    return pupils[length // 2]

def calculate_ref(x, y, avg_pupil_x, avg_pupil_y):
    """Calculate the reference mapping information based on the pixel coordination of the screen and the avg pupil coordinates"""
    """중간의 픽셀값이 (810, 540)이라고 가정하고, 오른쪽 눈의 좌표를 기준으로 했을 시"""
    mapping = {1:int(x/avg_pupil_x), 1:int(x/avg_pupil_y)}
    return mapping

def interpolate_gazetrack(coords):
    """Given an array of eye coordinates by frame, interpolate the missing coordinates"""
    pass

def transform_to_pixel(pupils, ref):
    """Transform a tuple of pupil coordinates into a corresponding screen pixel coordinates based on mapping information"""
    pass

def deduce_object_of_interest(pixel_coords, object_regions):
    """Deduce which object of interest each pixel coordinates are on and return an array"""
    pass
