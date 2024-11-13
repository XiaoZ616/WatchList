from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from watchlist import db


# 创建数据库模型类
class User(db.Model, UserMixin):
    
    
    
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(20))
    username = db.Column(db.String(20))                          # 用户名
    password_hash = db.Column( db.String(128))                   # 密码散列值
    
    def set_password(self, password):  # 设置密码
        self.password_hash = generate_password_hash(password)    # 保存对应密码散列值到对应
        
    def check_password(self, password): # 用于验证密码
        return check_password_hash(self.password_hash, password) # 返回布尔值 
    
class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)                 # 主键
    title = db.Column(db.String(60))                             # 电影标题
    year = db.Column(db.String(4))                               # 电影年份
