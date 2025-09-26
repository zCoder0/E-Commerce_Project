import pymysql

def connect():
    try:
        mycon = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="e_commerce"
        )
        mycur = mycon.cursor()
        return mycon, mycur

    except Exception as e:
        print("Database.py Error:", e)
        return None, None
