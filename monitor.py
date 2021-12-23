import cv2
import time
import logging
import random
import string

def randomString():
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))

logFormat = "{0}:{1}"
logFile = "monitoringsystem.log"
logging.basicConfig(filename=logFile, encoding='utf-8', level=logging.DEBUG)

camera = cv2.VideoCapture(0)
if camera is None:   
    print('请先连接摄像头')
    exit()

bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)

fps = 5 # 帧率
pre_frame = None  # 总是取前一帧做为背景（不用考虑环境影响）
pre_time = int(time.time())
 
while True:
    start = time.time()
    res, cur_frame = camera.read()
    if res != True:
        break
    end = time.time()
    seconds = end - start
    if seconds < 1.0/fps:
        time.sleep(1.0/fps - seconds)

    gray_img = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.resize(gray_img, (500, 500))
    gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)
 
    if pre_frame is None:
        pre_frame = gray_img
    else:
        img_delta = cv2.absdiff(pre_frame, gray_img)
        thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        flag = False
        for c in contours:
            if cv2.contourArea(c) < 1600: # 设置敏感度
                continue
            else:
                flag = True
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(cur_frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        if flag:
            currentTime = int(time.time())
            if currentTime - pre_time > 5:
                pre_time = currentTime
                print("记入日志ing")
                currentImage = "./images/" + randomString() + ".jpg"
                cv2.imwrite(currentImage, cur_frame)
                logging.info(logFormat.format(currentTime, currentImage))
        pre_frame = gray_img

    ret, frame = camera.read()
    fgmask = bs.apply(frame)
    th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]

    dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
    contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) > 1600:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

    cv2.imshow('show', frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
 
camera.release()
cv2.destroyAllWindows()