# import libraries
import cv2
import mediapipe as mp
import time
# read video and put in a variable
class FaceDetector():
    def __init__(self,minDetectionCon = 0.5):
        self.minDetectionCon = minDetectionCon

# Face identification and details
        self.mpFasce = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faseDetact = self.mpFasce.FaceDetection(minDetectionCon)
# Processing images and colors, placing a frame on the face,
# and determining the accuracy of recognition
    def findface(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faseDetact.process(imgRGB)
        #print(self.results)
        boxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                boxC = detection.location_data.relative_bounding_box
                ih ,iw ,ic = img.shape
                box = int(boxC.xmin * iw ), int(boxC.ymin *ih), \
                      int(boxC.width *iw ),int(boxC.height *ih)
                boxs.append([id,box,detection.score])
                if draw:
                    img = self.fancyDrow(img,box)
                    cv2.putText(img,f'{int(detection.score[0] * 100 )}%',
                                (box[0],box[1] - 20),cv2.FONT_HERSHEY_PLAIN,
                                2,(0,255,0),2)
        return img , boxs
    def fancyDrow(self,img,box,l=30,t=5,rt=1):
        x,y,w,h=box
        x1,y1 = x+w,y+h
        cv2.rectangle(img, box, (0, 255, 0), rt)
        #top left
        cv2.line(img,(x,y),(x+l,y),(0,255,0),t)
        cv2.line(img, (x, y), (x , y+l), (0, 255, 0), t)
        #top right
        cv2.line(img, (x1, y), (x1 - l, y), (0, 255, 0), t)
        cv2.line(img, (x1, y), (x1, y + l), (0, 255, 0), t)
        #bottom left
        cv2.line(img, (x, y1), (x + l, y1), (0, 255, 0), t)
        cv2.line(img, (x, y1), (x, y1 - l), (0, 255, 0), t)
        #bottom right
        cv2.line(img, (x1, y1), (x1 - l, y1), (0, 255, 0), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (0, 255, 0), t)
        return img
#Face frames, number of frames, and operating speed


def main():
    Read = cv2.VideoCapture("testss.mp4")
    ptime = 0
    detector = FaceDetector()
    while True:
        success, img = Read.read()
        img , boxs  = detector.findface(img)
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 255, 255), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(15)
if __name__ == '__main__':
    main()


