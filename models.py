from datetime import datetime

from exts import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False,unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=False)
    captcha = db.Column(db.String(100), nullable=False)
    # used = db.Column(db.Boolean, default=False)

class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship(UserModel, backref='questions')
    # backref 参数在 UserModel 中自动添加一个 questions 属性，
    # 这样可以通过 user.questions 来查看这个用户发布的所有问题
    # question.author 返回发布该问题的 UserModel 实例

class AnswerModel(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 外键
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # 关系，每个外键都需要一个关系
    question = db.relationship(QuestionModel, backref=db.backref('answers',order_by=create_time.desc()))
    # question.answers

    author = db.relationship(UserModel, backref='answers')
    # users.answers 可以查看该用户的评论