import numpy as np
import cv2
import serial
import time


ser = serial.Serial('COM5', 9600) 

xml = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(xml)

cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용

cap.set(3, 640) # 너비
cap.set(4, 480) # 높이
time.sleep(2)
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1) # 좌우 대칭
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    print("Number of faces detected: " + str(len(faces)))

    if len(faces):
            # 첫 번째 얼굴 영역 가져오기
        x, y, w, h = faces[0]

        # 얼굴 영역에 사각형 그리기
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # 얼굴의 정중앙 계산
        center_x = x + w // 2
        center_y = y + h // 2

        # 정중앙에 원 표시
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

        # 정중앙 좌표 출력
        print(f"Center of face: ({center_x}, {center_y})")

        # 정중앙 좌표 설정
        x, y = center_x, center_y

        # 데이터를 'x,y' 형식으로 변환
        data = f"{x},{y}\n"

        # 문자열을 바이트로 인코딩하여 전송
        ser.write(data.encode())
        print("write", data)

        # 데이터를 문자열로 읽고 개행 문자 제거
        received = ser.readline().decode().strip()
        print("read", received)

    cv2.imshow('result', frame)
    time.sleep(0.05)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # Esc 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
