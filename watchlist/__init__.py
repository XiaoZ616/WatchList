from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os



app=Flask(__name__)


#***************************配置动态密钥******************************************
# flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。
# session 用来在请求间存储数据，它会把数据签名后存储到浏览器的 Cookie 中，
# 所以我们需要设置签名所需的密钥

app .config['SECRET_KEY']= os.getenv('SECRET_KEY', 'hard_to_guess_string')  #设置密钥，用于加密



# **************************Sqlite 数据库初始化************************************
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.sqlite')) # 设置数据库的地址
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # 关闭对模型修改的监控
db = SQLAlchemy(app)



# **************************LoginManager初始化****************************************
login_manager = LoginManager(app)        # 实例化扩展类

login_manager.login_view = 'login'
login_manager.login_message = 'OO, 未登录用户不可以哦'

@login_manager.user_loader
def load_user(user_id):                  # 创建用户加载回调函数， 接受用户id最为参数
    
    from watchlist.models import User
    
    user = User.query.get(int(user_id))  # 查找数据库中对应主键的记录
    return user



from watchlist import views, errors, commands