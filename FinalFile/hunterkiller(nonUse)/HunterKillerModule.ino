#include <Servo.h>

Servo servoX, servoY;
int x = 0;
int y = 0;

void setup() {
  Serial.begin(9600);
  servoX.attach(9); // 서보 모터 핀 연결
  servoY.attach(10); // 서보 모터 핀 연결
  servoX.write(90);
  servoY.write(90);
}
void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');  // 데이터를 개행 문자까지 읽음
    processData(data);  // 데이터를 처리하는 함수 호출
    x = map(x, 0, 640, 0, 180);
    y = map(y, 0, 480, 180, 0);
    Serial.print(x);
    servoX.write(x); // 서보 모터 각도 설정
    servoY.write(y);
    // if(angle>0){
    //   servoX.write(90);
    // }el
  }
}

void processData(String data) {
  Serial.print("Received: ");  // 받은 데이터를 확인
  Serial.println(data);

  // 쉼표를 기준으로 문자열 분리
  int commaIndex = data.indexOf(',');
  if (commaIndex > 0) {
    String xStr = data.substring(0, commaIndex);
    String yStr = data.substring(commaIndex + 1);

    x = xStr.toInt();  // x 값 변환 및 저장
    y = yStr.toInt();  // y 값 변환 및 저장

    Serial.print("x: ");
    Serial.print(x);
    Serial.print(", y: ");
    Serial.println(y);
  }
}
