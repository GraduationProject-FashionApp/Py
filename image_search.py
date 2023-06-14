import numpy as np
import pickle
import random
import requests
from keras.models import load_model
from keras.preprocessing.image import image_utils
from keras.applications.resnet import preprocess_input
from sklearn.preprocessing import LabelEncoder
from io import BytesIO
import mysql.connector

# Database credentials
user = "root"
password = "password"
database = "fashonApp"

# Model Loading
model = load_model('my_model.h5')

# Load Label Encoder
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

def predict_category(image_url):
    # Load and preprocess image from url
    response = requests.get(image_url)
    image = image_utils.load_img(BytesIO(response.content), target_size=(224, 224))
    image = image_utils.img_to_array(image)
    image = preprocess_input(image)

    # Create image batch
    image = np.expand_dims(image, axis=0)

    # Predict category
    prediction = model.predict(image)

    # Get category index with highest probability
    category_index = np.argmax(prediction)

    # Convert category index to label
    category = label_encoder.inverse_transform([category_index])[0]

    return category

def get_products_from_category(category):
    # Connect to DB
    mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database=database
    )

    mycursor = mydb.cursor()

    # Execute SQL query to get products from predicted category
    mycursor.execute(f"SELECT pi.* FROM product_info pi JOIN predicted_categories pc ON pi.image_link = pc.image_link WHERE pc.category = '{category}'")

    # Fetch all products
    products = mycursor.fetchall()

    # Select 10 random products
    random_products = random.sample(products, 10)

    return random_products

# Predict category for given image url
image_url = input("Enter the image URL: ")
predicted_category = predict_category(image_url)
print('Predicted category:', predicted_category)

# Fetch 10 random products from the predicted category
products = get_products_from_category(predicted_category)
for product in products:
    print(product)
