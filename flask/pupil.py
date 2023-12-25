import sys
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()

video_file = './samples/WIN_20231222_11_10_25_Pro.webm'
video = cv2.VideoCapture(video_file)
print(video)
ret, frame = video.read()
gaze.refresh(frame)
left_pupil_coord = gaze.pupil_left_coords()
right_pupil_coord = gaze.pupil_right_coords()
print(left_pupil_coord, right_pupil_coord)

video_file = './samples/nopupil.webm'
video = cv2.VideoCapture(video_file)
print(video)
ret, frame = video.read()
gaze.refresh(frame)
left_pupil_coord = gaze.pupil_left_coords() # Returns None if no pupil
right_pupil_coord = gaze.pupil_right_coords() # Returns None if no pupil
print(left_pupil_coord, right_pupil_coord)

videos = ['center.webm', 'bottom.webm', 'left.webm', 'right.webm']
for video_file in videos:
    video = cv2.VideoCapture('./samples/' + video_file)
    ret, frame = video.read()
    try:
        gaze.refresh(frame)
        left_pupil_coord = gaze.pupil_left_coords()
        right_pupil_coord = gaze.pupil_right_coords()
        print(video_file, left_pupil_coord, right_pupil_coord)
    except:
        print("No pupil detected")

## Get Video
# while True:
#     ret, frame = video.read()
#     if not ret:
#         break
#     gaze.refresh(frame)
#     left_pupil_coord = gaze.pupil_left_coords()
#     right_pupil_coord = gaze.pupil_right_coords()
#     print(left_pupil_coord, right_pupil_coord)

"""Save Video as a file"""
"""근데 잘 생각해보니까 동영상을 파일로 저장할 일은 없지 않나?"""
# print("save video as file")
# video_file = './samples/bottom.webm'
# video = cv2.VideoCapture(video_file)
# outputname = 'samplevid.webm'
# fourcc = int(video.get(cv2.CAP_PROP_FOURCC)).to_bytes(4, byteorder=sys.byteorder).decode()
# print(fourcc)
# fourcc = cv2.VideoWriter_fourcc(*'vp90')
# width = round(video.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = round(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = video.get(cv2.CAP_PROP_FPS)
# print(width, height, fps)
# cv2.VideoWriter(outputname, fourcc, fps, (width, height))
