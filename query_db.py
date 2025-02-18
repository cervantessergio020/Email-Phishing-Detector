import mysql.connector

try:
    conn = mysql.connector.connect(
        host = 'phishingemailproject.cn0geogwil7k.us-east-2.rds.amazonaws.com',
        user = 'admin',
        password = 'EmailProject1',
        database = 'email_database',
    )
    
    cursor = conn.cursor()

except mysql.connector.Error as err:
    print(f"Error: {err}")
        
finally:
    if conn:
        cursor.close()
        conn.close()