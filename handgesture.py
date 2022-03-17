import cv2
from djitellopy import tello
import mediapipe as mp
import time

# 电脑摄像头
# cap = cv2.VideoCapture(1)
# while True:
#     ret, img = cap.read()
#     if ret:
#         cv2.imshow('img', img)
#
#     if cv2.waitKey(1) ==ord('q'):
#         break

# tello无人机摄像头
me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()
me.takeoff()

mpHands = mp.solutions.hands
hands =mpHands.Hands()
mpDraw =mp.solutions.drawing_utils
handLmsStyle =mpDraw.DrawingSpec(color=(0,0,255), thickness=5)
handConStyle =mpDraw.DrawingSpec(color=(0,255,0), thickness=10)
pTime =0
cTime =0


def action_to_do(Drone, fingers):
    if fingers ==[0, 0, 0, 0, 0]:
        Drone.land()
    elif fingers == [0, 1, 0, 0, 0]:
        me.send_rc_control(0, 50, 0, 0)
    # elif fingers == [0, 1, 1, 0, 0]:
    #     self.action = "Two flips"
    #
    # elif fingers == [0, 1, 1, 1, 0]:
    #     self.action = "Square"
    # else:
    #     self.action = " "


while True:
    img = me.get_frame_read().frame
    # img =cv2.resize(img,(360,240))
    result = hands.process(img)
    # print(result.multi_hand_landmarks)
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle,handConStyle)   #将监测到的手进行绘制（21个点）
            for i , lm in enumerate(handLms.landmark):    #i=第几个点 im=点的坐标

               xPos = int(lm.x *imgWidth)
               yPos = int(lm.y *imgHeight)
               cv2.putText(img ,str(i),(xPos-25, yPos+5),cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255), 2)
               print(i,xPos ,yPos )

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,f"FPS :{int(fps)}",(30, 50),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)