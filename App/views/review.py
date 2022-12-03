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
@review_views.route("/api/reviews/<int:review_id>/upvote", methods=["PUT"])
@jwt_required()
def upvote_review_action(review_id):
    review = get_review(review_id)
    if review:
        review.vote(current_identity.id, "up")
        return jsonify(review.toJSON()), 200
    return jsonify({"error": "review not found"}), 404


# Downvotes post given post id and user id
# DEPRECATED
@review_views.route("/api/reviews/<int:review_id>/downvote", methods=["PUT"])
@jwt_required()
def downvote_review_action(review_id):
    review = get_review(review_id)
    if review:
        review.vote(current_identity.id, "down")
        return jsonify(review.toJSON()), 200
    return jsonify({"error": "review not found"}), 404

@review_views.route("/api/reviews/<int:review_id>/vote", methods=["PUT"]) #/vote?type=upvote
@jwt_required()
def vote_review_action(review_id):
    vote_type = request.args.get("type")

    if not type:
        return "No specified vote type. Upvote or downvote.", 400

    review = get_review(review_id)
    if not review:
        return "No such review exists.", 404

    # # staff should not be able to vote more than once, new votes override older ones
    # votes = get_votes_by_staff(staff_id=review.user_id)
    # return jsonify([vote.toJSON() for vote in votes])

    # staff = get_user(review.user_id)
    staff = current_identity
    vote = create_vote_command(review=review, staff=staff, vote_type=vote_type)

    return jsonify(vote.toJSON())

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
