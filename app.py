from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # SQLite bazasi
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ma'lumotlar bazasida postlarni saqlash uchun model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'

# Ma'lumotlar bazasini yaratish
with app.app_context():
    db.create_all()

# Home page
@app.route('/')
def home():
    posts = Post.query.all()  # Barcha postlarni olish
    return render_template('home.html', posts=posts)

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Register user logic
        return redirect(url_for('login'))
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authentication logic
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Dashboard page for the blog
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = "User"  # Foydalanuvchi nomini qo'shish
        new_post = Post(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('dashboard'))

    posts = Post.query.all()
    return render_template('dashboard.html', posts=posts)

# View individual post
@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)  # Postni id bo'yicha topish
    return render_template('view_post.html', post=post)

# Logout
@app.route('/logout')
def logout():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)


# Dashboard page for the blog
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = "User"  # Foydalanuvchi nomi qo'shish
        new_post = Post(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('dashboard'))  # Yangi post qo'shilgandan so'ng, sahifani yangilash

    posts = Post.query.all()
    return render_template('dashboard.html', posts=posts)
# Postni ko'rish sahifasi
@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)  # post_id asosida postni topish
    return render_template('view_post.html', post=post)
