from flask import Flask, render_template, request

app = Flask(__name__)

# Data structure to store posts and replies (for demonstration purposes)
posts = []
replies = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts, replies=replies)

@app.route('/post', methods=['POST'])
def post():
    poster_name = request.form.get('poster')
    post_content = request.form.get('post_content')

    if poster_name and post_content:
        posts.append({'poster': poster_name, 'content': post_content})

    return render_template('index.html', posts=posts, replies=replies)

@app.route('/reply', methods=['POST'])
def reply():
    replier_name = request.form.get('replier_name')
    reply_content = request.form.get('reply_content')
    grades = request.form.get('grades')

    if replier_name and reply_content and grades:
        replies.append({'replier': replier_name, 'content': reply_content, 'grades': grades})

    return render_template('index.html', posts=posts, replies=replies)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)

