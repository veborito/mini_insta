from flask import render_template, redirect, url_for, flash, request
from app import app, db, images
from app.forms import LoginForm, RegistrationForm, UploadForm, CommentForm
from app.models import User, Comment, Photo
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = CommentForm()
    if form.validate_on_submit():
        photo_id = request.form['photo_id']
        photo = Photo.query.filter_by(id=photo_id).first()
        comment = Comment(text=form.comment.data, author=current_user, photo=photo)
        db.session.add(comment)
        db.session.commit()
        flash('Nice comment bro !')
        return redirect(url_for('index'))
    photos = Photo.query.all()
    return render_template("index.html", title='Home', photos=photos, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Wrong username or password, pls try again')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You registered successfully!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = UploadForm()
    if form.validate_on_submit():
        image_name = images.save(form.photo.data)
        file_url = url_for('static', filename='uploads/' + image_name)
        photo = Photo(name=file_url, author=current_user)
        db.session.add(photo)
        db.session.commit()
    photos = Photo.query.filter_by(user_id=current_user.id).all()
    return render_template('user.html', user=user, form=form, photos=photos)

@app.route('/delete-comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete-photo/<int:photo_id>', methods=['POST'])
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('user', username=current_user.username))
