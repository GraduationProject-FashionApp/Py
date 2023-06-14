import os
import json
import numpy as np
import pickle
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

# 이미지와 JSON 파일이 있는 디렉토리 경로를 지정합니다.
image_dir = "train1000/image"
json_dir = "train1000/annos"

# 이미지와 JSON 파일 이름을 가져옵니다.
image_files = os.listdir(image_dir)
json_files = os.listdir(json_dir)

# 카테고리 정보와 이미지 데이터를 저장할 리스트를 생성합니다.
categories = []
images = []

# 코드 일부
for image_file in image_files:
    # JSON 파일 이름을 가져옵니다.
    json_file = image_file.split(".")[0] + ".json"

    # JSON 파일이 있는지 확인합니다.
    if json_file in json_files:
        with open(os.path.join(json_dir, json_file)) as f:
            data = json.load(f)
            # 'item1'의 카테고리 이름을 가져옵니다.
            category1 = data['item1']['category_name']
            categories.append(category1)

            # 이미지를 로드하고 사전 처리한 후, images 리스트에 추가합니다.
            image = load_img(os.path.join(image_dir, image_file), target_size=(224, 224))
            image = img_to_array(image)
            image = preprocess_input(image)
            images.append(image)

            # 'item2'가 있는 경우, 'item2'의 카테고리 이름을 가져와 categories 리스트에 추가하고,
            # 같은 이미지를 images 리스트에 다시 추가합니다.
            if 'item2' in data:
                category2 = data['item2']['category_name']
                categories.append(category2)
                images.append(image) # 같은 이미지를 다시 추가합니다.

#--> 카테고리에 라벨인코더 사용하면 숫자가 중요도를 나타낼 수도.. 원핫인코딩 고려
# 라벨 인코더를 생성하고 카테고리를 숫자로 인코딩합니다.
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(categories)

# 라벨 인코더를 파일로 저장합니다.
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

num_classes = len(label_encoder.classes_)
labels = to_categorical(integer_encoded)

# 데이터를 학습 세트와 테스트 세트로 분리합니다.
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# ResNet50 모델을 로드하고 새로운 분류 층을 추가합니다.
base_model = ResNet50(weights='imagenet', include_top=False)
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)  # 출력 노드 수를 num_classes로 설정합니다.

model = Model(inputs=base_model.input, outputs=predictions)

# 모델을 컴파일합니다.
model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# 모델을 훈련합니다.
model.fit(np.array(X_train), np.array(y_train), epochs=10, validation_data=(np.array(X_test), np.array(y_test)))

# 학습된 모델을 저장합니다.
model.save('my_model.h5')