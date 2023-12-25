from flask import Flask, request, redirect
import tensorflow as tf
import json
import base64
import cv2
import numpy as np 
from models.pupil_tracker import GazeTracking

app = Flask(__name__)
model_dir = 'saved_model'
model = tf.keras.models.load_model(model_dir)

def Binarypattern(im):                               # creating function to get local binary pattern
    img= np.zeros_like(im)
    n=3                                              # taking kernel of size 3*3
    for i in range(0,im.shape[0]-n):                 # for image height
        for j in range(0,im.shape[1]-n):               # for image width
            x  = im[i:i+n,j:j+n]                     # reading the entire image in 3*3 format
            center       = x[1,1]                    # taking the center value for 3*3 kernel
            img1        = (x >= center)*1.0          # checking if neighbouring values of center value is greater or less than center value
            img1_vector = img1.T.flatten()           # getting the image pixel values
            img1_vector = np.delete(img1_vector,4)
            digit = np.where(img1_vector)[0]
            if len(digit) >= 1:                     # converting the neighbouring pixels according to center pixel value
                num = np.sum(2**digit)              # if n> center assign 1 and if n<center assign 0
            else:                                    # if 1 then multiply by 2^digit and if 0 then making value 0 and aggregating all the values of kernel to get new center value
                num = 0
            img[i+1,j+1] = num
    return(img)


@app.route('/', methods=['GET'])
def index():
    # redirect to exterior domain
    return redirect(location='https://www.naver.com')


@app.route('/api/img_send', methods=['POST'])
def upload_image():
    # receiving and decoding to np array
    jpg_original = base64.b64decode(request.get_json()['baseline_img'])
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)

    # preprocessing
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 흑백 변환
    img_reshaped = cv2.resize(img, (48, 48))
    img_normalized = img_reshaped / 255
    img_binary = Binarypattern(img_normalized)
    img_binary = tf.expand_dims(img_binary, axis=-1)
    img_binary = tf.expand_dims(img_binary, axis=0)
    
    # sentiment_names = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']
    sentiment_probs = model.predict(img_binary)[0]

    return {'data':{'anger':float(sentiment_probs[0]),
                    'disgust':float(sentiment_probs[1]),
                    'fear':float(sentiment_probs[2]),
                    'sadness':float(sentiment_probs[3]),
                    'surprise':float(sentiment_probs[4])}}

@app.route('/api/webm_send', methods=['POST'])
def upload_video():
    # video_file = request.files['video']
    video_file = 'WIN_20231222_11_10_25_Pro'
    gaze = GazeTracking()
    video = cv2.VideoCapture(video_file)
    if request.files['worktype'] == 'singleframe':
        ret, frame = video.read()
        gaze.refresh(frame)
        if gaze.pupils_located():
            left_pupil_coord = gaze.pupil_left_coords()
            right_pupil_coord = gaze.pupil_right_coords()
            is_blink =  gaze.is_blinking()
            print(left_pupil_coord, right_pupil_coord, is_blink)
        else:
            print("No pupil")    
    elif request.files['worktype'] == 'multiframe':
        while True:
            ret, frame = video.read()
            if not ret:
                break
            gaze.refresh(frame)
            left_pupil_coord = gaze.pupil_left_coords()
            right_pupil_coord = gaze.pupil_right_coords()
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
    
    