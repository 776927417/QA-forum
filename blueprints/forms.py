import wtforms
from sqlalchemy.testing.pickleable import User
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel,EmailCaptchaModel
from exts import db
# Form: 验证前端提交的数据是否符合要求
# validators验证器
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="wrong email format")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4,message="验证码格式错误")])
    username = wtforms.StringField(validators=[Length(min=3,max=20,message="wrong username format")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="wrong password ")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # 自定义验证：
    # 1. 不能重复注册邮箱
    def validate_email(self,field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError("Email already registered")

    # 2. 验证码是否一致
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email,captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError("Wrong captcha")

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="wrong email format")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="wrong password ")])

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message="标题格式错误")])
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误")])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, message="内容格式错误！")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id！")])