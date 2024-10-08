from langchain_ollama import OllamaLLM

# 모델 1 클래스
class Model1:
    def __init__(self):
        self.model = OllamaLLM(model="llama3.1")
    
    def process(self, message):
        return self.model.invoke(message)

# 모델 2 클래스
class Model2:
    def __init__(self):
        self.basemind ="음... 저게 맞는지 다시 한번 생각해봐야겠어, 부정적으로. 넌 한국인인 부정적인 사람이야"
        self.model = OllamaLLM(model="example")
    
    def process(self, message):
        return self.model.invoke(message)

# 모델 3 클래스
class Model3:
    def __init__(self):
        self.basemind = "두 의견을 듣고 두 의견을 수렴해보세요. 기본 전제는 다음과 같습니다: "
        self.model = OllamaLLM(model="llama3.1")
    
    def process(self, message):
        return self.model.invoke(message)

# 모델 4 클래스
class Model4:
    
    def __init__(self):
        self.model = OllamaLLM(model="llama3.1")
    
    def process(self, message):
        return self.model.invoke(message)

# MultiModel 대화 클래스
class MultiModelConversation:
    def __init__(self):
        # 각 모델 인스턴스를 생성
        self.model_1 = Model1()
        self.model_2 = Model2()
        self.model_3 = Model3()
        self.model_4 = Model4()
        
        # 기본 대화 텍스트 설정
        self.prere = "방안에 권한이 없는 사람이 있다면 그것은 도둑입니다. 권한을 가진 저는 8시에서 10시에 집에 없습니다."
        
        
        self.model_3.basemind += self.prere + " 결국 현재 감지한 저 사람은 도둑인가요?"

    def run_conversation(self, initial_message, conversation_rounds=5):
        # 초기 메시지 설정
        message = initial_message

        for i in range(conversation_rounds):
            # 모델 1이 메시지를 처리하고 응답을 생성
            print(f"모델 1이 받은 메시지: {self.prere}")
            response_1 = self.model_1.process(message + self.prere)
            print(f"모델 1의 응답: {response_1}")
            
            # 모델 2가 모델 1의 응답을 받아 처리하고 새로운 응답을 생성
            print(f"모델 2가 모델 1의 응답을 처리 중...")
            response_2 = self.model_2.process(response_1 + self.model_2.basemind)
            print(f"모델 2의 응답: {response_2}")
            
            # 모델 2의 응답을 다음 라운드에서 모델 1에게 전달할 메시지로 설정
            message = response_2

            print("-" * 50)  # 각 라운드를 구분하는 시각적인 구분선

            # 모델 3의 의견 수렴
            response_3 = self.model_3.process(self.model_3.basemind + response_1 + " 한 명은 이렇게 생각하고 " + response_2 + " 한 명은 이렇게 생각.")
            print(f"모델 3의 응답: {response_3}")
            
            # 모델 4의 응답 처리
            response_4 = self.model_4.process(response_3 + " |||| <- 앞에 문장은 주어진 문장입니다. 길게 말하지 마시고, 이 문맥에서 '저 사람은 도둑입니다'라고 인정하면 문장 안의 내용과 상관없이 문자열 ###감지됨###을 말하세요.")
            print(f"모델 4의 응답: {response_4}")

            # '###감지됨###'이 포함된 응답을 처리
            if '###감지됨###' in response_4:
                print("경고: 도둑이 감지되었습니다!")
                # 도둑이 감지된 경우 추가 행동 수행 (예: 알림, 로그 기록 등)
                break  # 대화를 종료

        print("대화 종료")

# 대화 실행
if __name__ == "__main__":
    # MultiModelConversation 클래스 인스턴스를 생성하고 대화를 실행
    conversation = MultiModelConversation()
    conversation.run_conversation("현재 9시, 지금 방안에 사람이 있어!")
