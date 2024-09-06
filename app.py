
from flask import Flask, session,g
from exts import db,mail
import config
from blueprints.QA import bp as qa_bp
from blueprints.auth import bp as auth_bp
from models import UserModel,QuestionModel # 把定义的table模型 导入
from flask_migrate import Migrate # 将模型导入到DB中

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# ---将其他插件与app绑定, 让flask可以管理实例flask
db.init_app(app) # 绑定db与app
mail.init_app(app)
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return "Hello World!"

# 钩子函数，让网页记住你
@app.before_request
def my_hook_def_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)

# 钩子函数，上下文处理器
@app.context_processor
def my_context_processor():
    return {'user':g.user}

if __name__ == '__main__':
    app.run(debug=True)
