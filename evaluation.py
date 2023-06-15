import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score

# CSV 파일 로드
df = pd.read_csv('prediction_results.csv')

# 정답 카테고리 설정
true_category = 'long sleeve top'

# 예측 결과 추출
y_true = df['category']
y_pred = df['predicted_category']

# Confusion Matrix 생성
cm = confusion_matrix(y_true, y_pred)

# 정확도 점수 계산
accuracy = accuracy_score(y_true, y_pred)

# Confusion Matrix 출력
print("Confusion Matrix:")
print(cm)

# 정확도 점수 출력
print("Accuracy Score:", accuracy)

# 정답이 아니라고 예측한 것들 / 정답인 long sleeve top으로 예측한 것들의 비율 계산
predicted_not_true = cm.sum(axis=0) - cm.diagonal()
predicted_as_true = cm.diagonal()
ratio = predicted_not_true / predicted_as_true

# 비율 출력
print("Ratio of predicted not true to predicted as true:")
print(ratio)
