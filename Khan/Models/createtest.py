import pymssql

# 打开数据库连接
db = pymssql.connect(server='LAPTOP-O0S0GFM6', user='sa', password='gx114514', database='master')

# 创建游标对象，并设置返回数据的类型为字典
cursor = db.cursor(as_dict=True)

# 设置数据库自动提交
db.autocommit(True)

# 直接使用 cursor.execute 来切换到新建的数据库
cursor.execute("USE testdb2")

# 创建表的SQL语句
create_table_query = """
CREATE TABLE Orders (
    user_id INT NOT NULL PRIMARY KEY IDENTITY(1,1),                 
    order_items NVARCHAR(MAX) NOT NULL,       -- 菜单项（JSON格式存储）   
    total_price DECIMAL(10, 2) NOT NULL      -- 总价格
);
"""


# 执行创建表的SQL语句
cursor.execute(create_table_query)
print("Orders 表已创建")

# 关闭游标和数据库连接
cursor.close()
db.close()
