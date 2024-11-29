import pymssql

# 数据库配置
DB_CONFIG = {
    "server": "LAPTOP-O0S0GFM6",
    "user": "sa",
    "password": "gx114514",
    "database": "testdb2"
}

def get_db_connection():
    try:
        conn = pymssql.connect(
            server=DB_CONFIG["server"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        return conn
    except pymssql.Error as e:
        print(f"Database connection error: {e}")
        return None
