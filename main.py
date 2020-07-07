from flask import Flask,render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user
from datetime import datetime
from flask_mail import Mail
from werkzeug import secure_filename
import json
import os
import math

local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config.update(
    MAIL_SERVER ='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL='True',
    MAIL_USERNAME= params['gmail_uname'],
    MAIL_PASSWORD= params['gmail_pw']
)
mail=Mail(app)
# copy the uri from https://stackoverflow.com/questions/27766794/switching-from-sqlite-to-mysql-with-flask-sqlalchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# since we have not given any username and password while installation of XAMPP so root will be the username
# and password is blank, dbname given in phpmyadmin is mymlblog
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = params['upload_location']
db = SQLAlchemy(app)

# Since we have a contact table in DB so we will make a Contacts class
# Table elements of contacts table are sno, name, email, phone_num, msg, date
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(30),nullable=False)
    phone_num = db.Column(db.String(12),nullable=False)
    msg = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(12),nullable=True)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(80),nullable=False)
    subtitle = db.Column(db.String(80),nullable=False)
    slug = db.Column(db.String(21),nullable=False)
    content = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(12),nullable=True)
    image_file = db.Column(db.String(12), nullable=True)

@app.route('/')
def home():

    posts = Posts.query.filter_by().all()
    #[0:params['no_of_posts']]
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts =posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts']) + int(params['no_of_posts'])]
    # Pagination Logic
    # First page - can not go to Previous page only next page is enabled
    if (page == 1):
        prev = "#"
        next = "/?page=" + str(page +1)
    elif (page==last):
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    # Middle Page - Can go to either previous or next page
    #prev = page -1
    #next = page + 1
    # Last Page - Can only go to previous page
    #prev = page - 1
    #next = _#
    return render_template('index.html',params = params, posts = posts, prev = prev, next = next)
# return 'Hello, World!'

@app.route('/post/<string:post_slug>', methods = ['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params = params,post=post)

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():

    # If the user is already logged in no need to re-authenticate
    if ('user' in session and session['user'] == params['admin_user']):
        posts = Posts.query.all()
        return render_template('dashboard.html', posts=posts)

    if request.method=='POST':
        usermail = request.form.get('Email')
        userpwd = request.form.get('pwd')
        if (usermail == params['admin_user'] and userpwd == params['admin_pw']):
            # set the session variable
            session['useremailid'] = usermail
            posts=Posts.query.all()
            return render_template('dashboard.html',params = params, posts=posts)
    else:
        return render_template('login.html',params = params)

@app.route('/about')
def about():
    return render_template('about.html',params = params)

@app.route("/edit/<string:sno>", methods = ['GET', 'POST'])
def edit(sno):
    #if ('user' in session and session['user'] == params['admin_user']):
        if request.method == 'POST':
            box_title = request.form.get('Title')
            subtitle = request.form.get('subtitle')
            slug = request.form.get('slug')
            content = request.form.get('content')
            image_file = request.form.get('image_file')
            date = datetime.now()
           # print(box_title)
           # print()
           # print(subtitle)
           # print()
           # print(slug)
           # print()
           # print(content)
           # print()

            if sno == '0':
                post = Posts(Title=box_title,subtitle=subtitle,slug =slug,content=content,date=date,image_file=image_file)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.Title = box_title
                post.subtitle= subtitle
                post.slug = slug
                post.content = content
                post.image_file = image_file
                post.date = date
                db.session.commit()
                return redirect('/edit/'+sno)


        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=post)
    #return render_template('edit.html', params=params, sno=sno)

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    #if ('user' in session and session['user'] == params['admin_user']):
        if (request.method == 'POST'):
            f=request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
            return "Uploaded Successfully"

@app.route('/logout')
def logout():
    session.pop('useremailid')
    #logout_user()
    return redirect('/dashboard')
    #if 'useremailid' in session:
    #    username = session['useremailid']
    #    return 'Logged in as ' + username + '<br>' + \
    #           "<b><a href = '/logout'>click here to log out</a></b>"
    #return "You are not logged in <br><a href = '/login'></b>" + \
    #   "click here to log in</b></a>"

@app.route("/delete/<string:sno>", methods = ['GET', 'POST'])
def delete(sno):
    if ('useremailid' in session and session['useremailid'] == params['admin_user']):
        post=Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        #return render_template('dashboard.html', params=params, post=post)
    return redirect('/dashboard')


@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        # Add entry to the database, email, phone_num, msg, date
        name=    request.form.get('name')# Get the values from contact.html
        email=    request.form.get('email')
        phone = request.form.get('phone_num')
        message= request.form.get('msg')

        entry = Contacts(name = name, phone_num = phone, msg = message,date = datetime.now(), email = email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender = email,
                          recipients = [params['gmail_uname']],
                          body = message + '\n' + phone
                          )
    return render_template('contact.html',params = params)

app.run(debug=True)
