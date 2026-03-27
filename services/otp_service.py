import random
from twilio.rest import Client
from config.settings import Settings

class OTPService:
    def __init__(self):
        self.client = None
        if Settings.TWILIO_SID:
            self.client = Client(Settings.TWILIO_SID, Settings.TWILIO_AUTH_TOKEN)
    
    def send_otp(self, phone, otp):
        if not self.client:
            print(f"Demo OTP for {phone}: {otp}")
            return True
        
        try:
            self.client.messages.create(
                body=f"Voting OTP: {otp}",
                from_=Settings.TWILIO_PHONE,
                to=phone
            )
            return True
        except:
            return False
    
    def generate_otp(self):
        return str(random.randint(100000, 999999))