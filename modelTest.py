import csv
import numpy as np
import pickle
import requests
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import image_utils
from keras.applications.resnet import preprocess_input
from sklearn.preprocessing import LabelEncoder
import mysql.connector
from io import BytesIO

# MySQL 연결 설정
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0705",
    database="fashonApp"
)

# DB에서 이미지 URL을 가져오기 위한 커서
cursor = db_connection.cursor()

# 모델과 라벨 인코더를 로드합니다.
model = load_model('my_model.h5')
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# SQL 쿼리를 실행하여 image_link를 가져옵니다.
cursor.execute("SELECT image_link FROM product_info")

# 결과를 저장할 csv 파일을 엽니다.
with open('prediction_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['image_link', 'category'])

    # 각 image_link에 대해
    for image_link in cursor.fetchall():
        # 이미지 데이터를 로드합니다.
        response = requests.get(image_link[0])
        image = Image.open(BytesIO(response.content))

        # 이미지가 흑백이라면 RGB로 변환합니다.
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 이미지를 모델의 입력 크기에 맞게 조정합니다.
        image = image.resize((224, 224))

        # 이미지 데이터를 numpy 배열로 변환하고 전처리합니다.
        image = image_utils.img_to_array(image)
        image = preprocess_input(image)
        # 이미지 배치를 생성합니다. (1, 224, 224, 3)
        image = np.expand_dims(image, axis=0)
        # 이미지 카테고리를 예측합니다.
        prediction = model.predict(image)
        # 가장 가능성이 높은 카테고리의 인덱스를 가져옵니다.
        category_index = np.argmax(prediction)
        # 카테고리 인덱스를 레이블로 변환합니다.
        category = label_encoder.inverse_transform([category_index])[0]

        # 예측 결과를 csv 파일에 저장합니다.
        writer.writerow([image_link[0], category])
