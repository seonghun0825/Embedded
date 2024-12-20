import serial
import time

# 시리얼 포트와 연결 설정
ser = serial.Serial('COM5', 9600)  # 아두이노가 연결된 포트에 맞게 수정

time.sleep(2)  # 아두이노 초기화 시간 대기

while True:
    angle = input("Enter the servo angle (0-180): ")  # 사용자 입력
    ser.write(angle.encode())  # 입력 값을 시리얼 포트를 통해 아두이노로 전송
    print(f"Sent angle {angle} to Arduino")
    time.sleep(1)  # 1초 대기
