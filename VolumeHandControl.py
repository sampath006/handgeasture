import math

import cv2
import time
import numpy as np
import handtrackingmodule as htm
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam=640,480
p_time = 0
c_time = 0

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector=htm.handDetector(detec_conf=0.7)
devices = AudioUtilities.GetSpeakers()
interface= devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None
)
volume=cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
vol_ran=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0,None)
min_vol=vol_ran[0]
max_vol=vol_ran[1]
vol_Bar=np.interp(volume.GetMasterVolumeLevel(),[min_vol,max_vol],[400,150])
vol_per=np.interp(volume.GetMasterVolumeLevel(),[min_vol,max_vol],[0,100])
print(volume.GetMasterVolumeLevel())
while True:
    success,img=cap.read()
    img=detector.findhands(img)
    li=detector.findPosition(img,idNum=[4,8])
    if len(li)!=0:
        x1,y1=li[4][1],li[4][2]
        x2,y2=li[8][1],li[8][2]
        #print(li[4],li[8])
        cv2.line(img,(x1,y1),(x2,y2),(0,0,0),3)
        cx=(x1+x2)//2
        cy=(y1+y2)//2
        length = math.hypot(x2 - x1, y2 - y1)
        print(length)
        #hand_range=30-250
        #volrange=-65 to 0
        vol=np.interp(length,[30,250],[min_vol,max_vol])
        vol_Bar = np.interp(volume.GetMasterVolumeLevel(), [min_vol, max_vol], [400, 150])
        vol_per = np.interp(volume.GetMasterVolumeLevel(), [min_vol, max_vol], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img,(85,150),(100,400),(0,255,0),3)
    cv2.rectangle(img,(85,int(vol_Bar)),(100,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'vol {int(vol_per)}', (40,450), cv2.FONT_ITALIC, 2, (0, 0, 0))
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(img,f'FPS {int(fps)}', (30,50), cv2.FONT_ITALIC, 1, (0, 0, 0))
    cv2.imshow("img",img)

    cv2.waitKey(1)