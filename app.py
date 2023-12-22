import os
import sys
import click
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)

# Data structure to store posts and replies (for demonstration purposes)
# database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(20))  
    content = db.Column(db.String(100))


class Reply(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))  
    content = db.Column(db.String(100))
    grade = db.Column(db.String(5))  


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    db.session.commit()
    click.echo('Done.')

posts = []
replies = []
results = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts, replies=replies, results=results)

@app.route('/post', methods=['POST'])
def post():
    poster_name = request.form.get('poster')
    post_content = request.form.get('post_content')
    # add to database
    new_post = Post(name=poster_name, content=post_content)
    db.session.add(new_post)
    db.session.commit()
    # if poster_name and post_content:
    #     # posts.append({'poster': poster_name, 'content': post_content})
    #     posts.append(new_post)
    posts = Post.query.all()
    replies = Reply.query.all()
    return render_template('index.html', posts=posts, replies=replies)

@app.route('/reply', methods=['POST'])
def reply():
    replier_name = request.form.get('replier_name')
    reply_content = request.form.get('reply_content')
    grades = request.form.get('grades')

    new_reply = Reply(name=replier_name, content=reply_content, grade = grades)
    db.session.add(new_reply)
    db.session.commit()

    # if replier_name and reply_content and grades:
    #     # replies.append({'replier': replier_name, 'content': reply_content, 'grades': grades})
    #     replies.append(new_reply)

    posts = Post.query.all()
    replies = Reply.query.all()
    return render_template('index.html', posts=posts, replies=replies, results=results)

@app.route('/get', methods=['GET', 'POST'])
def get():
    name = request.form.get('user_name')

    get_result = Post.query.filter_by(name=name).first()

    if get_result:
        # replies.append({'replier': replier_name, 'content': reply_content, 'grades': grades})
        get_result = [get_result]
    else:
        get_result = [{'name':'not found', 'content':'not found'}]

    posts = Post.query.all()
    replies = Reply.query.all()
    return render_template('index.html', posts=posts, replies=replies, get_result=get_result)

@app.route('/update', methods=['PUT'])
def put():
    name = request.form.get('user_name')
    content = request.form.get('content')
    new_content = request.form.get('new_content')

    put_result = Post.query.filter_by(name=name, content=content).first()

    if put_result:
        put_result.content = new_content
        db.session.commit() 
        put_result = [put_result]
    else:
        put_result = [{'name':'not found', 'content':'not found'}]

    posts = Post.query.all()
    replies = Reply.query.all()
    return render_template('index.html', posts=posts, replies=replies, put_result=put_result)
    # return jsonify({'message': 'Resource updated successfully'})
   

@app.route('/delete', methods=['DELETE'])
def delete():
    name = request.form.get('user_name')
    content = request.form.get('content')

    del_result = Post.query.filter_by(name=name, content=content).first()

    if del_result:
        db.session.delete(del_result) 
        db.session.commit()
        del_result = [del_result]
    else:
        del_result = [{'name':'not found', 'content':'not found'}]

    posts = Post.query.all()
    replies = Reply.query.all()
    return render_template('index.html', posts=posts, replies=replies, del_result=del_result)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8000, debug=True)

