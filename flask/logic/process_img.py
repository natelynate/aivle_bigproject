import numpy as np
import cv2
import tensorflow as tf

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


def preprocess_image(img_jpg_original):
    """Apply preprocessing steps to the jpg image.
       Resized to (48, 48), applied regularization and expanded dim into (1, 48, 48, 1)"""
    jpg_as_np = np.frombuffer(img_jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)

    # preprocessing
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 흑백 변환
    img_reshaped = cv2.resize(img, (48, 48))
    img_normalized = img_reshaped / 255
    img_binary = binarypattern(img_normalized)
    img_binary = tf.expand_dims(img_binary, axis=-1)
    img_binary = tf.expand_dims(img_binary, axis=0)
    return img_binary
