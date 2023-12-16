# import Libraries
import cv2 as cv
import pickle
import cvzone
import numpy as np

# read the video we're working on
cap = cv.VideoCapture('video.mp4')
# We open the pre-prepared parking lot file
with open('car', 'rb') as f:
    poslist = pickle.load(f)
# know the width and height
width, height = 180, 272

# We create a function to find the empty places from the filled places
def chackpark(imgpro):

    spacecounter = 0
    for pos in poslist:
        x, y = pos
        # Lack of car space
        imgCrop = imgpro[y:y + height, x:x + width]
        count = cv.countNonZero(imgCrop)
        # We determine the presence of the car or not, according to the filled space
        if count < 4500:
            color = (0, 255, 0)
            thickness = 5
            spacecounter += 1
        else:
            color = (0, 0, 255)

            thickness = 2

        cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        # We use a library cvzone to determine how many cars there are
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spacecounter}/{len(poslist)}', (100, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 200, 0))



while True:
    # We count the number of tires through opencv
    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv.dilate(imgMedian, kernel, iterations=1)

    chackpark(imgDilate)
    cv.imshow("Image", img)
    cv.waitKey(15)