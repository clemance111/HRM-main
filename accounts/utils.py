import math,random
def generate_otp(limit):
    digits = "123456789abcdefghijklmnopqrstuvwxyz"
    OTP = ""
    for i in range(limit) :
        OTP += digits[math.floor(random.random() * len(digits))]
    return OTP.upper()
