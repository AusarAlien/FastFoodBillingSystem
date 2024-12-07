from flask import Blueprint, request, jsonify
import pymssql
import os

admin_bp = Blueprint('admin', __name__)

# 数据库配置
DB_CONFIG = {
    'server': os.getenv('DB_SERVER', 'LAPTOP-O0S0GFM6'),
    'user': os.getenv('DB_USER', 'sa'),
    'password': os.getenv('DB_PASSWORD', 'gx114514'),
    'database': os.getenv('DB_DATABASE', 'testdb2')
}

# 数据库连接函数
def get_db_connection():
    return pymssql.connect(
        server=DB_CONFIG['server'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

# API: 获取所有菜单项
@admin_bp.route('/', methods=['GET'])
def get_menu_items():
    try:
        with get_db_connection() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute("SELECT * FROM MenuItems")
                menu_items = cursor.fetchall()
        return jsonify(menu_items), 200

    except pymssql.Error as db_err:
        return jsonify({'error': '数据库错误', 'details': str(db_err)}), 500
    except Exception as e:
        return jsonify({'error': '服务器错误', 'details': str(e)}), 500

# API: 添加新菜单项
@admin_bp.route('/', methods=['POST'])
def add_menu_item():
    data = request.json
    name = data.get('name')
    price = data.get('price')

    if not name or price is None:
        return jsonify({'error': '请提供菜品名称和价格'}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                insert_query = "INSERT INTO MenuItems (name, price) VALUES (%s, %s)"
                cursor.execute(insert_query, (name, price))
                conn.commit()
        return jsonify({'message': '菜品添加成功'}), 201

    except pymssql.Error as db_err:
        return jsonify({'error': '数据库错误', 'details': str(db_err)}), 500

# API: 更新菜单项
@admin_bp.route('/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    data = request.json
    name = data.get('name')
    price = data.get('price')

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                update_query = "UPDATE MenuItems SET name=%s, price=%s WHERE id=%s"
                cursor.execute(update_query, (name, price, item_id))
                conn.commit()
        return jsonify({'message': '菜品更新成功'}), 200

    except pymssql.Error as db_err:
        return jsonify({'error': '数据库错误', 'details': str(db_err)}), 500

# API: 删除菜单项
@admin_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                delete_query = "DELETE FROM MenuItems WHERE id=%s"
                cursor.execute(delete_query, (item_id,))
                conn.commit()
        return jsonify({'message': '菜品删除成功'}), 200

    except pymssql.Error as db_err:
        return jsonify({'error': '数据库错误', 'details': str(db_err)}), 500
