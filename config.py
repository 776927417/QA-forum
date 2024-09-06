
# 分页器
PER_PAGE_COUNT = 2

# secret key 存储session-cookie用--不用重复登陆/验证
SECRET_KEY = "asdfdsa"

# 单独文件
# 配置session，DB,加密等
USERNAME = 'root'
PASSWORD = 'localhost'
HOSTNAME ='127.0.0.1'
PORT = '3306'
DATABASE = 'qaforum_zhiliao'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD, HOSTNAME,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI

# biyjvsszznqwbcci
# 邮箱配置，发件箱
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "776927417@qq.com"
MAIL_PASSWORD = "swvkrsqxmrrjbegd"
MAIL_DEFAULT_SENDER = "776927417@qq.com"


