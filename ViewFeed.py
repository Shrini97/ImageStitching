import cv2
video_path_1   = 'rtsp://112.133.197.90:2555/1/h264major'
video_path_2 = 'rtsp://admin:admin@123@112.133.197.90:2554/cam/realmonitor?channel=1&subtype=1' #-> zoomed in
vid_1 = cv2.VideoCapture(video_path_1)
vid_2 = cv2.VideoCapture(video_path_2)
while True:
    ret_1 , original_frame_1 = vid_1.read()
    ret_2, original_frame_2 = vid_2.read()
    cv2.imshow("frame_1", original_frame_1)
    cv2.imshow("frame_2", original_frame_2)
    cv2.waitKey(1)