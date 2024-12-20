
import serial
import time
import math
ser = serial.Serial('COM5', 9600) # 시리얼 포트 설정 (환경에 맞게 변경)
time.sleep(2) # 시리얼 포트 초기화 대기 시간
a = 10

#2048 1회전


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

        a = input()

        ser.write(f"{a}\n".encode())
        arduino_data = ser.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {arduino_data}")
    
        
        # time.sleep(1)
        
        
        
    
        
except:
    print("종료")
    


