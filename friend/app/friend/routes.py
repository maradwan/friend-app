from friend import app
from flask import Flask, render_template, request, flash, session, url_for, redirect
from forms import ContactForm, SignupForm, SigninForm, FriendsForm
from flask_mail import Message, Mail
from models import db, User, Friends
from flask import Markup

mail = Mail()

app.config['RECAPTCHA_PUBLIC_KEY'] = ''
app.config['RECAPTCHA_PRIVATE_KEY'] = ''

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='WebSite', recipients=['maradwan@gmail.com'])
      msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'

@app.route('/delete')
def delete():

   User.query.filter_by(email = session['email']).delete()
   db.session.commit()
   return redirect(url_for('signout'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
    return redirect(url_for('profile'))    

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
       
      session['email'] = newuser.email
      return redirect(url_for('profile'))
      #return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
   
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).first()


  if user is None:
    return redirect(url_for('signin'))
  else:
   # return redirect(url_for('friends'))
    return render_template('profile.html')

  
@app.route('/friends' , methods = ['GET', 'POST'])
def friends():
  
  form = FriendsForm()

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).first()

  if user is None:
    return redirect(url_for('signin'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('friends.html', form=form)
    else:
      newfriend = Friends(form.f_firstname.data, form.f_lastname.data, form.f_email.data, form.f_phone.data, user.uid )
      db.session.add(newfriend)
      db.session.commit()

      flash('Record was successfully added')
      return redirect(url_for('profile'))
      #return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"

  elif request.method == 'GET':
    return render_template('friends.html', form=form)

@app.route('/showall')
def showall():

   user = User.query.filter_by(email = session['email']).first()
   return render_template('showall.html', friends = Friends.query.filter_by(user_id = user.uid).all())

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  
  if 'email' in session:
    return redirect(url_for('profile')) 
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('home'))
