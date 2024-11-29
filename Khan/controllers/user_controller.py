from flask import Blueprint, jsonify, request
from Models.models import get_menu_items, submit_order

user_controller = Blueprint('user_controller', __name__)

# 获取菜单项
@user_controller.route('/menu-items', methods=['GET'])
def menu_items():
    items = get_menu_items()
    if items is None:
        return jsonify({"error": "Failed to fetch menu items"}), 500
    return jsonify(items)

# 提交订单
@user_controller.route('/submit-order', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('user_id')
    order_details = data.get('order_details')  # List of items
    total_amount = data.get('total_amount')

    if not (user_id and order_details and total_amount):
        return jsonify({"error": "Missing required fields"}), 400

    order_id = submit_order(user_id, order_details, total_amount)
    if order_id:
        return jsonify({"message": "Order submitted successfully", "order_id": order_id}), 201
    return jsonify({"error": "Failed to submit order"}), 500
