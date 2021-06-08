import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
p_time=0
c_time=0
while True:
    success, img = cap.read()
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=hands.process(imageRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for lm in results.multi_hand_landmarks:
            for id,land_m in enumerate(lm.landmark):
                #print(id,land_m)
                h,w,c=img.shape
                cx,cy=int(land_m.x*w),int(land_m.y*h)
                print(id,cx,cy)
                if id==1:
                    cv2.circle(img,(cx,cy),25,(0,0,255))
            mpDraw.draw_landmarks(img, lm,mpHands.HAND_CONNECTIONS)
    c_time=time.time()
    fps=1/(c_time-p_time)
    p_time=c_time

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_ITALIC,3,(0,0,0))



    cv2.imshow("Image", img)
    cv2.waitKey(10)