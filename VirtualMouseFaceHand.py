import cv2
import mediapipe as mp
import time
import Module as md
import math
import pyautogui
import autopy
import numpy as np


cap = cv2.VideoCapture(0)
tracker = md.handTracker()
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True) #face_mesh
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)
wScreen,hScreen =  autopy.screen.size()
#print(wScreen,hScreen)
frameR = 110
smooth  = 4
ptime = 0
plocX,plocY = 0,0
clocX,clocY = 0,0

while True:
    success,image = cap.read()
    image = cv2.flip(image, 1)
    image = tracker.handsFinder(image)
    lmList = tracker.positionFinder(image)

    # eye click
    output1 = face_mesh.process(image)
    landmark_points = output1.multi_face_landmarks
    frame_h, frame_w, _ = image.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark 
        left = [landmarks[145], landmarks[159]]
        lef = [landmarks[145]]
        for landmark in lef:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(image, (x-1, y-6), 5, (255, 0, 0),thickness=2)    
            cv2.circle(image, (x-1, y-5), 1, (255, 0, 255),thickness=2) 

    
    # 2. Get the tip of the index and middle fingers
      
    if len(lmList) != 0:
       cv2.circle(image,(lmList[8][1],lmList[8][2]), 10 , (0,0,255),thickness=3) 
       cv2.circle(image,(lmList[4][1],lmList[4][2]), 10 , (0,0,255),thickness=3) 
       #cv2.circle(image,(lmList[12][1],lmList[12][2]), 6 , (0,0,255),cv2.FILLED) 
        
       #print((lmList[8][1],lmList[8][2]))
       x1 = lmList[12][1]
       x2 = lmList[4][1]
       y1 = lmList[12][2]
       y2 = lmList[4][2]
       x3 = lmList[8][1]
       y3 = lmList[8][2]
       lengthDrag = math.hypot(x2 - x1, y2 - y1)
       lengthClick = math.hypot(x2 - x3, y2 - y3)
       

       #if lengthClick < 22:
        
        #print((left[0].y - left[1].y)) 
       if lengthDrag < 35 :
            #cv2.circle(image,(lmList[12][1],lmList[12][2]), 7 , (0,0,0),cv2.FILLED)
            cv2.circle(image,(lmList[4][1],lmList[4][2]), 6 , (255,0,0),cv2.FILLED) 
            cv2.rectangle(image,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),1)
            x33 = np.interp(x2,(frameR,wCam-frameR),(0,wScreen))
            y33 = np.interp(y2,(frameR,hCam-frameR),(0,hScreen))

            clocX = plocX + (x33-plocX)/smooth
            clocY = plocY + (y33-plocY)/smooth


            if clocX > 1530:
                clocX = 1530
            if clocY > 855:
                clocY = 855    
            #print(y33)    
            autopy.mouse.move(clocX,clocY)
            print((left[0].y - left[1].y))
            if (left[0].y - left[1].y) < 0.01:
               autopy.mouse.click()
               

            plocX,plocY = clocX,clocY

            #x0,y0 = pyautogui.position()
           #print(x0,y0)
            #pyautogui.moveTo(x1, y1)
       
       
       #print(length)



    if cv2.waitKey(5) & 0xFF == ord('q'):
        break  
    cv2.imshow("Video",image)
    cv2.waitKey(1)