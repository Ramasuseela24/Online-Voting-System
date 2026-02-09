import random
import datetime

def generate_otp():
    return str(random.randint(100000, 999999))

def otp_expiry():
    return datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
