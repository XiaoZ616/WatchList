from flask import *
from flask_sqlalchemy import *
import os
import click
from werkzeug.security import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



app=Flask(__name__)


# ************************************************************Sqlite 数据库*****************************************************************
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(app.root_path, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False             # 关闭对模型修改的监控
db = SQLAlchemy(app)                                             # 实例化数据库


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



#生成数据库表 （命令行）
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


# 生成管理员账户 （命令行）
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=False, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create admin"""
    db.create_all()
    
    admin = User.query.first()
    # 更新管理员
    if admin is not None:
        click.echo('Updating user...')
        admin.username = username
        admin.set_password(password)
    # 创建管理员 
    else:
        click.echo('Creating user...')
        admin = User(username=username, name='Admin')
        User.set_password(password)
        db.session.add(User)
        
    db.session.commit()
    click.echo('Done.')
    
# # 生成虚拟数据 （命令行）
# @app.cli.command()
# def crefakedata():
    
#     db.create_all()
    
#     name = 'Bin Chou'
#     movies = [
#         {'title': 'My Neighbor Totoro', 'year': '1988'},
#         {'title': 'Dead Poets Society', 'year': '1989'},
#         {'title': 'A Perfect World', 'year': '1993'},
#         {'title': 'Leon', 'year': '1994'},
#         {'title': 'Mahjong', 'year': '1996'},
#         {'title': 'Swallowtail Butterfly', 'year': '1996'},
#         {'title': 'King of Comedy', 'year': '1999'},
#         {'title': 'Devils on the Doorstep', 'year': '1999'},
#         {'title': 'WALL-E', 'year': '2008'},
#         {'title': 'The Pork of Music', 'year': '2012'},
#     ]
    
#     # 加入虚拟数据
#     # user = user(name=name)
#     # db.session.add(user)
#     for m in movies:
#         movie = Movie(title=m['title'], year =m['year'])
#         db.session.add(movie)
    
#     db.session.commit()
#     print('Done.')



# flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。
# session 用来在请求间存储数据，它会把数据签名后存储到浏览器的 Cookie 中，
# 所以我们需要设置签名所需的密钥
app.config['SECRET_KEY'] = 'zbt'         # 等同于 app.secret_key = 'zbt'


#****************************************************************Flask_Login 用户认证************************************************************

login_manager = LoginManager(app)        # 实例化扩展类

login_manager.login_view = 'login'
login_manager.login_message = 'OO, 未登录用户不可以哦'

@login_manager.user_loader
def load_user(user_id):                  # 创建用户加载回调函数， 接受用户id最为参数
    user = User.query.get(int(user_id))  # 查找数据库中对应主键的记录
    return user








#**********************************************************************视图函数******************************************************************

# 创建电影条目视图函数(主页面)
@app.route('/movie', methods=['GET','POST'])      #显示电影条目用的是get请求

def index():
    
    if request.method=='POST':
        if not current_user.is_authenticated:     #未登录取消创建功能
            return redirect(url_for('index'))
        else:
            # 获取表单数据
            title = request.form.get('title')
            year = request.form.get('year')
            
            # 服务器端表单提交数据验证
            if not title or not year or len(year)>4 or len(title)>60:
                flash('Invalid input')
                return redirect(url_for('index'))

            movie=Movie(title=title, year=year)
            db.session.add(movie)
            db.session.commit()
            flash('Item created')
            return redirect(url_for('index'))
    
    # 读取记录，传入模板
    movies = Movie.query.all()
    # user = User.query.first()
    return render_template('index.html', movies=movies, current_user=current_user)




# "404报错自定义函数"
@app.errorhandler(404)
def page_not_found(e):
    
    from watchlist.models import User
    
    user = User.query.first()
    return render_template('errors/404.html',user=user),404


# "400报错自定义函数"
@app.errorhandler(400)
def page_not_found(e):
    
    from watchlist.models import User
    
    user = User.query.first()
    return render_template('errors/400.html',user=user),400


# "500报错自定义函数"
@app.errorhandler(500)
def page_not_found(e):
    
    from watchlist.models import User
    
    user = User.query.first()
    return render_template('errors/500.html',user=user),500


# "503报错自定义函数"
@app.errorhandler(503)
def page_not_found(e):
    
    from watchlist.models import User
    
    user = User.query.first()
    return render_template('errors/503.html',user=user),503



# "编辑条目视图函数"
@app.route('/movie/edit/<int:movie_id>', methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie=Movie.query.get(movie_id) #获取指定movie_id的记录
    user=User.query.get(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        
        # 服务器端表单提交数据验证
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            # return redirect(url_for('index', movie_id=movie_id))  # 重定向回对应的编辑页面
        
        
        movie.title=title   #更新电影标题
        movie.year=year     #更新年份
        db.session.commit()
        flash('Item updated')
        return redirect(url_for('index'))
    
    return render_template('edit.html', movie=movie, user=user)



# 删除视图函数
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    user=User.query.first()
    movie=Movie.query.get(movie_id)
    
    db.session.delete(movie)
    db.session.commit()
    flash('Delete Success')
    return redirect(url_for('index'))
    
    # movies=user.query.all()
    # return render_template('index.html',movies=movies,user=user)
    
            
# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        # 是否填写完整
        if not username or not password:
            flash('Invalid input')
            return redirect(url_for('login')) #未填写完直接返回登录界面
         
        #验证用户名和密码是否匹配
        if username == user.username and user.check_password(password):
            login_user(user)                  #Flask_Login提供的登录函数
            flash('Login success.')
            return redirect(url_for('index')) #进入主页
        else:
            flash('Invalid username or password ')
            return redirect(url_for('login')) #返回登录界面
        
    return render_template('login.html')
    
#登出
@app.route('/logout', methods=['POST'])
@login_required      #需要登录
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('login'))
   
   
#重设用户名
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        
        if not name or len(name)>20 :
            flash('Invalid input.')
            return redirect(url_for('settings'))
        
        current_user.name = name                #等于: user = User.query.first()  user.name = name
        db.session.commit()
        flash("Settings updated.")
        return redirect(url_for('index'))
    
    return render_template('settings.html', user=current_user)
    
# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password :
            flash('Lack of username or password.')
            return redirect(url_for('register'))

        if len(username)>20 or len(password) < 5:
            flash('Username too long or password too short.')
            return redirect(url_for('register'))
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Welcome, {username}!')
        return redirect(url_for('login'))
    
    return render_template('register.html')




if __name__=="__main__":
    app.run(debug=1)