
import os
JWT_SECRET_KEY = os.urandom(24)
class Config:
    SECRET_KEY = "supersecretkey"
    JWT_SECRET_KEY = "jwtsecretkey"
    MONGO_URI = "mongodb://127.0.0.1:27017/votingDB"
