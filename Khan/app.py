from flask import Flask
from flask_cors import CORS
from controllers.user_controller import user_controller
from controllers.admin_controller import admin_controller
from routes.menu import menu_bp
from routes.orders import orders_bp
from routes.admin import admin_bp

app = Flask(__name__)
CORS(app)
# 配置 CORS，指定来源和允许的 HTTP 方法

# 注册路由
#app.register_blueprint(user_controller, url_prefix='/user')
#app.register_blueprint(admin_controller, url_prefix='/admin')
app.register_blueprint(menu_bp, url_prefix='/api/menu')  # 注册菜单 API 的蓝图
app.register_blueprint(orders_bp, url_prefix='/api/orders')  # 注册订单 API 的蓝图
app.register_blueprint(admin_bp, url_prefix='/api/admin/')

if __name__ == '__main__':
    app.run(debug=True)
