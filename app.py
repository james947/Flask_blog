from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime

#creating blog db with sqlite
conn = sqlite3.connect('blog.db')
c = conn.cursor()
conn.close()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////E:\blog project\blog.db'

db = SQLAlchemy(app)


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)


@app.route('/index')
#index page route 
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/about')
#about route
def about():
    return render_template('about.html')


@app.route('/post/<int:post_id>')
#view post route
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    date_posted = post.date_posted.strftime('%B %d %Y')
    return render_template('post.html',post=post, date_posted=date_posted)


@app.route('/contact')
#contact route
def contact():
    return render_template('contact.html')

@app.route('/createpost')
#create post view
def createpost():
    return render_template('addpost.html')

@app.route('/create', methods=["POST"])
#add new post view
def create():
    #request form data
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    #create variable post to add data to db
    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    #commit to db and end session
    db.session.add(post)
    db.session.commit()
    return redirect (url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



    