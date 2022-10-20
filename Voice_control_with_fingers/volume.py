# import libraries
import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume
#Specify the area of ​​the popup
Wcam, Hcam = 700, 500
#Turn on the camera and set the height and width
cam = cv.VideoCapture(0)
cam.set(3, Wcam)
cam.set(4, Hcam)
Time = 0
#Retrieve the function of hand selection and volume control
detector = htm.handDetector(detectionCon=0.7, maxHands=1)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol = (255, 0, 0)
while True:
    success ,img = cam.read()
    #fain hand
    img = detector.findHands(img)
    lmList ,bbox = detector.findPosition(img, draw=True)
    if len(lmList) != 0:
        # Filter based on size
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
        if 250 < area < 1000:
            # Find Distance between index and Thumb
            length, img, lineinfo = detector.findDistance(4, 8, img)
            # Convert Volume
            volBar = np.interp(length, [50, 200], [400, 150])
            volPer = np.interp(length, [50, 200], [0, 100])
            # Reduce Resolution to make it smoother
            smoothness = 10
            volPer = smoothness * round(volPer / smoothness)
            # Check fingers up
            fingers = detector.fingersUp()
            # If pinky is down set volume
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                cv.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)
        # Drawings
        cv.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv.FILLED)
        cv.putText(img, f'{int(volPer)} %', (40, 450), cv.FONT_HERSHEY_COMPLEX,
                   1, (255, 0, 0), 3)
        cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
        cv.putText(img, f'Vol Set: {int(cVol)}', (400, 50), cv.FONT_HERSHEY_COMPLEX,
                    1, colorVol, 3)

        # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - Time)
    Time = cTime
    cv.putText(img, f'FPS: {int(fps)}', (40, 50), cv.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv.imshow("Img", img)
    key = cv.waitKey(1)
    # It shuts down when the esc key is pressed
    if key == 27:
        break