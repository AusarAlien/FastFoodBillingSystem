import pyodbc
import os
from flask import Blueprint, jsonify, current_app
from flask_cors import CORS

menu_bp = Blueprint('menu', __name__)
CORS(menu_bp)
# 配置数据库连接
DB_CONFIG = {
    'server': os.getenv('DB_SERVER', 'LAPTOP-O0S0GFM6'),  # 默认值
    'user': os.getenv('DB_USER', 'sa'),  # 默认值
    'password': os.getenv('DB_PASSWORD', 'gx114514'),  # 默认值
    'database': os.getenv('DB_DATABASE', 'testdb2')  # 默认值
}

# 连接到 SQL Server 数据库
def get_db_connection():
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={DB_CONFIG["server"]};'
        f'DATABASE={DB_CONFIG["database"]};'
        f'UID={DB_CONFIG["user"]};'
        f'PWD={DB_CONFIG["password"]}'
    )
    return conn

# 获取菜单
@menu_bp.route('/', methods=['GET'])
def get_menu():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM MenuItems")
        menu_items = cursor.fetchall()

        # 将查询结果转化为字典格式
        menu_data = [{
            'id': item.id,
            'name': item.name,
            'price': float(item.price)  # 将价格转换为浮点数
        } for item in menu_items]

        return jsonify(menu_data), 200

    except pyodbc.DatabaseError as db_error:
        print(f"Database error: {db_error}")
        return jsonify({'error': '数据库错误，无法加载菜单'}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': '无法加载菜单'}), 500
    finally:
        # 最后确保数据库连接被关闭
        if 'conn' in locals():
            conn.close()

# 获取菜单项数量
@menu_bp.route('/count', methods=['GET'])
def get_menu_count():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM MenuItems")
        count = cursor.fetchone()[0]  # 获取菜单项数量

        return jsonify({'status': 'success', 'count': count}), 200

    except pyodbc.DatabaseError as db_error:
        print(f"Database error: {db_error}")
        return jsonify({'error': '数据库错误，无法加载菜单项数量'}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': '无法加载菜单项数量'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

