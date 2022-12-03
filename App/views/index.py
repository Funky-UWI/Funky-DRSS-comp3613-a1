from flask import Blueprint, Response, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required

from App.controllers.auth import authenticate, login_user, logout_user
from App.controllers.user import create_user
from App.controllers.student import *
from App.controllers.review import *

index_views = Blueprint("index_views", __name__, template_folder="../templates")


@index_views.route("/", methods=["GET"])
@login_required
def index_page():
    if current_user.is_authenticated:
        reviews = get_all_reviews()
        reviews_json = [review.toJSON() for review in reviews]
        return render_template("index.html", reviews=reviews_json)
    return redirect(url_for('index_views.login_page'))

@index_views.route('/students', methods=['GET'])
@login_required
def student_manager_page():
    students = get_all_students()
    # search function
    query = request.args
    if query:
        if 'search' in query:
            if query['search'] != "":
                students = get_students_by_name(query['search'])
            else:
                students = get_all_students()
    students_json = [student.toJSON() for student in students]
    return render_template('studentmanager.html', students=students_json)

@index_views.route('/reviews', methods=['GET'])
@login_required
def review_manager_page():
    reviews = get_reviews_by_user(current_user.id)
    # search function
    # query = request.args
    # if query:
    #     if 'search' in query:
    #         if query['search'] != "":
    #             reviews = get_reviews_by_name(query['search'])
    #         else:
    #             reviews = get_all_reviews()
    reviews_json = [review.toJSON() for review in reviews]
    for review in reviews_json:
        review['student'] = get_student(review['student_id']).toJSON()

    return render_template('reviewmanager.html', reviews=reviews_json)

@index_views.route('/review', methods=['POST'])   #/review?student_id=1
@login_required
def new_review():
    student_id = request.args.get('student_id')
    form = request.form
    review = create_review(student_id=student_id, user_id=current_user.id, text=form.get('review_text'))

    reviews = get_reviews_by_user(current_user.id)
    reviews_json = [review.toJSON() for review in reviews]
    return redirect(url_for("index_views.review_manager_page", reviews=reviews_json))

@index_views.route('/review/<id>', methods=['POST'])
@login_required
def edit_review(id):
    data = request.form
    update_review(id, data.get("review_text"))
    return review_manager_page()

@index_views.route('/student/<id>', methods=["GET"])
@login_required
def get_student_reviews_page(id):
    reviews = get_reviews_by_student(id)
    # reviews_json = [review.toJSON() for review in reviews]
    reviews_json = [review.toJSON() for review in reviews]
    for review in reviews_json:
        review['student'] = get_student(review['student_id']).toJSON()
        
    return render_template('studentreviews.html', reviews=reviews_json)



@index_views.route('/student/<id>', methods=["DELETE"])
@login_required
def delete_student_route(id):
    delete_student(id)
    reviews = get_reviews_by_student(id)
    reviews_json = [review.toJSON() for review in reviews]
    return student_manager_page()

@index_views.route('/student/<id>', methods=["POST"])
@login_required
def update_student_route(id):
    data = request.form
    update_student(id, data['edit_name'], data['edit_programme'], data['edit_faculty'])
    return student_manager_page()

@index_views.route('/student', methods=["POST"])
@login_required
def post_new_student():
    data = request.form
    student = create_student(data['name'], data['programme'], data['faculty'])
    return redirect(url_for("index_views.student_manager_page"))


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

@index_views.route("/reviews/<int:review_id>/vote", methods=["POST"])
@login_required
def vote_review_action(review_id):
    # vote_type = request.args.get("type")
    vote_type = request.form.get("type")

    if not type:
        flash("No specified vote type. Upvote or downvote.")
        return Response(status=404)

    review = get_review(review_id)
    if not review:
        flash("Review does not exist.")
        return Response(status=404)

    # # staff should not be able to vote more than once, new votes override older ones
    # votes = get_votes_by_staff(staff_id=review.user_id)
    # return jsonify([vote.toJSON() for vote in votes])

    # staff = get_user(review.user_id)
    staff = current_user
    vote = create_vote_command(review=review, staff=staff, vote_type=vote_type)

    # return jsonify(vote.toJSON())
    reviews = get_reviews_by_user(current_user.id)
    reviews_json = [review.toJSON() for review in reviews]
    # return render_template('reviewmanager.html', reviews=reviews_json)
    # return redirect(url_for("index_views.review_manager_page", reviews=reviews_json))
    # return redirect(url_for("index_views.get_student_reviews_page", reviews=reviews_json))
    return get_student_reviews_page(review.student_id)

# @index_views.context_processor
# def get_user_reviews():
#     reviews = get_reviews_by_user(current_user.id)
#     reviews_json = [review.toJSON() for review in reviews]
#     return {'reviews': reviews_json}

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