import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSignal, QObject
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
with open('./virtualtest/events.json', 'r', encoding='utf-8') as file:
    json_str = file.read()

print(json_str)
# 각 모델의 체인을 정의
def create_model_chain(model_name, prompt_template):
    llm = OllamaLLM(model=model_name)
    prompt = PromptTemplate(input_variables=["input"], template=prompt_template)
    return LLMChain(llm=llm, prompt=prompt)

# 모델별 프롬프트 템플릿 정의
model_1_prompt = "{input}를 학습한다 "
model_2_prompt = "{input}이 모델이 낸 의견에 대해서 허점을 찾아서 반박한다."
model_3_prompt = "두 의견을 바탕으로 결론 도출. 전제: @@중요한 목표@@@ {input} 결론은 분명하게, 모호할 경우 부정으로."
model_4_prompt = "{input} |||| <- 주어진 문장에서 '저 사람은 도둑입니다'를 확인하면 '###감지됨###' 출력."

# 각 모델 체인 생성
model_1_chain = create_model_chain("llama3.1", model_1_prompt)
model_2_chain = create_model_chain("example", model_2_prompt)
model_3_chain = create_model_chain("llama3.1", model_3_prompt)
model_4_chain = create_model_chain("llama3.1", model_4_prompt)

# PyQt5 GUI 애플리케이션 클래스 정의
class LangChainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 레이아웃 설정
        layout = QVBoxLayout()

        # 위젯 생성
        self.label = QLabel("초기 메시지를 입력하세요:")
        layout.addWidget(self.label)

        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)

        self.run_button = QPushButton("실행", self)
        self.run_button.clicked.connect(self.run_chain)
        layout.addWidget(self.run_button)

        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.warning_label = QLabel("")
        layout.addWidget(self.warning_label)

        # 메인 레이아웃 설정
        self.setLayout(layout)
        self.setWindowTitle("LangChain 도둑 탐지 앱")
        self.setGeometry(100, 100, 600, 400)

        # ThreadPool 생성
        self.thread_pool = QThreadPool()

    def run_chain(self):
        # 사용자 입력 가져오기
        initial_message = self.input_field.text()
        if not initial_message:
            self.result_display.setText("입력을 입력해주세요.")
            return

        # 체인 작업 실행
        worker = ChainWorker(initial_message, self.result_display)
        worker.signals.update_result.connect(self.update_result_display)
        worker.signals.finished.connect(self.check_detection)
        self.thread_pool.start(worker)

    def update_result_display(self, message):
        self.result_display.append(message)

    def check_detection(self):
        if '###감지됨###' in self.result_display.toPlainText():
            self.warning_label.setText("경고: 도둑이 감지되었습니다!")
        else:
            self.warning_label.setText("도둑이 감지되지 않았습니다.")

class WorkerSignals(QObject):
    update_result = pyqtSignal(str)
    finished = pyqtSignal()

class ChainWorker(QRunnable):
    def __init__(self, input_text, result_display):
        super().__init__()
        self.input_text = input_text+ "<== 앞의 내용은 불특정 누군가의 입력이다. 그리고 이후의 내용은 너가 처리해야할 주인과 관련된 자료이다. 앞의 누군가의 입력과 자료를 비교하고 그사람이 주인과 동일 인물인지 의견을 내라" + json_str
        self.signals = WorkerSignals()
        self.result_display = result_display

    def run(self):
        # 각 단계별 체인을 실행하고 그 결과를 emit하여 업데이트
        response = self.input_text
        for i, chain in enumerate([model_1_chain, model_2_chain, model_3_chain, model_4_chain], start=1):
            response = chain.run(response)
            self.signals.update_result.emit(f"모델 {i}의 응답:\n{response}\n")
        self.signals.finished.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LangChainApp()
    ex.show()
    sys.exit(app.exec_())
