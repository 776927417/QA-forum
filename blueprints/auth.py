import random

from werkzeug.security import generate_password_hash,check_password_hash

from models import EmailCaptchaModel,UserModel
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
import string
from .forms import RegisterForm,LoginForm
# . (单点): 表示当前包（模块）所在的目录。
# .. (双点): 表示当前包的上级目录。

bp = Blueprint("auth", __name__, url_prefix="/auth")

# /auth/login
@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱未注册")
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password,password):
                session["user_id"] = user.id
                return redirect("/")
            else:
                print("密码不正确")
                return redirect(url_for('auth.login'))
        else:
            print(f"form.errors: {form.errors}")
            return redirect(url_for("auth.login"))

# GET：从服务器上获取数据
# POST：将客户端的数据提交给服务器
# /auth/register
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf: wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

# 如果没有指定method，默认get请求
@bp.route('/captcha/email')
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits * 4  # 自然数字符串*4
    captcha = random.sample(source, 4)  # 每次随机取4位,组成验证码
    captcha = "".join(captcha)  # 修改code格式，中间没有符号间隔
    message = Message(subject="知了传课注册验证码", body=f"your verification code is: {captcha}",  # 生成邮件
                      recipients=[email])  # 收件邮箱
    mail.send(message)  # 发送邮件
    # 本地也要缓存一份验证码，用于验证用户输入是否相等
    # 储存在cache中最合适，小体量网站也可以存在DB中
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API 需要固定格式
    # {code: 200/400/500, message:"",data:{}}
    return jsonify({"code": 200, "message": "", "data": None})

@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["2324044921@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功！"

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")