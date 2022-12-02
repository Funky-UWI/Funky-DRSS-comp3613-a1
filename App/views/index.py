from flask import Blueprint, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user

from App.controllers.auth import authenticate, login_user, logout_user
from App.controllers.user import create_user
from App.controllers.student import *
from App.controllers.review import *

index_views = Blueprint("index_views", __name__, template_folder="../templates")


@index_views.route("/", methods=["GET"])
def index_page():
    if current_user.is_authenticated:
        return render_template("index.html")
    return redirect(url_for('index_views.login_page'))

@index_views.route('/students', methods=['GET'])
def student_manager_page():
    students = get_all_students()
    students_json = [student.toJSON() for student in students]
    return render_template('studentmanager.html', students=students_json)

@index_views.route('/reviews', methods=['GET'])
def review_manager_page():
    reviews = get_all_reviews()
    reviews_json = [review.toJSON() for review in reviews]
    return render_template('reviewmanager.html', reviews=reviews_json)

@index_views.route('/student/<id>', methods=["GET"])
def get_student_reviews_page():
    reviews = get_upvotes_by_review()

@index_views.route("/login", methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route("/login", methods=["POST"])
def login():
    data = request.form
    user = authenticate(data['username'], data['password'])
    if not user:
        flash('Invalid Credentials.')
        return redirect(url_for("index_views.login_page"))
    try:
        login_user(user, remember=False)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("index_views.login_page"))
    return redirect(url_for('index_views.index_page'))

@index_views.route("/logout", methods=["GET"])
def logout_page():
    logout_user()
    return redirect(url_for("index_views.login_page"))

@index_views.route("/signup", methods=['GET'])
def signup_page():
    return render_template('signup.html')


@index_views.route('/signup', methods=["POST"])
def signup():
    data = request.form
    user = create_user(data['username'], data['password'], access=1)
    return redirect(url_for('index_views.login_page', id=user.id))