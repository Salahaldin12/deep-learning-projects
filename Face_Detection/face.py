# import libraries
import cv2
import mediapipe as mp
import time
# read video and put in a variable
Read = cv2.VideoCapture("testss.mp4")
ptime =0
# Face identification and details
mpFasce = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faseDetact = mpFasce.FaceDetection()
# Processing images and colors, placing a frame on the face,
# and determining the accuracy of recognition
while True:
    success, img = Read.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faseDetact.process(imgRGB)
    print(results)
    if results.detections:
        for id, detection in enumerate(results.detections):
            #mpDraw.draw_detection(img, detection)
            #print(detection.location_data.relative_bounding_box)
            boxC = detection.location_data.relative_bounding_box
            ih ,iw ,ic = img.shape
            box = int(boxC.xmin * iw ), int(boxC.ymin *ih), \
                  int(boxC.width *iw ),int(boxC.height *ih)
            cv2.rectangle(img , box,(0,255,0),4)
            cv2.putText(img,f'{int(detection.score[0] * 100 )}%',
                        (box[0],box[1] - 20),cv2.FONT_HERSHEY_PLAIN,
                        2,(0,255,0),2)

#Face frames, number of frames, and operating speed
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {int(fps)}' , (10,70), cv2.FONT_HERSHEY_PLAIN,
                3, (255,255,255),2)
    cv2.imshow("Image", img)
    cv2.waitKey(10)