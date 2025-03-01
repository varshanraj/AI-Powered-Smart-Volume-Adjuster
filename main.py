import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

cap = cv2.VideoCapture(0) #Checks for camera,  0 refers to the default camera

mpHands = mp.solutions.hands             #detects hand/finger, mpHands is a module for hand tracking, and hands
hands = mpHands.Hands()                  #complete the initialization configuration of hands
mpDraw = mp.solutions.drawing_utils      #mpDraw is a module for drawing utilities.

#To access speaker through the library pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#_iid_ stands for "interface identifier." It's a special attribute used to identify an interface
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin,volMax = volume.GetVolumeRange()[:2]

while True:
    success,img = cap.read()                        #If camera works capture an image
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)    #Convert to rgb

    #Collection of gesture information
    results = hands.process(imgRGB)                 #completes the image processing.

    lmList = [] #empty list
    if results.multi_hand_landmarks:                #list of all hands detected.
        #By accessing the list, we can get the information of each hand's corresponding flag bit
        for handlandmark in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmark.landmark):      #adding counter and returning it
                h,w,_ = img.shape       #returns the dimensions of the image array as a tuple
            #underscore here is just used to indicate that this value is being ignored. no. of colour channels like RGB
            # number of rows of pixels in the image - 'h'
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy]) #adding to the empty list 'lmList'
            mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)

    if lmList != []:
        #getting the value at a point
                        #x      #y
        x1,y1 = lmList[4][1],lmList[4][2]       #thumb, [4] is used to access the 5th landmark in the lmList
        x2,y2 = lmList[8][1],lmList[8][2]       #index finger
        #creating circle at the tips of thumb and index finger
        cv2.circle(img,(x1,y1),13,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),13,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)       #create a line b/w tips of index finger and thumb

        length = hypot(x2-x1,y2-y1)                     #distance b/w tips using hypotenuse
 # from numpy we find our length,by converting hand range in terms of volume range ie b/w -63.5 to 0
        vol = np.interp(length,[30,350],[volMin,volMax])

        print(vol,int(length))
        volume.SetMasterVolumeLevel(vol, None)

        # Hand range 30 - 350
        # Volume range -63.5 - 0.0
    cv2.imshow('Image',img)                         #Show the video
    if cv2.waitKey(1) & 0xff==ord(' '):             #By using spacebar delay will stop
        break

cap.release()                   #stop cam
cv2.destroyAllWindows()         #close window
