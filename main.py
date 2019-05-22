from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:hello19@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&ZP38'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))
    blogs = db.relationship('Blog',backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
    
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("made it here")
        user = User.query.filter_by(username=username).first()
        print("made it here too")
        if user and user.password == password:
            
            user_login = User(username,password)
            session['user_login'] = user_login
            print("made it if statement")
           # flash("Logged In")
            #return redirect('/newpost')
            return "Hi"
        elif user and user.password != password:
            flash("Password is Incorrect")
            return redirect('/login')
        elif user.username != username:
            flash("Username does not exist")
            return redirect('/login')
    elif request.method == 'GET':
        return redirect('/signup')
    
    return render_template('login.html')

    
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user and existing_user.password == password:
            session['username'] = username
            return redirect('/newpost')
        elif len(username) == 0 or len(password) == 0 or len(password2) == 0:
            flash("One or more fields are invalid. Please try again.")
            return redirect('/signup')
        elif not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/login')
        elif password != password2:
            flash("Passwords do not match.")
            return redirect('/signup')
        elif len(username) < 3 and len(username) >= 1:
            flash("Username must be greater than 3 characters")
            return redirect('/signup')
        elif len(password) < 3 and len(password) >= 1:
            flash("Password must be greater than 3 characters")
            return redirect('/signup')
        else:
            flash('Duplicate user')
            
    return render_template('signup.html')


@app.route('/blog',methods=['GET'])
def blog():
    blog_id = request.args.get('id')
    if blog_id:
        postid = Blog.query.get(blog_id)
        return render_template('display.html',postid=postid)
    
        
@app.route('/newpost',methods=['GET','POST']) 
def newpost():
    if request.method == 'POST':
        new_title = cgi.escape(request.form['title'])
        new_body = cgi.escape(request.form['body'])
        if len(new_title) == 0:
            flash("Please enter a title for your new post")
            return render_template('post.html')
        elif len(new_body) == 0:
            flash("Please enter a body for your new post")
            return render_template('post.html')
        else:
            new_blog = Blog(new_title, new_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id={}'.format(new_blog.id))

    elif request.method == 'GET':
        return render_template('post.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route("/", methods=['POST','GET'])
def index():
    owner = User.query.filter_by(username=session['username']).first()
    
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        blogpost = Blog(new_title,new_body,owner)
        db.session.add(blogpost)
        db.session.commit()

    posts = Blog.query.filter_by(owner=owner)
    return render_template('login.html', title ="Blogz", posts=posts)


if __name__ == '__main__':
    app.run()