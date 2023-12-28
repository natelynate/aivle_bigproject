# This is a script file for testing the RESTful API Functionalities of the project
# 
#
# 
import json
import requests
import cv2
import base64

task = 'ref' # ref/AB
url = 'http://127.0.0.1:105/api/eyetrack/reference'
coords = [(1920//2, 1080//2), (0, 1080//2), (1920, 1080//2), (1920//2, 0), (1920//2, 1080)]
locs = ['center', 'left', 'right', 'up', 'down']
for idx, loc_tag in enumerate(locs):
  coord = coords[idx]
  image = cv2.imread(f'./sample_data/{loc_tag}.jpg')
  encoded_image = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
  headers = {'content-type':'application/json'}
  payload =  {'frames':[encoded_image for _ in range(24)], 
              'test_id':'sample_test1',
              'test_taker_id':'yoonkihwa',
              'pixel_x':coord[0],
              'pixel_y':coord[1],
              'location_tag':loc_tag}
        
  response = requests.post(url, headers=headers, data=json.dumps(payload))           
  print("For ref point task", loc_tag, response.text)
  if not response.text['result']:
    print("Reference point acquisition has failed. Try again.")
  print("=====================================================")
