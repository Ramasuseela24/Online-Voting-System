from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from extensions import mongo
from utils.encryption import encrypt_vote

vote_bp = Blueprint("vote", __name__)

@vote_bp.route("/cast", methods=["POST"])
@jwt_required()
def cast_vote():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if user["hasVoted"]:
        return jsonify({"message": "You already voted"}), 400

    encrypted = encrypt_vote(request.json["candidateId"])

    mongo.db.votes.insert_one({
        "voterId": user_id,
        "encryptedVote": encrypted
    })

    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"hasVoted": True}}
    )

    return jsonify({"message": "Vote cast successfully"})
