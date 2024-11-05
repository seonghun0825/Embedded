import matplotlib.pyplot as plt
import numpy as np

# 예시 데이터 설정
# 각 모델별 첫 번째 및 두 번째 실행에서 응답 길이
model_responses_1 = [150, 200, 180, 220]  # 첫 번째 실행 응답 길이 (모델 1~4)
model_responses_2 = [160, 190, 170, 230]  # 두 번째 실행 응답 길이 (모델 1~4)

# 모델 이름 설정
models = ['모델 1', '모델 2', '모델 3', '모델 4']

# 그래프 그리기
x = np.arange(len(models))  # x 축 위치
width = 0.35  # 바 너비

fig, ax = plt.subplots()
bar1 = ax.bar(x - width/2, model_responses_1, width, label='첫 번째 실행')
bar2 = ax.bar(x + width/2, model_responses_2, width, label='두 번째 실행')

# 그래프 설정
ax.set_xlabel('모델')
ax.set_ylabel('응답 길이')
ax.set_title('두 번의 실행에서 모델별 응답 길이 비교')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend()

plt.show()
