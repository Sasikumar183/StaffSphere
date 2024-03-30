from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, EditProfileForm,TrainingRequestForm

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    staff_id = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class TrainingRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(20), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    training_provider = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Integer)
    status = db.Column(db.String(20), default='Pending')
with app.app_context():
    db.create_all()

# Route for user login
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        staff_id = form.staff_id.data
        password = form.password.data

        user = User.query.filter_by(staff_id=staff_id).first()

        if user and user.password == password:
            # Authentication successful, store user's ID in session
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid staff ID or password. Please try again.', 'danger')

    return render_template('login.html', form=form)

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Extract registration data from the form
        name = form.name.data
        dob = form.dob.data
        qualification = form.qualification.data
        role = form.role.data
        phone = form.phone.data
        email = form.email.data
        address = form.address.data
        staff_id = form.staff_id.data
        password = form.password.data

        # Create a new user instance
        new_user = User(name=name, dob=dob, qualification=qualification, role=role,
                        phone=phone, email=email, address=address,
                        staff_id=staff_id, password=password)

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        # Fetch user details from database based on user ID
        user = User.query.get(user_id)
        if user:
            staff_name = user.name

            # Fetch training requests specific to the logged-in user
            training_requests = TrainingRequest.query.filter_by(staff_id=user.staff_id).all()

            return render_template('landing.html', staff_name=staff_name, training_requests=training_requests)
    
    # If user is not logged in or user details not found, redirect to login page
    return redirect(url_for('login'))
    

@app.route('/training/request', methods=['GET', 'POST'])
def training_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            print("Hello")
            staff_name = user.name
            form = TrainingRequestForm()
            if request.method == 'POST':
                print("Working")
                course_name = form.course_name.data
                training_provider = form.training_provider.data
                organization = form.organization.data
                duration = form.duration.data
                from_date = form.from_date.data
                to_date = form.to_date.data
                budget = form.budget.data
                print(budget)
                
                new_training_request = TrainingRequest(staff_id=user.staff_id, course_name=course_name,
                                                            training_provider=training_provider, organization=organization,
                                                            duration=duration, from_date=from_date, to_date=to_date,
                                                            budget=budget)

                # Add the new training request to the database
                db.session.add(new_training_request)
                db.session.commit()
                flash('Training request submitted successfully!', 'success')
                return redirect(url_for('dashboard'))


            return render_template('training.html', form=form, staff_name=staff_name)
    return redirect(url_for('dashboard'))


# Route for editing user profile
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            user_details = {
                'name': user.name,
                'dob': user.dob,
                'qualification': user.qualification,
                'role': user.role,
                'phone': user.phone,
                'email': user.email,
                'address': user.address
            }
            if form.validate_on_submit():
                # Update user details in the database
                user.name = form.name.data
                user.dob = form.dob.data
                user.qualification = form.qualification.data
                user.role = form.role.data
                user.phone = form.phone.data
                user.email = form.email.data
                user.address = form.address.data
                db.session.commit()
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('dashboard'))
            return render_template('edit.html', form=form, user_details=user_details)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username and password match
        if username == 'admin' and password == 'Admin@123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_index'))
        else:
            return render_template('admin_login.html', message='Invalid credentials. Please try again.')
    return render_template('admin_login.html')

# Admin index route
# Logout route
@app.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/index')
def admin_index():
    if session.get('admin_logged_in'):
        # Fetch training requests from the database
        training_requests = TrainingRequest.query.all()
        return render_template('admin_index.html', training_requests=training_requests)
    else:
        return redirect(url_for('admin_login'))

@app.route('/get_history', methods=['GET', 'POST'])
def get_history(): 
    staff_name = None  # Default value for staff name

    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        
        # Retrieve user details from the database based on staff ID
        user = User.query.filter_by(staff_id=staff_id).first()
        if user:
            staff_name = user.name 
            print(staff_name)
            
        # Retrieve training requests for the specified staff ID from the database
        accepted_requests = TrainingRequest.query.filter_by(staff_id=staff_id, status='Accepted').all()
        rejected_requests = TrainingRequest.query.filter_by(staff_id=staff_id, status='Rejected').all()
        pending_requests = TrainingRequest.query.filter_by(staff_id=staff_id, status='Pending').all()

        return render_template('gethistory.html', 
                               accepted_requests=accepted_requests,
                               rejected_requests=rejected_requests,
                               pending_requests=pending_requests,
                               staff_name=staff_name)  # Pass staff name to the template

    return render_template('gethistory.html', staff_name=staff_name)  # Pass staff name to the template for GET requests




@app.route('/update_request/<int:request_id>', methods=['POST'])
def update_request(request_id):
    # Check if the admin is logged in
    if session.get('admin_logged_in'):
        # Get the action (accept or reject) from the form submission
        action = request.form.get('action')

        # Fetch the training request from the database
        training_request = TrainingRequest.query.get(request_id)

        if training_request:
            if action == 'accept':
                # Update the status of the training request to 'Accepted' in the database
                training_request.status = 'Accepted'
                db.session.commit()
                flash('Training request accepted successfully!', 'success')
            elif action == 'reject':
                # Update the status of the training request to 'Rejected' in the database
                training_request.status = 'Rejected'
                db.session.commit()
                flash('Training request rejected successfully!', 'success')
            else:
                flash('Invalid action!', 'danger')

            # Redirect back to the admin index page after updating the request
            return redirect(url_for('admin_index'))
        else:
            flash('Training request not found!', 'danger')
            return redirect(url_for('admin_index'))
    else:
        flash('You must be logged in as admin!', 'danger')
        return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
