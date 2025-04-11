from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F:/base/posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 게시글 모델
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    content = db.Column(db.Text)
    admin_comment = db.Column(db.Text)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

# 홈 페이지
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

# 글 작성
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        new_post = Post(
            title=request.form['title'],
            author=request.form['author'],
            content=request.form['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    return render_template('write.html')

# 게시글 상세
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

# ✅ 손익계산서 탭
@app.route('/income', methods=['GET', 'POST'])
def income():
    print("✅🔥🔥🔥🔥🔥🔥🔥 /income 라우트 진입")
    result = None
    if request.method == 'POST':
        raw_data = request.form['statement']
        lines = raw_data.strip().split('\n')
        result = [line.strip() for line in lines if line.strip()]
    return render_template('income.html', result=result)

print("🔥 등록된 URL 목록:")
for rule in app.url_map.iter_rules():
    print(rule)
    
# 실행
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')




