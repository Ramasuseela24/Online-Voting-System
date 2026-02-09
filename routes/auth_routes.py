from flask import Blueprint, request, jsonify
from extensions import mongo, bcrypt
from flask_jwt_extended import create_access_token
from utils.otp import generate_otp, otp_expiry
import datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"message": "User already exists"}), 400

    hashed = bcrypt.generate_password_hash(data["password"]).decode()

    mongo.db.users.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": hashed,
        "role": "voter",
        "hasVoted": False
    })

    return jsonify({"message": "Registered successfully"})
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = mongo.db.users.find_one({"email": data["email"]})

    if not user or not bcrypt.check_password_hash(user["password"], data["password"]):
        return jsonify({"message": "Invalid credentials"}), 400

    otp = generate_otp()

    mongo.db.users.update_one(
        {"email": data["email"]},
        {"$set": {"otp": otp, "otpExpires": otp_expiry()}}
    )

    return jsonify({"message": "OTP sent", "otp": otp})
@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    user = mongo.db.users.find_one({"email": data["email"]})

    if not user:
        return jsonify({"message": "User not found"}), 400

    if user["otp"] != data["otp"]:
        return jsonify({"message": "Invalid OTP"}), 400

    if user["otpExpires"] < datetime.datetime.utcnow():
        return jsonify({"message": "OTP expired"}), 400

    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={"role": user["role"]}
    )

    return jsonify({"token": token})
