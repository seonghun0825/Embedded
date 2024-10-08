import json
from langchain_ollama import OllamaLLM

base_regular = "스케줄을 추가할께 응답은 json의 형식으로 시간이 키값이고, 활동이 value 값으로 응답을 내라 문단을 잘 제작하렴, 빠뜨리는 문법없이"
model = OllamaLLM(model="example")

# 응답을 JSON 형식으로 변환
response_json = json.dumps({
                        "10시" : "기상",
                        "12시" : "출근",
                        "13시" : "중식",
                        "17시" : "퇴근",
                        "19시" : "석식",
                        "22시" : "취침"                        
                        }, ensure_ascii=False, indent=4)
print(response_json)

data = {
    "question": "스케줄입력정보",
    "context": {
        "8시" : "기상",
        "9시" : "출근",
        "12시" : "중식",
        "18시" : "석식",
        "20시" : "퇴근",
        "23시" : "취침"
        }
}

# JSON 데이터를 문자열로 변환
json_input = json.dumps(data, ensure_ascii=False, indent=4)
print(json_input)

# OllamaLLM에 전달
response = model.invoke(json_input)
print(response)

response= model.invoke(base_regular + "오후 9시 퇴근, 오전7시 기상")
print(response)

# 두 모델 인스턴스 생성
model_1 = OllamaLLM(model="llama3.1")
model_2 = OllamaLLM(model="example")
model_3 = OllamaLLM(model="llama3.1")
model_4 = OllamaLLM(model="llama3.1")
base = "방안에 권한이 없는 사람이 있다면 그것은 도둑입니다.권한을 가진저는 8시에서 10시에 집에 없습니다"
base1 = "음...저게맞는지 다시한번 생각해봐야겠어, 부정적으로"
SUM = "두 의견을 듣고 두의견을 수렴해보세요" + "기본 전제는 다음과 같습니다" + base + "결국 현재 감지한 저 사람은 도둑인가요? 도둑이 맞다면 스크립트제어를 위해 특수문자'@'를 표기해주세요"

# 초기 메시지 설정
message = "현재 9시, 지금 방안에 사람이있어!"
conversation_rounds = 5

# 두 모델이 대화하는 과정에서 각 모델의 역할을 명확하게 구분
for i in range(conversation_rounds):
    
    # 모델 1이 메시지를 처리하고 응답을 생성
    print(f"모델 1이 받은 메시지: {message}")
    response_1 = model_1.invoke(message + base)
    print(f"모델 1의 응답: {response_1}")
    
    # 모델 2가 모델 1의 응답을 받아 처리하고 새로운 응답을 생성
    print(f"모델 2가 모델 1의 응답을 처리 중...")
    response_2 = model_2.invoke(response_1 + base1)
    print(f"모델 2의 응답: {response_2}")
    
    # 모델 2의 응답을 다음 라운드에서 모델 1에게 전달할 메시지로 설정
    message = response_2

    print("-" * 50)  # 각 라운드를 구분하는 시각적인 구분선

    # 모델 3의 의견 수렴
    response_3 = model_3.invoke(SUM + response_1 + " 한명은 이렇게 생각하고 " + response_2 + " 한명은 이렇게 생각")
    print(f"모델 3: {response_3}")
    
    # 모델 4의 응답 처리
    response_4 = model_4.invoke(response_3 + "|||| <-앞에문장은 주어진 문장입니다.길게 말하지 마시고. 이 문맥에서 '저사람은 도둑입니다'라고 인정하면 문장안의 내용과 상관없이 문자열 ###감지됨###을 말하세요.")
    print(f"모델 4: {response_4}")

    # '###감지됨###'이 포함된 응답을 처리
    if '###감지됨###' in response_4:
        print("경고: 도둑이 감지되었습니다!")
        # 도둑이 감지된 경우 추가 행동 수행 (예: 알림, 로그 기록 등)
        break  # 대화를 종료

print("대화 종료")


