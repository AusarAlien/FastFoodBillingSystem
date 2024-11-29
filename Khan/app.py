from flask import Flask
from controllers.user_controller import user_controller
from controllers.admin_controller import admin_controller

app = Flask(__name__)

# 注册路由
app.register_blueprint(user_controller, url_prefix='/user')
app.register_blueprint(admin_controller, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
