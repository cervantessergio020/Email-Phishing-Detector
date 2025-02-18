import mysql.connector
import datetime
  
def insert_email(id, subject, score, issues):
    try:
        conn = mysql.connector.connect(
            host = 'phishingemailproject.cn0geogwil7k.us-east-2.rds.amazonaws.com',
            user = 'admin',
            password = 'EmailProject1',
            database = 'email_database',
        )
        
        cursor = conn.cursor()
        
        now = datetime.timezone.utc()
        cursor.execute("INSERT INTO Email (email_id, user_id, subject, timestamp, score, has_attachment, issues) VALUES (%d, 1, %s, %s, %d, 0, %s)", (id, subject, now, score, issues))
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    
    finally:
        if conn:
            cursor.close()
            conn.close()
