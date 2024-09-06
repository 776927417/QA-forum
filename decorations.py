
from functools import wraps
from flask import session, redirect, url_for, request,g

# 自定义装饰器，
# 如果很多函数都需要同样的验证代码，
# 则可以定义装饰器，让整体简洁，减少重复
def login_required(f):
    @wraps(f)
    def check_if_login(*args, **kwargs):
        # 检查用户是否登录
        if not g.user:
            # 如果未登录，重定向到登录页面，并附加原始请求的URL参数
            return redirect(url_for('auth.login'))
        # 如果已登录，继续执行视图函数
        return f(*args, **kwargs)
    return check_if_login
