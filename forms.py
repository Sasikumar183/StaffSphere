from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField,DateField
from wtforms.validators import DataRequired, Email, Length,data_required

class LoginForm(FlaskForm):
    staff_id = StringField('Staff ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dob = StringField('Date of Birth (YYYY-MM-DD)', validators=[DataRequired()])
    qualification = StringField('Qualification', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    staff_id = StringField('Staff ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dob = StringField('Date of Birth (YYYY-MM-DD)', validators=[DataRequired()])
    qualification = StringField('Qualification', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update')

class TrainingRequestForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired()])
    training_provider = StringField('Training Provider', validators=[DataRequired()])
    organization = StringField('Organization', validators=[DataRequired()])
    duration = IntegerField('Duration (in days)', validators=[DataRequired()])
    from_date = DateField('From Date', validators=[DataRequired()])
    to_date = DateField('To Date', validators=[DataRequired()])
    budget = IntegerField('Budget (if applicable)')
    submit = SubmitField('Submit')
