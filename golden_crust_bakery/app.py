from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
import os

app = Flask(__name__)
# Use an absolute path for the database to ensure consistency
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bakery.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_very_secret_key_here' # Needed for session management and flash messages
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Route name for the login page
login_manager.login_message_category = 'info' # Bootstrap category for flash messages


# --- Database Models ---

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    shipping_address = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    orders = db.relationship('Order', backref='customer', lazy=True)
    blog_posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    variety = db.Column(db.String(50), nullable=True)  # e.g., Sourdough, Whole Wheat
    image_url = db.Column(db.String(200), nullable=True, default='default_product.jpg')

    def __repr__(self):
        return f'<Product {self.name}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending') # e.g., Pending, Processing, Shipped, Delivered, Cancelled
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_at_purchase = db.Column(db.Float, nullable=False)
    product = db.relationship('Product') 

    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Product:{self.product_id} Qty:{self.quantity}>'

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content_html = db.Column(db.Text, nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'

# --- End Database Models ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    products_data = Product.query.all()
    return render_template('products.html', products=products_data)

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.phone_number = request.form.get('phone_number')
        current_user.shipping_address = request.form.get('shipping_address')
        
        try:
            db.session.commit()
            flash('Your profile has been updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
        return redirect(url_for('profile'))
        
    return render_template('profile.html', user=current_user)

# For placeholder links in footer - create dummy routes or point them to index for now
@app.route('/contact')
def contact():
    # In a real app, this would render a contact.html page
    return render_template('index.html', message="Contact page coming soon!")

@app.route('/privacy')
def privacy():
    # In a real app, this would render a privacy.html page
    return render_template('index.html', message="Privacy Policy page coming soon!")

@app.route('/blog/<slug>')
def blog_post(slug):
    # Mock data for blog posts - in a real app, this would come from a database
    mock_posts = {
        "the-secret-to-perfect-sourdough": {
            "title": "The Secret to Perfect Sourdough",
            "date": "October 27, 2023",
            "image": "https://via.placeholder.com/800x400/F9A825/3E2723?text=Perfect+Sourdough",
            "content_html": "<p>This is the full content for 'The Secret to Perfect Sourdough'.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse varius enim in eros elementum tristique. Duis cursus, mi quis viverra ornare, eros dolor interdum nulla, ut commodo diam libero vitae erat.</p>"
        },
        "baking-with-autumn-flavors": {
            "title": "Baking with Autumn Flavors",
            "date": "October 22, 2023",
            "image": "https://via.placeholder.com/800x400/5D4037/FFF8E1?text=Autumn+Baking",
            "content_html": "<p>This is the full content for 'Baking with Autumn Flavors'.</p><p>Embrace the season with our favorite fall recipes, featuring pumpkin, apple, and warm spices. Perfect for a cozy weekend treat.</p>"
        },
        "meet-the-baker-marias-story": {
            "title": "Meet the Baker: Maria's Story",
            "date": "October 15, 2023",
            "image": "https://via.placeholder.com/800x400/E53935/FFFFFF?text=Meet+Maria",
            "content_html": "<p>This is the full content for 'Meet the Baker: Maria's Story'.</p><p>Get to know our head baker, Maria, and her journey into the world of artisan bread making. Her passion is an inspiration to us all!</p>"
        },
        "benefits-of-whole-grains": {
            "title": "The Benefits of Whole Grains",
            "date": "October 10, 2023",
            "image": "https://via.placeholder.com/800x400/FFF8E1/212121?text=Healthy+Grains+Post",
            "content_html": "<p>This is the full content for 'The Benefits of Whole Grains'.</p><p>Learn about the nutritional advantages of incorporating more whole grains into your diet, and discover our tastiest whole grain breads.</p>"
        }
    }
    post = mock_posts.get(slug)
    if post:
        return render_template('blog_post.html', 
                               post_title=post['title'], 
                               publish_date=post['date'], 
                               image_url=post['image'],
                               # For the mock HTML content, we might need to adjust how it's rendered
                               # If it's actual HTML, the template should use |safe filter
                               # For now, passing as is, assuming template might just display it or use a placeholder
                               post_content_html=post['content_html'] 
                              )
    # If slug not found, perhaps redirect to blog index or show a 404
    return render_template('blog.html', error_message="Blog post not found.")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Basic validation
        if not username or not email or not password or not confirm_password:
            flash('All fields are required.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        existing_user_username = User.query.filter_by(username=username).first()
        if existing_user_username:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user_email:
            flash('Email address already registered. Please use a different one.', 'error')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during registration: {str(e)}', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_or_email = request.form.get('username') # Field can be username or email
        password = request.form.get('password')
        
        # Try to find user by username or email
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user) # Add 'remember=True' if you want "remember me" functionality
            flash('Login successful!', 'success')
            # Redirect to the page user was trying to access, or profile/index
            next_page = request.args.get('next')
            return redirect(next_page or url_for('profile'))
        else:
            flash('Login unsuccessful. Please check username/email and password.', 'error')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # create_tables_command_func() # Call this once to create tables, then comment out or use a command
    app.run(debug=True, host='0.0.0.0', port=8080)

# Function to create tables, callable from CLI
def create_tables_command_func():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

@app.cli.command("create-db")
def create_db_cli_command():
    """Creates the database tables."""
    create_tables_command_func()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
