# extension扩展文件
# 存在为了解决循环引用
# 一些插件，比如：flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()