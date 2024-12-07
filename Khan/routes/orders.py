from flask import Blueprint, request, jsonify
from flask_cors import CORS
import pymssql
import json
import os
from datetime import datetime

orders_bp = Blueprint('orders', __name__)  # 创建蓝图
CORS(orders_bp)  # 允许所有域名跨域请求
# 数据库配置
DB_CONFIG = {
    'server': os.getenv('DB_SERVER', 'LAPTOP-O0S0GFM6'),  # 默认值
    'user': os.getenv('DB_USER', 'sa'),  # 默认值
    'password': os.getenv('DB_PASSWORD', 'gx114514'),  # 默认值
    'database': os.getenv('DB_DATABASE', 'testdb2')  # 默认值
}

# 数据库连接
def get_db_connection():
    return pymssql.connect(
        server=DB_CONFIG['server'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

# API: 接收订单数据并写入数据库
@orders_bp.route('/save', methods=['POST'])
def save_order():
    data = request.json
    order_items = data.get('order_items')  # 订单内容（数组）
    total_price = data.get('total_price')  # 总价

    # 参数验证
    if not all([order_items, total_price]):
        return jsonify({'error': '缺少必要参数'}), 400

    order_items_json = json.dumps(order_items)
    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                insert_query = """
                INSERT INTO Orders (order_items, total_price)
                OUTPUT INSERTED.user_id
                VALUES (%s, %s)
                """
                cursor.execute(insert_query, (order_items_json, total_price))


                # 获取插入的 user_id
                user_id_row = cursor.fetchone()
                conn.commit()  # 记得提交事务
                print("数据已成功插入")
                if user_id_row is None:
                    return jsonify({'error': '订单插入成功，但未获取到订单ID'}), 500
                user_id = user_id_row[0]  # 提取 user_id

        response = {
            'status': 'success',
            'message': '订单已保存',
            'user_id': user_id,
            'order_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(response), 201
    except pymssql.Error as db_err:
        return jsonify({'error': '数据库错误', 'details': str(db_err)}), 500
    except Exception as e:
        print(f'服务器错误: {str(e)}')
        return jsonify({'error': '服务器错误', 'details': str(e)}), 500


# API: 获取所有订单信息
@orders_bp.route('/', methods=['GET'])
def get_orders():
    try:
        with get_db_connection() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute("SELECT * FROM Orders")
                orders = [
                    {
                        'user_id': row['user_id'],  # 使用user_id代替order_id
                        'order_items': json.loads(row['order_items']),
                        'total_price': float(row['total_price']),
                        'order_date' : row['order_date']
                    }
                    for row in cursor
                ]
        return jsonify({'status': 'success', 'orders': orders}), 200

    except pymssql.Error as db_err:
        return jsonify({'error': '数据库错误', 'details': str(db_err)}), 500
    except Exception as e:
        return jsonify({'error': '服务器错误', 'details': str(e)}), 500


# API: 获取订单数量
@orders_bp.route('/count', methods=['GET'])
def get_order_count():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Orders")
                count = cursor.fetchone()[0]  # 获取总数

        return jsonify({'status': 'success', 'count': count}), 200

    except pymssql.Error as db_err:
        return jsonify({'error': '数据库错误', 'details': str(db_err)}), 500
    except Exception as e:
        return jsonify({'error': '服务器错误', 'details': str(e)}), 500




