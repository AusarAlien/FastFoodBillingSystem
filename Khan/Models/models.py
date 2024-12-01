from .datebase import get_db_connection

# 获取所有菜单项
def get_menu_items():
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor(as_dict=True)
    cursor.execute("SELECT * FROM MenuItems WHERE is_available = 1")
    items = cursor.fetchall()
    conn.close()
    return items

# 提交订单
def submit_order(user_id, order_details, total_amount):
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        # 插入订单记录
        cursor.execute("""
            INSERT INTO Orders (user_id, order_time, total_amount, payment_status, pickup_status)
            VALUES (%s, GETDATE(), %s, 'Pending', 'Pending')
        """, (user_id, total_amount))
        conn.commit()
        order_id = cursor.lastrowid

        # 插入订单详情
        for detail in order_details:
            cursor.execute("""
                INSERT INTO OrderDetails (order_id, item_id, quantity, customizations)
                VALUES (%s, %s, %s, %s)
            """, (order_id, detail['item_id'], detail['quantity'], detail.get('customizations', '')))
        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        print(f"Error submitting order: {e}")
        return None
    finally:
        conn.close()

# 管理员：添加或更新菜单项
def upsert_menu_item(item_id, name, description, price, category, image_url, is_available):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        if item_id:  # 更新现有项
            cursor.execute("""
                UPDATE MenuItems
                SET name = %s, description = %s, price = %s, category = %s, image_url = %s, is_available = %s
                WHERE item_id = %s
            """, (name, description, price, category, image_url, is_available, item_id))
        else:  # 添加新项
            cursor.execute("""
                INSERT INTO MenuItems (name, description, price, category, image_url, is_available)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, description, price, category, image_url, is_available))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error upserting menu item: {e}")
        return False
    finally:
        conn.close()
