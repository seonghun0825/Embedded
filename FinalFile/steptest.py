
import serial
import time
import math
import cv2
import numpy as np
import picamera2
ser = serial.Serial('/dev/ttyACM0', 9600) # 시리얼 포트 설정 (환경에 맞게 변경)
time.sleep(2) # 시리얼 포트 초기화 대기 시간
a = 0
a1 = 0
c = 0 
Rdata =0
xml = './Ibedded/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(xml)
cam2 = picamera2.Picamera2()
cam2.configure(cam2.create_video_configuration(main={"size": (1680,1232)}))
cam2.start()

def dot_product(vec1, vec2):
    product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    print("Dot product:", product)
    return product

def magnitude(vec):
    mag = math.sqrt(sum(v**2 for v in vec))
    print("Magnitude:", mag)
    return mag

def angle_between(vec1, vec2):
    dot_prod = dot_product(vec1, vec2)
    mag1 = magnitude(vec1)
    mag2 = magnitude(vec2)
    cos_theta = dot_prod / (mag1 * mag2)
    print("Cosine of the angle:", cos_theta)
    angle = math.acos(cos_theta)  # 라디안 단위의 각도
    angle_degrees = math.degrees(angle)  # 각도를 도 단위로 변환
    print("Angle in degrees:", angle_degrees)
    return angle_degrees
center_x =0
center_y = 0
try :
    #여기 a는 파일 까가지고 최근값 넣으면 됨 쉽네
    a = 0
    a1 =0
    with open('/home/hnu/Ibedded/saveData', 'r')as file:
        Rdata = file.read()
    
        
        # f"{a},{a1}\n"
        
    ser.write(f"{Rdata}\n".encode())
    
    arduino_data = ser.readline().decode('utf-8').strip()
    #초기화완료 이다음엔 서버로부터 목표쬔 좌표값 받아서 내적연산후 각도 산출후 적용
    time.sleep(3)
    while True:
        frame = cam2.capture_array()
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grey, 1.1, 5)
        
        # for (x,y,w,h) in faces:
        #     cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0))
        frame_center_x = frame.shape[1]//2
        frame_center_y = frame.shape[0]//2
        cv2.circle(frame,(frame_center_x, frame_center_y),5,(0,0,255),-1)
        if len(faces):
            x,y,w,h = faces[0]
            
            center_x = x + w // 2
            center_y = y + h // 2
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
            cv2.line(frame, (frame_center_x,frame_center_y),(center_x, center_y),(255,255,0),2)
        #일종의 테스트 코드 (input)
        #실제적용환경에선 각 초점 장치들의 산출벡터를 입력받을것
        #사실상 화각 정사영에서 y는 1로 고정이니까 나머지 x만 신경쓰면될듯
        deltax = ((frame_center_x - center_x))/(1680*0.5)
        deltay = ((frame_center_y - center_y))/(1232/2)

        x = [0.0 ,0.1]
        y = [deltax,1.0]
        
        #list(map(float, input("Enter the second vector (comma-separated): ").split(',')))
        #이부분에서 내적연산 들어가고 마무리 result로 전송
        print(f"frame {frame_center_x}, center: {center_x}")
        print(y)
        if(y ==[0,0]):
            y = [0,0.1]    
        a = angle_between(x,y)
        #연산파트 
        cros =np.cross(x,y)
        if (cros > 0):
            a = a
        elif (cros < 0):
            a = -a
        #------------------------   pitch
        x1 = [0.0 ,1.0]
        y1 = [deltay,1.0]
        
        print(y1)
        if(y1 ==[0,0]):
            y1 = [0,0.1]    
        a1 = angle_between(x1,y1)
        #연산파트 
        cros1 =np.cross(x1,y1)
        if (cros1 > 0):
            a1 = a1
        elif (cros1 < 0):
            a1 = -a1
       
        
        print(f"a : {a}\n")
        print(f"a1 : {a1}\n")
        Rdata = f"{a},{a1},{c}" 
        ser.write(f"{Rdata}\n".encode())
        arduino_data1 = ser.readline().decode('utf-8').strip()
        
        print(f"Received from Arduino: {arduino_data1}")
    

        
        
        
        
        cv2.imshow("PiCamera2",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(1) # 시리얼 포트 초기화 대기 시간

except:
    print("종료")
Rdata = f"{a},{-a1}" 
with open('/home/hnu/Ibedded/saveData', 'w')as file:
   file.write(Rdata)




ser.write(f"{Rdata}\n".encode())
cam2.stop()
cv2.destroyAllWindows()
