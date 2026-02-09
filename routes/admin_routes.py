from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from extensions import mongo
from utils.encryption import decrypt_vote

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/results", methods=["GET"])
@jwt_required()
def results():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Admin access only"}), 403

    votes = mongo.db.votes.find()
    results = {}

    for vote in votes:
        candidate = decrypt_vote(vote["encryptedVote"])
        results[candidate] = results.get(candidate, 0) + 1

    return jsonify(results)
