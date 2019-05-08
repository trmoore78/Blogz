from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hello1@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

page_header  = """ <!DOCTYPE html>
<html>
    <head>
    <a>Welcome to WebCaesar</a> 
    <style>
    form {{
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
            }}
    textarea {{
                margin: 10px 0;
                width: 540px;
                height: 120px;
            }}
        </style>
    </head>
"""
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        return "(%d, %s, %s)"% (self.id,self.title,self.body)
        

posts ={}
count = [0]


@app.route('/Blog', methods=['POST'])
def Blog():
    blog_id = int(request.form['id'])
    id = Blog.query.get(blog_id)
    return render_template('base.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        return render_template('base.html', title=title,body=body)
    else:
        return render_template('post.html')


@app.route("/")
def index():
    all_posts = Blog.query.get.all('id')
    posts = {'posts':all_posts}
    return render_template('base.html', posts)


if __name__ == '__main__':
    app.run()