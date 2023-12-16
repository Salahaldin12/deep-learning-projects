import cv2 as cv
import pickle

# img = cv.imread('tes.png')

try:
    with open('car', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


width, height = 150, 272
def mouseClick(events, x, y, flags , params ):
    if events == cv.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
    with open('car', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv.imread('tes.png')
    cv.rectangle(img,(730,97),(880,370),(255,0,0),2)
    for pos in posList:
        cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 0), 2)
    cv.imshow("img", img)
    cv.setMouseCallback("img", mouseClick)
    cv.waitKey(1)