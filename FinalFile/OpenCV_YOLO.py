import numpy as np
import cv2

# YOLO 설정 파일 및 가중치 파일
weights_path = "yolov3.weights"
config_path = "yolov3.cfg"
names_path = "coco.names"

# YOLO 네트워크 및 클래스 이름 로드
net = cv2.dnn.readNet(weights_path, config_path)
with open(names_path, "r") as f:
    classes = f.read().strip().split("\n")

cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
cap.set(3, 640) # 너비
cap.set(4, 480) # 높이

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1) # 좌우 대칭

    # 네트워크에 프레임을 입력으로 제공
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    class_ids = []
    confidences = []
    boxes = []

    # 출력에서 필요한 정보 추출
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # 비최소 억제 기술로 중복 박스 제거
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # 객체 감지 결과 표시
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow('Object Detection', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # Esc 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
