# import Libraries
import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import cvzone
from pynput.keyboard import Controller
import pygame

pygame.init()
pygame.mixer.init()
#Add sound for clicks
mc = pygame.mixer.Sound("kc.wav")
#Turn on the camera and select the working screen area
cam = cv.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)
#setting buttons
detector = HandDetector(detectionCon=0.8)
keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = " "
CLICK_DISTANCE = 0
keyboard = Controller()
#Draw and locate buttons on the screen
def drawAll(img, buttonList):

    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                     (0, 0, 0), cv.FILLED)
        cv.putText(imgNew, button.text, (x + 40, y + 60),
                   cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out
#Properties
class Button():
    def __init__(self, pos, text, size=[75,75]):
        self.pos = pos
        self.text = text
        self.size = size

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    success, img = cam.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 0, 200), cv.FILLED)
                cv.putText(img, button.text, (x + 20, y + 65),
                           cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)

                #when clicked
                if l < 30:
                    keyboard.press(button.text)
                    pygame.mixer.Sound.play(mc)

                    cv.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv.FILLED)
                    cv.putText(img, button.text, (x + 20, y + 65),
                               cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 0), 4)
                    finalText += button.text
                    sleep(0.15)
            #You can change the numbers to switch the place
            #The location of the writing pad on the screen
    cv.rectangle(img, (100, 500), (800, 600), (175, 100, 0), cv.FILLED)
    cv.putText(img, finalText, (100, 580),
               cv.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    cv.imshow("Image", img)
    key = cv.waitKey(1)
    # It shuts down when the esc key is pressed
    if key == 27:
        break


