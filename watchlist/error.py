from flask import render_template
from watchlist import app


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