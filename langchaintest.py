import json
from langchain_ollama import OllamaLLM

base_regular = "스케줄을 추가할께 응답은 json의 형식으로 시간이 키값이고, 활동이 value 값으로 응답을 내라 문단을 잘 제작하렴, 빠뜨리는 문법없"
model = OllamaLLM(model="example")
response = model.invoke(base_regular+" 10시 기상 12시 출근 5시 퇴")

# 응답을 JSON 형식으로 변환
response_json = json.dumps({"response": response}, ensure_ascii=False, indent=4)
print(response_json)

data = {
    "question": "스케줄입력정보",
    "context": "8시 기상, 10시 퇴"
}

# JSON 데이터를 문자열로 변환
json_input = json.dumps(data, ensure_ascii=False)
print(json_input)
# OllamaLLM에 전달
response = model.invoke(json_input)
print(response)

response= model.invoke(base_regular + "오후 9시 퇴근, 오전7시 기상")
print(response)
