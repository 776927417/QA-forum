web flask 知了实战 Q&A forum
回顾与总结：
## -----------------视图函数转跳方式
1. redirect + url_for + '' + py文件名.def函数名 

```python
return redirect(url_for('qa.qa_detail', qa_id=question_id))
```

2. render_template + .html 

   ```python
   return render_template("index.html",questions=search_results)
   ```

## -----------------GET method
——从DB获取data

```python
question	   = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
search_results = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
```

## -----------------POST method
——把数据存入数据库

```python
content = form.content.data
question_id = form.question_id.data
answer = AnswerModel(content = content, question_id = question_id,author_id = g.user.id)
db.session.add(answer)
db.session.commit()
```

##  -----------------前端转跳

带参视图函数，从前端传入参数：
```html
<div class="question-title">
    <a href="{{url_for('qa.qa_detail',qa_id=question.id)}}">		{{question.title}}
    </a>
</div>
```

action转跳到相应接口，使用接口的功能：
——form内用name传参(后端：request.args.get('q'))

```html
<form class="form-inline my-2 my-lg-0" method="GET" 
      action="{{ url_for('qa.search')}}">
    <input class="form-control mr-sm-2" 
           type="search" 		placeholder="关键字" 
           aria-label="Search" 
           name="q">
    <button class="btn btn-outline-success my-2 my-sm-0" 
            type="submit">搜索
    </button>
</form>
```

