import numpy as np
import cv2

xml = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(xml)

cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용

cap.set(3, 640) # 너비
cap.set(4, 480) # 높이

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1) # 좌우 대칭
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    print("Number of faces detected: " + str(len(faces)))

    if len(faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # 얼굴의 정중앙 계산
            center_x = x + w // 2
            center_y = y + h // 2
            # 정중앙에 원 표시
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
            # 정중앙 좌표 출력
            print(f"Center of face: ({center_x}, {center_y})")

    cv2.imshow('result', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # Esc 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
