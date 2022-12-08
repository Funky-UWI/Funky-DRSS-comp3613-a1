from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity

from App.controllers import (
    create_review,
    get_review,
    get_all_reviews,
    update_review,
    delete_review,
    create_vote_command,
    get_user,
    get_votes_by_staff
)
from App.controllers.auth import identity
from App.controllers.command import get_vote_by_review_and_staff, overwrite_vote
from App.controllers.review import get_reviews_by_user

review_views = Blueprint("review_views", __name__, template_folder="../templates")


# Create review given user id, student id and text
@review_views.route("/api/reviews", methods=["POST"])
@jwt_required()
def create_review_action():
    data = request.json
    review = create_review(
        user_id=data["user_id"], student_id=data["student_id"], text=data["text"]
    )
    if review:
        return jsonify(review.toJSON()), 201
    return jsonify({"error": "review not created"}), 400


# List all reviews
@review_views.route("/api/reviews", methods=["GET"])
@jwt_required()
def get_all_reviews_action():
    reviews = get_all_reviews()
    return jsonify([review.toJSON() for review in reviews]), 200


# Gets review given review id
@review_views.route("/api/reviews/<int:review_id>", methods=["GET"])
@jwt_required()
def get_review_action(review_id):
    review = get_review(review_id)
    if review:
        return jsonify(review.toJSON()), 200
    return jsonify({"error": "review not found"}), 404


# Upvotes post given post id and user id
# DEPRECATED
@review_views.route("/api/reviews/<int:review_id>/vote", methods=["PUT"])
@jwt_required()
def api_vote_review_action(review_id):
    vote_type = request.args.get("type")

    if get_review(review_id) is None:
        return jsonify("Review does not exist.")

    if not vote_type:
        return jsonify("No vote type specified.", 400)

    # if current_identity:
    #     return jsonify(current_identity.toJSON()), 404

    vote = create_vote_command(review_id, current_identity.id, vote_type=vote_type)
    if vote==None:
        old_vote = get_vote_by_review_and_staff(review_id, current_identity.id)
        vote = overwrite_vote(old_vote.id, vote_type)
        VoteType = {
            'upvote': 1,
            'downvote': -1
        }
        if old_vote.vote_type == VoteType[vote_type]:
            print(old_vote.vote_type)
            print(VoteType[vote_type])
            return jsonify("User " + str(current_identity.id) + " has already voted " + vote_type + " for review " +str(review_id) + ". Deleting vote object."), 200

    return jsonify(vote.toJSON())

# @review_views.route("/api/reviews/<int:review_id>/vote", methods=["PUT"]) #/vote?type=upvote
# @jwt_required()
# def vote_review_action(review_id):
#     vote_type = request.args.get("type")

#     if not type:
#         return "No specified vote type. Upvote or downvote.", 400

#     review = get_review(review_id)
#     if not review:
#         return "No such review exists.", 404

#     # # staff should not be able to vote more than once, new votes override older ones
#     # votes = get_votes_by_staff(staff_id=review.user_id)
#     # return jsonify([vote.toJSON() for vote in votes])

#     # staff = get_user(review.user_id)
#     staff = current_identity
#     vote = create_vote_command(review=review, staff=staff, vote_type=vote_type)

#     return jsonify(vote.toJSON())

# Updates post given post id and new text
# Only admins or the original reviewer can edit a review
@review_views.route("/api/reviews/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review_action(review_id):
    data = request.json
    review = get_review(review_id)
    if review:
        if current_identity.id == review.user_id or current_identity.is_admin():
            update_review(review_id, text=data["text"])
            return jsonify({"message": "post updated successfully"}), 200
        else:
            return jsonify({"error": "Access denied"}), 403
    return jsonify({"error": "review not found"}), 404


# Deletes post given post id
# Only admins or the original reviewer can delete a review
@review_views.route("/api/reviews/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review_action(review_id):
    review = get_review(review_id)
    if review:
        if current_identity.id == review.user_id or current_identity.is_admin():
            delete_review(review_id)
            return jsonify({"message": "post deleted successfully"}), 200
        else:
            return jsonify({"error": "Access denied"}), 403
    return jsonify({"error": "review not found"}), 404


# Gets all votes for a given review
@review_views.route("/api/reviews/<int:review_id>/votes", methods=["GET"])
@jwt_required()
def get_review_votes_action(review_id):
    review = get_review(review_id)
    if review:
        return jsonify(review.get_all_votes()), 200
    return jsonify({"error": "review not found"}), 404
