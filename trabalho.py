import cv2 as cv
import numpy as np
import pyautogui
from screeninfo import get_monitors
import time

pyautogui.FAILSAFE = False

TAMANHO_TELA = 0
ALTURA_TELA = 0

for m in get_monitors():
    TAMANHO_TELA = m.width
    ALTURA_TELA = m.height



camera = cv.VideoCapture(0, cv.CAP_DSHOW)

width = camera.get(cv.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv.CAP_PROP_FRAME_HEIGHT)

diferenca_width = (TAMANHO_TELA / width) * 1.5
diferenca_height = (ALTURA_TELA / height) * 1.5


def nothing(param):
    pass

cv.namedWindow("result")
cv.createTrackbar('h', 'result', 0, 179, nothing)
cv.createTrackbar('s', 'result', 0, 255, nothing)
cv.createTrackbar('v', 'result', 0, 255, nothing)

while 1:

    x_camera, y_camera = pyautogui.position()

    _, frame = camera.read()
    frame = cv.flip(frame, 1)
    frame2 = cv.flip(frame, 1)
    frame3 = cv.flip(frame, 1)
    frame4 = cv.flip(frame, 1)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    h = cv.getTrackbarPos('h', 'result')
    s = cv.getTrackbarPos('s', 'result')
    v = cv.getTrackbarPos('v', 'result')
    lower = np.array([104, 255, 41])
    upper = np.array([255, 255, 255])
    lower2 = np.array([0, 118, 224])
    upper2 = np.array([255, 255, 255])
    lower3 = np.array([61, 161, 46])
    upper3 = np.array([255, 255, 255])
    lower4 = np.array([28, 166, 93])
    upper4 = np.array([255, 255, 255])

    mask = cv.inRange(hsv, lower, upper)
    mask2 = cv.inRange(hsv, lower2, upper2)
    mask3 = cv.inRange(hsv, lower3, upper3)
    mask4 = cv.inRange(hsv, lower4, upper4)
    result = cv.bitwise_and(frame, frame, mask=mask)
    result2 = cv.bitwise_and(frame2, frame2, mask=mask2)
    result3 = cv.bitwise_and(frame3, frame3, mask=mask3)
    result4 = cv.bitwise_and(frame4, frame4, mask=mask4)

    gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
    gray2 = cv.cvtColor(result2, cv.COLOR_BGR2GRAY)
    gray3 = cv.cvtColor(result3, cv.COLOR_BGR2GRAY)
    gray4 = cv.cvtColor(result4, cv.COLOR_BGR2GRAY)
    _, borda = cv.threshold(gray, 3, 255, cv.THRESH_BINARY)
    _2, borda2 = cv.threshold(gray2, 3, 255, cv.THRESH_BINARY)
    _3, borda3 = cv.threshold(gray3, 3, 255, cv.THRESH_BINARY)
    _4, borda4 = cv.threshold(gray4, 4, 255, cv.THRESH_BINARY)

    contornos, _ = cv.findContours(borda, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    contornos2, _2 = cv.findContours(borda2, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    contornos3, _3 = cv.findContours(borda3, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    contornos4, _4 = cv.findContours(borda4, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    
    for contorno in contornos:
        area = cv.contourArea(contorno)
        if area > 500:
            (x,y,w,h) = cv.boundingRect(contorno)
            #cv.drawContours(frame, contorno, -1, (255,0,0), 2)
            cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),1)
            cv.putText(frame, f'x: {x}, y: {y}', (x,y-20), cv.FONT_HERSHEY_SIMPLEX, 1,1)
            
            x_camera = x*diferenca_width
            y_camera = y*diferenca_height

            x_terco = x / 3

            if ( x < x_terco * 2 ):
                x_camera = x_camera / 1.5
                if ( x < x_terco ):
                    x_camera = x_camera / 1.2
            if (x_camera < 1):
                x_camera = 1
            pyautogui.moveTo(x_camera, y_camera)

    for contorno2 in contornos2:
        area2 = cv.contourArea(contorno2)
        if area2 > 500: 
            (x,y,w,h) = cv.boundingRect(contorno2)
            #cv.drawContours(frame, contorno, -1, (255,0,0), 2)
            cv.rectangle(frame2, (x,y), (x+w, y+h), (0,255,0),1)
            cv.putText(frame2, f'x: {x}, y: {y}', (x,y-20), cv.FONT_HERSHEY_SIMPLEX, 1,1)
            pyautogui.click(x_camera, y_camera)
            time.sleep(2)

    for contorno3 in contornos3:
        area3 = cv.contourArea(contorno3)
        if area3 > 500: 
            (x,y,w,h) = cv.boundingRect(contorno3)
            #cv.drawContours(frame, contorno, -1, (255,0,0), 2)
            cv.rectangle(frame3, (x,y), (x+w, y+h), (0,255,0),1)
            cv.putText(frame3, f'x: {x}, y: {y}', (x,y-20), cv.FONT_HERSHEY_SIMPLEX, 1,1)
            pyautogui.rightClick(x_camera, y_camera)
            time.sleep(2)
    
    for contorno4 in contornos4:
        area4 = cv.contourArea(contorno4)
        if area3 > 500: 
            (x,y,w,h) = cv.boundingRect(contorno4)
            #cv.drawContours(frame, contorno, -1, (255,0,0), 2)
            cv.rectangle(frame4, (x,y), (x+w, y+h), (0,255,0),1)
            cv.putText(frame4, f'x: {x}, y: {y}', (x,y-20), cv.FONT_HERSHEY_SIMPLEX, 1,1)
            pyautogui.press('Esc')

    k = cv.waitKey(60)
    if k == 27:
        break

cv.destroyAllWindows()