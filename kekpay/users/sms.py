
def send_message(phone, message):
    print("I am not integrated to any sms services so I just print it here")
    print(f"{phone}, {message}")

def send_verification_message(phone, verification_code):
    message = f"Hello, verification code is: {verification_code}"
    send_message(phone, verification_code)
