import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,stat_img_mod=False,Max_hands=2, detec_conf=0.5,track_conf=0.5):
        self.mode=stat_img_mod
        self.max_hands=Max_hands
        self.detection_confidence=detec_conf
        self.track_confidence=track_conf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.max_hands,self.detection_confidence,self.track_confidence)
        self.mpDraw=mp.solutions.drawing_utils
    def findhands(self,img, draw=True):
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        if self.results.multi_hand_landmarks:
            for lm in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, lm,self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self,img, handNum=0,draw=True,idNum=None):
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]
            for id, land_m in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(land_m.x * w), int(land_m.y * h)
                if draw:
                    if idNum==None or id in idNum:
                        cv2.circle(img, (cx, cy), 25, (0, 0, 255))
                lmlist.append([id,cx,cy])
        return  lmlist


def main():
    cap = cv2.VideoCapture(0)
    p_time = 0
    c_time = 0
    detector=handDetector()
    while True:
        success, img = cap.read()
        img=detector.findhands(img)
        li=detector.findPosition(img)
        if len(li)!=0:
            print(li[4])
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3, (0, 0, 0))

        cv2.imshow("Image", img)
        cv2.waitKey(10)


if __name__=="__main__":
    main()