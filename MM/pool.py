import pymysql as mysql

def connectionPool():
    db=mysql.connect(host="localhost",port=3306,user="root",password="Pratik@123",db="mm")
    cmd=db.cursor()
    return (db,cmd)