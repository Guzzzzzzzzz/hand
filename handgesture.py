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

# detector = HandDetector()
#  指尖列表，分别代表大拇指、食指、中指、无名指和小指的指尖
tip_ids = [4, 8, 12, 16, 20]

while True:
    img = me.get_frame_read().frame
    #img =cv2.resize(img,(360,240))
    result = hands.process(img)
    # print(result.multi_hand_landmarks)
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]
    lmslist = []
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle,handConStyle)   #将监测到的手进行绘制（21个点）
            for i , lm in enumerate(handLms.landmark):    #i=第几个点 im=点的坐标

                xPos = int(lm.x *imgWidth)
                yPos = int(lm.y *imgHeight)
                lmslist.append([id, xPos, yPos])
                cv2.putText(img ,str(i),(xPos-25, yPos+5),cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255), 2)
            print(i,xPos ,yPos )

        fingers = []
        for tid in tip_ids:
            # 找到每个指尖的位置
            x, y = lmslist[tid][1], lmslist[tid][2]
            cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
            # 如果是大拇指，如果大拇指指尖x位置大于大拇指第二关节的位置，则认为大拇指打开，否则认为大拇指关闭
            if tid == 4:
                if lmslist[tid][1] > lmslist[tid - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # 如果是其他手指，如果这些手指的指尖的y位置大于第二关节的位置，则认为这个手指打开，否则认为这个手指关闭
            else:
                if lmslist[tid][2] < lmslist[tid - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        # fingers是这样一个列表，5个数据，0代表一个手指关闭，1代表一个手指打开
        # 判断有几个手指打开
        cnt = fingers.count(1)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,f"FPS :{int(fps)}",(30, 50),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)