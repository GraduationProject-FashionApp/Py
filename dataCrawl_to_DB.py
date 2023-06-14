import pandas as pd
import mysql.connector

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0705",
    database="FashonApp"
)

mycursor = mydb.cursor()

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("dataCrawl.csv", skiprows=1)

# Loop over the rows in the DataFrame
for _, row in df.iterrows():
    # Prepare an insert statement
    sql = """
    INSERT INTO product_info (product_name, original_price, discounted_price, discount_rate, image_link, search_keyword, purchase_link)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    val = (row["product_name"], row["original_price"], row["discounted_price"], row["discount_rate"], row["image_link"],
           row["search_keyword"], row["purchase_link"])

    # Execute the insert statement
    mycursor.execute(sql, val)

# Commit the transaction
mydb.commit()

print(mycursor.rowcount, "record inserted.")
