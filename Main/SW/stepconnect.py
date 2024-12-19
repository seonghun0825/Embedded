
import serial
import time

ser = serial.Serial('COM5', 9600) # 시리얼 포트 설정 (환경에 맞게 변경)
time.sleep(2) # 시리얼 포트 초기화 대기 시간
a = 10
while True:
    if ser.in_waiting > 0:
        arduino_data = ser.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {arduino_data}")
    
    ser.write(f"{a}\n".encode())
    
    time.sleep(1)
