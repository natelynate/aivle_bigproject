from flask import Flask, request
import pymysql
import base64
from logic.db import * # import db setup functions
from logic.process_img import * # import image processing functions


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
@app.route('/api/video_upload', methods=['POST'])
def upload_video():
    pass

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
    