#include <Servo.h>
#include "HX711.h"

// 서보 설정
Servo ESC;

// 회전 속도(Tacho) 설정
unsigned long rpmtime;  // 회전 시간 측정 변수
float rpmfloat;  // 회전 속도 계산을 위한 변수
unsigned int rpm;  // 회전 속도 값
bool tooslow = 1;  // 회전 속도가 너무 느릴 때를 나타내는 플래그

const int INTERRUPT_SENSOR_PIN = 2;  // 인터럽트 센서 핀 설정

// 로드 셀 설정
const int LOADCELL_DOUT_PIN = 5;  // 로드 셀 데이터 핀
const int LOADCELL_SCK_PIN = 6;  // 로드 셀 클럭 핀
HX711 scale;  // HX711 로드 셀 객체 생성
int powerLevel;  // 서보 파워 레벨

long zero = 345303;  // 로드 셀 영점 설정값
long weight_read = 652664;  // 로드 셀 측정값
long weight = 185.6;  // 실제 무게값

bool test_mode = false;  // 테스트 모드 플래그

void setup() {
  Serial.begin(115200);  // 시리얼 통신 초기화, 115200 보드레이트 설정
  TCCR3A = 0;  // 타이머/카운터 제어 레지스터 A 설정
  TCCR3B = 0b00000100;  // 프리스케일러 256 설정
  TIMSK3 = 0b00000001;  // 타이머 오버플로우 인터럽트 활성화
  
  ESC.attach(8);  // 서보 핀 8에 연결
  pinMode(2, INPUT);  // 센서 핀을 입력 모드로 설정

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);  // 로드 셀 초기화
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_SENSOR_PIN), RPM, FALLING);  // 인터럽트 설정
}

void loop() {
  float cal_factor = (weight_read - zero) / weight;  // 로드 셀 보정 계수 계산

  static char receivedData[10];  // 수신된 데이터를 저장할 배열 (최대 10자리 숫자)
  static byte dataIndex = 0;  // 데이터 인덱스 초기화

  // 시리얼로부터 데이터 수신
  while (Serial.available() > 0) {
    char receivedChar = Serial.read();  // 수신된 문자 읽기

    if (receivedChar == '\n') {
      // 데이터 수신 완료 시 처리

      receivedData[dataIndex] = '\0';  // 수신된 데이터 끝에 null 문자 추가
      int receivedNumber = atoi(receivedData);  // 문자열을 정수로 변환
      powerLevel = receivedNumber;  // 파워 레벨 업데이트

      // 다음 데이터 수신을 위해 인덱스 초기화
      dataIndex = 0;
    } else {
      // 수신된 문자를 버퍼에 추가
      receivedData[dataIndex] = receivedChar;

      // 인덱스를 증가시키고, 버퍼 오버플로우를 방지
      if (dataIndex < sizeof(receivedData) - 1) {
        dataIndex++;
      } else {
        // 버퍼 오버플로우 처리 필요 시 추가
      }
    }
  }

  int thrusttoservo = map(0, 100, 0, 90, powerLevel);  // 파워 레벨을 서보 각도로 변환
  
  ESC.write(thrusttoservo);  // 서보 모터에 각도 명령 전달
  
  Serial.print("powerLevel: ");
  Serial.print(powerLevel);
  Serial.print("_");
    
  delay(1000);  // 1초 대기
  Serial.print("RPM: ");
  
  if (tooslow == 1) {  // 회전 속도가 너무 느린 경우
    Serial.print("-1");
  }
  else {  // 회전 속도를 계산하여 출력
    rpmfloat = 60 / (rpmtime / float((16000000 / 256)));
    rpm = round(rpmfloat);
    Serial.print(rpm);
  }
  Serial.print("_");

  if (scale.is_ready()) {  // 로드 셀이 준비되었는지 확인
    long reading = scale.read();  // 로드 셀 데이터 읽기
    Serial.print("HX711 reading: ");
    Serial.print(reading);
    Serial.print("_Thrust: ");
    Serial.print((reading - zero) / cal_factor);  // 추력을 계산하여 출력
  } else {
    Serial.print("HX711 not found_Thrust: -1");  // 로드 셀을 찾지 못한 경우 출력
  }

  Serial.println();  // 줄 바꿈
}

// 타이머 오버플로우 인터럽트 서비스 루틴
ISR(TIMER3_OVF_vect) {
  tooslow = 1;  // 회전 속도가 너무 느린 상태로 설정
}

// 회전 속도를 측정하는 인터럽트 서비스 루틴
void RPM () {
  rpmtime = TCNT3;  // 타이머 카운터 값을 읽음
  TCNT3 = 0;  // 타이머 카운터를 0으로 리셋
  tooslow = 0;  // 회전 속도가 느리지 않음을 표시
}
