
import serial
import time
import math
ser = serial.Serial('COM5', 9600) # 시리얼 포트 설정 (환경에 맞게 변경)
time.sleep(2) # 시리얼 포트 초기화 대기 시간
a = 10

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

try :
    #여기 a는 파일 까가지고 최근값 넣으면 됨 쉽네
    a = 0
    ser.write(f"{a}\n".encode())
    arduino_data = ser.readline().decode('utf-8').strip()
    #초기화완료 이다음엔 서버로부터 목표쬔 좌표값 받아서 내적연산후 각도 산출후 적용

    while True:
        #일종의 테스트 코드 (input)
        #실제적용환경에선 각 초점 장치들의 산출벡터를 입력받을것
        #사실상 화각 정사영에서 y는 1로 고정이니까 나머지 x만 신경쓰면될듯

        x = [0.0, 1.0]
        y = list(map(float, input("Enter the second vector (comma-separated): ").split(',')))
        #이부분에서 내적연산 들어가고 마무리 result로 전송
        print(x)
        a = angle_between(x,y)
        #연산파트 


        ser.write(f"{a}\n".encode())
        arduino_data = ser.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {arduino_data}")
    
        
        # time.sleep(1)
        
        
        
    
        
except:
    print("종료")
    


