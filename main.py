from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods= ['GET'])
def index():
    if request.args:
        blog_id = request.args.get('id')
        posts = Blog.query.get(blog_id)
        return render_template('blogpost.html', posts=posts)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', title='Blog Entry', blogs=blogs)

# @app.route('/blog')
# def blog():
    # blog_id = request.args.get('id')

    # if blog_id == None:
        # posts = Blog.query.get(blog_id)
        # return render_template('blogpost.html', post=posts, title='Build-a-blog')

    # else:
        # post= Blog.query.get(blog_id)
        # return render_template('blogpost.html', post=post, title='Blog Entry')

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_entry = request.form['blog-entry']
        title_error = ''
        blog_error = ''

        if not blog_title:
            title_error = "Please Write a Blog Title"
        if not blog_entry:
            blog_error = "Please put something in the entry"

        if not blog_error and not title_error:
            new_entry = Blog(blog_title, blog_entry)
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/blog?id={}'.format(new_entry.id))
        else:
            return render_template('newpost.html', title='New Entry', title_error= title_error, 
            entry_error=blog_error,blog_title=blog_title, blog_entry=blog_entry)
    
    return render_template('newpost.html', title='New Entry')

if __name__ == "__main__":
    app.run()