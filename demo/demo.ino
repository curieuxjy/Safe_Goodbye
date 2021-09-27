int Led2 = 2; // LED 연결단자 설정
int Led3 = 3; // LED 연결단자 설정
int Led4 = 4; // LED 연결단자 설정
int Led5 = 5; // LED 연결단자 설정
int Led6 = 6; // LED 연결단자 설정
int Led7 = 7; // LED 연결단자 설정
int Led8 = 8; // LED 연결단자 설정
int Led9 = 9; // LED 연결단자 설정
int buzzer = 10; //부저 단자 설정
int sensorpin = 11; // 센서값을 읽을 단자 설정
int pin1 =12; //모터 정회전 단자 설정
int pin2 =13; //모터 역회전 단자 설정
int detect = 0;
int c=0;

void setup () 
{Serial.begin(9600);
  pinMode (Led2, OUTPUT); // LED 단자를 아웃풋으로 설정
  pinMode (Led3, OUTPUT); // LED 단자를 아웃풋으로 설정
  pinMode (Led4, OUTPUT); // LED 단자를 아웃풋으로 설정
  pinMode (Led5, OUTPUT); // LED 단자를 아웃풋으로 설정
  pinMode (Led6, OUTPUT); // LED 단자를 아웃풋으로 설정
  pinMode (Led7, OUTPUT); // LED 단자를 아웃풋으로 설정
  pinMode (Led8, OUTPUT); // LED 단자를 아웃풋으로 설정
  pinMode (Led9, OUTPUT); // LED 단자를 아웃풋으로 설정toplight
  pinMode (sensorpin, INPUT); // 센서값을 인풋으로 설정
  pinMode(pin1,OUTPUT); // 정회전 출력
  pinMode(pin2,OUTPUT); // 역회전 출력
  
}
 
void loop () 
{while (Serial.available()>0){
  char c = Serial.read();
  if (c=='1'){
  int interval = 500;
  digitalWrite(2,HIGH), digitalWrite(6,HIGH);
  delay(interval);
  digitalWrite(3,HIGH), digitalWrite(7,HIGH);
  delay(interval);
  digitalWrite(4,HIGH), digitalWrite(8,HIGH);
  delay(interval);
  digitalWrite(5,HIGH);//4번째
  delay(interval);
  digitalWrite(9,HIGH);//toplight
  delay(interval);
  detect = digitalRead(11);
 
  
  if(detect == LOW){//센서감지됨
  tone(buzzer,523,3000);//높은도 1000ms울리기
  digitalWrite(9,LOW);
  delay(200);
  digitalWrite(9,HIGH);
  delay(200);
  digitalWrite(9,LOW);
  delay(200);
  digitalWrite(9,HIGH);
  delay(200);
  digitalWrite(9,LOW);
  delay(200);
  digitalWrite(9,HIGH);
  delay(200);
  digitalWrite(2,LOW), digitalWrite(6,LOW);
  digitalWrite(3,LOW), digitalWrite(7,LOW);
  digitalWrite(4,LOW), digitalWrite(8,LOW);
  digitalWrite(5,LOW), digitalWrite(9,LOW);
  delay(1000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,HIGH);//자동문 닫힘
  delay(4000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,LOW);
  delay(3000);
  digitalWrite(pin1,HIGH);
  digitalWrite(pin2,LOW);//자동문 열림
  delay(3000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,LOW);
  delay(3000);
  }

  else{
  digitalWrite(2,LOW), digitalWrite(6,LOW);
  digitalWrite(3,LOW), digitalWrite(7,LOW);
  digitalWrite(4,LOW), digitalWrite(8,LOW);
  digitalWrite(5,LOW), digitalWrite(9,LOW);
  delay(1000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,HIGH);//자동문 닫힘
  delay(4000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,LOW);
  delay(3000);
  digitalWrite(pin1,HIGH);
  digitalWrite(pin2,LOW);//자동문 열림
  delay(3000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,LOW);
  delay(3000);
  }
  }
  
  if (c=='2'){
  int interval = 2000;
  digitalWrite(2,HIGH), digitalWrite(6,HIGH);
  delay(interval);
  digitalWrite(3,HIGH), digitalWrite(7,HIGH);
  delay(interval);
  digitalWrite(4,HIGH), digitalWrite(8,HIGH);
  delay(interval);
  digitalWrite(5,HIGH);//4번째
  delay(interval);
  digitalWrite(9,HIGH);//toplight
  delay(interval);
  detect = digitalRead(11);
 
  
  if(detect == LOW){//센서감지됨
  tone(buzzer,523,2000);//높은도 1000ms울리기
  digitalWrite(9,LOW);
  delay(200);
  digitalWrite(9,HIGH);
  delay(200);
  digitalWrite(9,LOW);
  delay(200);
  digitalWrite(9,HIGH);
  delay(200);
  digitalWrite(9,LOW);
  delay(200);
  digitalWrite(9,HIGH);
  delay(200);
  digitalWrite(2,LOW), digitalWrite(6,LOW);
  digitalWrite(3,LOW), digitalWrite(7,LOW);
  digitalWrite(4,LOW), digitalWrite(8,LOW);
  digitalWrite(5,LOW), digitalWrite(9,LOW);
  delay(3000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,HIGH);//자동문 닫힘
  delay(4000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,LOW);
  delay(3000);
  digitalWrite(pin1,HIGH);
  digitalWrite(pin2,LOW);//자동문 열림
  delay(3000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,LOW);
  delay(3000);
  }

  else{
  digitalWrite(2,LOW), digitalWrite(6,LOW);
  digitalWrite(3,LOW), digitalWrite(7,LOW);
  digitalWrite(4,LOW), digitalWrite(8,LOW);
  digitalWrite(5,LOW), digitalWrite(9,LOW);
  delay(2000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,HIGH);//자동문 닫힘
  delay(3000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,LOW);
  delay(4000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,LOW);
  delay(3000);
  digitalWrite(pin1,HIGH);
  digitalWrite(pin2,LOW);//자동문 열림
  delay(3000);
  digitalWrite(pin1,LOW);
  digitalWrite(pin2,LOW);
  delay(3000);
  }
  }
}
}
