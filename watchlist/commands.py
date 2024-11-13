import click
from watchlist import app, db




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
    
    from watchlist.models import User, Movie
    
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
    
# 生成虚拟数据 （命令行）
@app.cli.command()
def crefakedata():
    
    from watchlist.models import User, Movie
    
    db.create_all()
    
    name = 'Bin Chou'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    
    # 加入虚拟数据
    # user = user(name=name)
    # db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year =m['year'])
        db.session.add(movie)
    
    db.session.commit()
    print('Done.')