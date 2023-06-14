import numpy as np
import pickle
from keras.models import load_model
from keras.preprocessing.image import image_utils
from keras.applications.resnet import preprocess_input
from sklearn.preprocessing import LabelEncoder

# 모델을 로드합니다.
model = load_model('my_model.h5')

# 라벨 인코더를 로드합니다.
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)
# 예측하려는 이미지를 로드하고 전처리합니다.
image = image_utils.load_img('train1000/image/000002.jpg', target_size=(224, 224))
image = image_utils.img_to_array(image)
image = preprocess_input(image)

# 이미지 배치를 생성합니다. (1, 224, 224, 3)
image = np.expand_dims(image, axis=0)

# 이미지 카테고리를 예측합니다.
prediction = model.predict(image)

# 가장 가능성이 높은 카테고리의 인덱스를 가져옵니다.
category_index = np.argmax(prediction)

# 카테고리 인덱스를 레이블로 변환합니다.
category = label_encoder.inverse_transform([category_index])

print('Predicted category:', category)