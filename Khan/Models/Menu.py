import pymssql


def create_menu_table():
    # 确认数据库连接信息
    server = 'LAPTOP-O0S0GFM6'
    user = 'sa'
    password = 'gx114514'
    database = 'testdb2'

    try:
        # 打开数据库连接
        with pymssql.connect(server=server, user=user, password=password, database=database) as db:
            # 创建游标对象
            with db.cursor() as cursor:
                # 创建表的SQL语句
                create_table_query = """
                CREATE TABLE MenuItems (
                    id INT NOT NULL PRIMARY KEY IDENTITY(1,1),  -- 自增主键
                    name NVARCHAR(100) NOT NULL,                 -- 菜单项名称
                    price DECIMAL(10, 2) NOT NULL                -- 菜单项价格
                );
                """
                # 执行创建表的SQL语句
                cursor.execute(create_table_query)
                print("MenuItems 表已创建")

                # 调用插入数据的函数
                insert_menu_items(cursor)

                # 提交更改
                db.commit()

    except Exception as e:
        print(f"发生错误: {e}")


def insert_menu_items(cursor):
    menu_items = [
        {'name': '宫保鸡丁', 'price': 28},
        {'name': '麻婆豆腐', 'price': 18},
        {'name': '红烧肉', 'price': 38},
        {'name': '鱼香茄子', 'price': 22},
        {'name': '酸辣土豆丝', 'price': 15}
    ]

    insert_query = "INSERT INTO MenuItems (name, price) VALUES (%s, %s)"

    for item in menu_items:
        # 验证价格是否有效
        if item['price'] < 0:
            print(f"价格无效: {item['price']}，未插入 {item['name']}")
            continue
        cursor.execute(insert_query, (item['name'], item['price']))

    print("菜单项已插入")


create_menu_table()
