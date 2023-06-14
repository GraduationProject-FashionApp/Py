import csv
import mysql.connector

# MySQL 연결 설정
db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="0705",
  database="fashonApp"
)

# CSV 파일을 읽어들여 DB에 저장합니다.
with open('prediction_results.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # 첫 번째 행은 헤더이므로 건너뜁니다.

    cursor = db_connection.cursor()
    for row in reader:
        image_link, category = row
        query = f"""
            INSERT INTO predicted_categories (image_link, category)
            VALUES ('{image_link}', '{category}');
        """
        cursor.execute(query)

# 모든 INSERT 작업을 완료한 후에는 반드시 commit을 해야 합니다.
db_connection.commit()
