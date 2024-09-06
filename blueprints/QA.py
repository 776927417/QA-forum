from flask import Blueprint, render_template, request, g, url_for, redirect,current_app
from flask_paginate import Pagination

import config
from decorations import login_required
from exts import db
from models import QuestionModel, AnswerModel
from .forms import QuestionForm, AnswerForm

bp = Blueprint('qa', __name__, url_prefix='/')

# 帖子主页：呈现所有帖子的标题和概要
@bp.route('/')
def index():
    # 从DB获取用户的提问
    question = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('index.html',questions=question)

# 发布帖子
@bp.route('/qa/publish',methods=['GET','POST'])
@login_required
def publish_question():
    if request.method == 'GET':
        return render_template("publish_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            # 取出前端传入的数据
            title_to_db = form.title.data
            content_to_db = form.content.data
            # 构造数据库的条目结构
            question = QuestionModel(title = title_to_db,content = content_to_db, author = g.user)
            # 存入数据库
            db.session.add(question)
            db.session.commit()
            # todo 跳转到这篇问答的详情页
            return redirect("/")
        else:
            print(f"QA form.errors: {form.errors}")
            return redirect(url_for("qa.publish_question"))

# 看具体帖子的问答情况
# 不需要登录就能看帖
@bp.route('/qa/detail/<qa_id>')
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html",question=question)

# 用户在主页搜索帖子
@bp.route('/search')
def search():
    # 获取搜索框内容
    q = request.args.get('q')
    # 搜索框条件查询，返回结果
    search_results = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("index.html",questions=search_results)

# 把用户在前端填写的answer传入数据库
@bp.route('/answer/publish',methods=['POST'])
def publish_answer():
    form = AnswerForm(request.form)
    print(f"form 所有字段名: {form._fields}")  # 打印出所有字段及其名称
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content = content, question_id = question_id,author_id = g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('qa.qa_detail', qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))