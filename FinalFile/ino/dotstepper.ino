#include <AccelStepper.h>  // 스텝모터 가속 제어를 위한 라이브러리 추가
#include <math.h>

int FULLSTEP = 4;  // 라이브러리 풀 스텝 설정 계수 정의
int HALFSTEP = 8;  // 라이브러리 하프 스텝 설정 계수 정의
 int data1,data2,res = 0;
int steps_per_rev = 2048;  // 스텝모터 회전 단계 수 정의
String data;
int x,y,c;
// 스텝모터 객체 생성
// 마이크로 스테핑 모드 설정
// 모듈과 연결된 디지털 핀을 IN1-IN3-IN2-IN4 순서로 정의
AccelStepper myStepper1(FULLSTEP, 8,10,9,11);
AccelStepper myStepper2(FULLSTEP, 4, 6, 5, 7); //요축 건들지 마셈

void setup() {
  Serial.begin(9600);
  myStepper2.setMaxSpeed(550);      // myStepper1의 회전 속력 한도를 1000 step/s으로 설정
  myStepper2.setAcceleration(500);    // myStepper1의 회전 가속력을 50 step/s^2으로 설정
  myStepper2.setSpeed(300); 
  myStepper2.moveTo(1);
  
  myStepper1.setMaxSpeed(550);      // myStepper1의 회전 속력 한도를 1000 step/s으로 설정
  myStepper1.setAcceleration(500);    // myStepper1의 회전 가속력을 50 step/s^2으로 설정
  myStepper1.setSpeed(300); 
  myStepper1.moveTo(1);
           // myStepper1의 회전 속력을 200 step/s으로 설정
    // myStepper1의 목표 단계를 2048단계로 설정
  
  //YAW) 750 : 90   1500 : 180
  //PITCH) 500 : 90   1000 : 180
  
}

void loop() {
  
  // 사전에 설정한 대로 myStepper1 동작 시작
  // if (myStepper2.distanceToGo() == 0)  // myStepper1이 목표 단계까지 동작해야할 단계가 0과 같을 경우
  // {
  //   myStepper2.moveTo(-myStepper2.currentPosition());  // myStepper1의 목표 단계를 반대로 설정
  // }
  
  // if(Serial.available() > 0){
  //   data = Serial.readStringUntil('\n');
  //   Serial.print("Received from Python: ");
  //   Serial.println(data);
  // }
  // Serial.println(res); // 데이터 전송
  // delay(1000); // 1초 대기


  // data1 = data.toInt();
  // res = res + data1+100;



//이부분은 모터가 입력에 따라 제대로 작동하는지 알아봤던 시험코드
  if(Serial.available() > 0){
    data = Serial.readStringUntil('\n');
    
    Serial.println(String(data1)+ ","+String(data2)); // 데이터 전송 ###
    //Serial.println(data2); // 데이터 전송 ###
    processData(data);
    // delay(1000); // 1초 대기
    myStepper1.setMaxSpeed(550);      // myStepper1의 회전 속력 한도를 1000 step/s으로 설정
    myStepper1.setAcceleration(500);
    myStepper2.setMaxSpeed(550);      // myStepper1의 회전 속력 한도를 1000 step/s으로 설정
    myStepper2.setAcceleration(500);    // myStepper1의 회전 가속력을 50 step/s^2으로 설정
    
    data1 = x;
    data2 = y;
    int resultX = map(data1, 0, 360, 0, steps_per_rev*3);
    int resulty = map(data2, 0, 360, 0, steps_per_rev*2);
    myStepper2.setSpeed(300);
    myStepper2.moveTo(resultX);
    
    myStepper1.setSpeed(300);
    myStepper1.moveTo(resulty);
    
  }
  myStepper1.run();  // 사전에 설정한 대로 myStepper1 동작 시작
  myStepper2.run();  // 사전에 설정한 대로 myStepper1 동작 시작
  

}
void processData(String data){
  int commaIndex1 = data.indexOf(',');
  

  String num1 = data.substring(0, commaIndex1);
  String num2 = data.substring(commaIndex1 + 1);
  

  x = num1.toInt();
  y = num2.toInt();
  
  
  }
  /*void processData(String data){
  String sy = data. substring(commaIndex +1);
  if(commaIndex > 0) {
    String sx = data.substring(0, commaIndex);
    String sy = data. substring(commaIndex +1);
    
    x = sx.toInt();
    y = sy.toInt();
  }*/
