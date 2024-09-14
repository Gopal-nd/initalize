from flask import Flask, jsonify, request, render_template,flash,redirect,url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from form import CraetePostForm
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = 'mysecretkey'  # For session management


app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), default="user")  # 'user' or 'admin'

    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    
    

with app.app_context():
    db.create_all()
    
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CraetePostForm()
    try:
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('home'))
    except:
        return render_template('user.html', usernme="me")    
    return render_template('post.html', form=form)




p = [{
    'author': 'Corey Schafer',
    'title': 'Blog Post 1',
    'content': 'First post content',
    'date_posted': 'April 20, 2018'
},{
    'author': 'Jane Doe',
    'title': 'Blog Post 2',
    'content': 'Second post content',
    'date_posted': 'April 21, 2018'
},{
    'author': 'John Doe',
    'title': 'Blog Post 3',
    'content': 'Third post content',
    'date_posted': 'April 22, 2018'
}]


# A simple route to test the API
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('index.html',posts=posts)

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/child')
def child():
    return render_template('child.html')

@app.route('/home')
def index():
    return "Hello, World!"

@app.route('/users' ,methods=['GET'])
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Add logic to store this data to a database
        new_user = User(username=username, email=email, password=password)
        # For now, we'll just simulate user registration success.
        try:
            db.session.add(new_user)
            db.session.commit()

            # Flash a custom success message
            flash(f'User {username} registered successfully!', 'success')

            return redirect(url_for('users'))
        except:
            # Flash an error message if there's an issue
            flash('There was an issue adding the user. The email might already exist.', 'error')

            return redirect(url_for('register'))

    return render_template('register.html')


# A sample REST API route to get data
@app.route('/api/data', methods=['GET'])
def get_data():
    # Sample data
    data = {
        'message': 'Hello, this is a REST API response',
        'data': [1, 2, 3, 4, 5]
    }
    return jsonify(data)

# A REST API route to post data
@app.route('/api/data', methods=['POST'])
def post_data():
    # Get JSON data from the request
    incoming_data = request.json
    response = {
        'status': 'Success',
        'received': incoming_data
    }
    return jsonify(response), 201


# edit a post

# Route to edit a post
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('view_post', id=id))
    
    return render_template('edit_post.html', post=post)


@app.route('/post/<int:id>')
def view_post(id):
    post = Post.query.get_or_404(id)
    return render_template('view_post.html', post=post)

#delete a post
@app.route('/delete/<int:id>',methods=['POST'])
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))
# Run the Flask app

if __name__ == '__main__':
    app.run(debug=True),
    app.run(host="0.0.0.0", port=5000)