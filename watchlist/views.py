from flask import redirect, render_template, request, flash, url_for
from flask_sqlalchemy import *
from flask_login import *
from watchlist import app





# 创建电影条目视图函数(主页面)
@app.route('/movie', methods=['GET','POST'])      #显示电影条目用的是get请求

def index():
    
    from watchlist.__init__ import db, login_manager
    from watchlist.models import Movie
    
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



# "编辑条目视图函数"
@app.route('/movie/edit/<int:movie_id>', methods=['GET','POST'])
@login_required
def edit(movie_id):
    
    from watchlist.models import User, Movie
    from watchlist.__init__ import db
    
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
    
    from watchlist.models import User, Movie
    from watchlist import db
    
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
    
    from watchlist.models import User
    
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
    
    from watchlist import db
    
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
    
    from watchlist.models import User
    from watchlist import db
    
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