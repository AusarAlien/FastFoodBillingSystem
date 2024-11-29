from flask import Blueprint, jsonify, request
from Models.models import upsert_menu_item

admin_controller = Blueprint('admin_controller', __name__)


# 添加或更新菜单项
@admin_controller.route('/menu-item', methods=['POST'])
def add_or_update_menu_item():
    data = request.json

    # 获取请求数据
    item_id = data.get('item_id')  # 如果是更新，则传 item_id，否则为 None
    name = data.get('name')
    price = data.get('price')

    # 验证必填字段
    if not name or price is None:  # price 需要检查是否为 None，这样可以验证它是否被传入
        return jsonify({"error": "Missing required fields: name and price"}), 400

    # 验证价格是否为有效数字
    if not isinstance(price, (int, float)) or price < 0:
        return jsonify({"error": "Price must be a valid non-negative number"}), 400

    description = data.get('description')
    category = data.get('category')
    image_url = data.get('image_url')
    is_available = data.get('is_available', True)

    success = upsert_menu_item(item_id, name, description, price, category, image_url, is_available)

    if success:
        return jsonify({"message": "Menu item updated successfully"}), 200
    return jsonify({"error": "Failed to update menu item"}), 500

