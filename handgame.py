import  cv2
import  mediapipe as mp
import time
import handtrackingmodule as htm
cap = cv2.VideoCapture(0)
p_time = 0
c_time = 0
detector=htm.handDetector()
while True:
    success, img = cap.read()
    img=detector.findhands(img)
    li=detector.findPosition(img,idNum=4)
    if len(li)!=0:
        print(li[4])
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3, (0, 0, 0))

    cv2.imshow("Image", img)
    cv2.waitKey(10)

