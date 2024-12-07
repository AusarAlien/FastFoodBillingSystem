import pymssql
import os

# 数据库配置
DB_CONFIG = {
    'server': os.getenv('DB_SERVER', 'LAPTOP-O0S0GFM6'),
    'user': os.getenv('DB_USER', 'sa'),
    'password': os.getenv('DB_PASSWORD', 'gx114514'),
    'database': os.getenv('DB_DATABASE', 'testdb2')
}

def add_order_date_column():
    try:
        # 连接到数据库
        with pymssql.connect(
            server=DB_CONFIG['server'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        ) as conn:
            with conn.cursor() as cursor:
                # 定义 ALTER TABLE SQL 语句
                alter_table_query = """
                ALTER TABLE Orders
                ADD order_date DATETIME NOT NULL DEFAULT GETDATE();
                """
                # 执行 ALTER TABLE 语句
                cursor.execute(alter_table_query)
                conn.commit()  # 提交事务
                print("成功添加列 'order_date' 到表 'Orders'")

    except pymssql.Error as e:
        print(f"数据库错误: {e}")

if __name__ == '__main__':
    add_order_date_column()
