import csv

file_path = './dataCrawl.csv'
temp_file_path = './dataCrawl_temp.csv'

with open(file_path, 'r', newline='', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    rows = [row[:4000] for row in reader]

with open(temp_file_path, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

# 임시 파일을 원본 파일로 덮어쓰기
import shutil
shutil.move(temp_file_path, file_path)
