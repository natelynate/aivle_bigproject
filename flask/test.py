# This is a script file for testing the RESTful API Functionalities of the project
# 
#
# 
import json
import requests
import cv2
import base64

  # Open video file in binary mode
task = 'ref' # ref/AB
# headers = {
#     'Content-Type': 'multipart/form-data'
# }
url = 'http://127.0.0.1:105/api/eyetrack'

if task == 'ref':
  image1 = cv2.imread('./sample_data/center.jpg')
  image2 = cv2.imread('./sample_data/left.jpg')
  image3 = cv2.imread('./sample_data/right.jpg')
  image4 = cv2.imread('./sample_data/up.jpg')
  image5 = cv2.imread('./sample_data/down.jpg')
  # Convert captured image to JPG
  string1 = base64.b64encode(cv2.imencode('.jpg', image1)[1]).decode()
  string2 = base64.b64encode(cv2.imencode('.jpg', image2)[1]).decode()
  string3 = base64.b64encode(cv2.imencode('.jpg', image3)[1]).decode()
  string4 = base64.b64encode(cv2.imencode('.jpg', image4)[1]).decode()
  string5 = base64.b64encode(cv2.imencode('.jpg', image5)[1]).decode()
  headers = {'content-type':'application/json'}
  payload =  {
          'frames':[string1, string2, string3, string4, string5], 
          'tasktype':'get_ref',
          'project_id':'project123',
          'testtaker_id':'123456',
          'image_id':None,
          'pixel_x':450,
          'pixel_y':450,
          'object_locations':None}
  response = requests.post(url, 
                           headers=headers,
                           data=json.dumps(payload))
  print("For ref point task", response.text)
  print("=====================================================")


# elif task == 'AB':
#     video = {'video': (video_file.name, video_file, 'video/webm')}
#     body = {
#             'tasktype':'get_ref',
#             'project_id':'project123',
#             'testtaker_id':'123456',
#             'image_id':'a1b2c3d4',
#             'pixel_x':None,
#             'pixel_y':None,
#             'object_locations':[[[100, 100], [300, 300]], 
#                                 [[350, 100], [550, 300]], 
#                                 [[600, 100], [800, 300]]]}
#     response = requests.post(url, 
#                                 headers=headers, 
#                                 files=video,
#                                 data=body)
#     print("AB Test", response.text)
