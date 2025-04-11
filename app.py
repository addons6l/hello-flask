


from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)

# 외장하드에 저장된 SQLite DB 경로 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F:/base/posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 경고 제거

db = SQLAlchemy(app)

# 게시글 테이블 구조 정의
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))     # 작성자 추가
    content = db.Column(db.Text)
    admin_comment = db.Column(db.Text)    # 관리자 댓글 필드

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    post = db.relationship('Post', backref=db.backref('comments', lazy=True))


# 홈 페이지 (게시글 목록)
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

# 글 작성 페이지
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        new_post = Post(
            title=request.form['title'],
            author=request.form['author'],  # 작성자 추가
            content=request.form['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    return render_template('write.html')

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        comment_content = request.form['comment']
        new_comment = Comment(post_id=post.id, content=comment_content)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(f'/post/{post_id}')

    return render_template('detail.html', post=post)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 테이블이 없으면 생성

    app.run(debug=True, host='0.0.0.0')
