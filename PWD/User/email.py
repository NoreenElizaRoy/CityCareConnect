from django.core.mail  import send_mail
import random
from django.conf import settings
from .models import CustomUser
from django.utils.http import urlsafe_base64_encode

def send_otp_via_email(email,otp):
    subject = f'Your account verification email!!'
    #otp = random.randint(1000,9999)
    message = f'Hello!!\n Thank you for signing upon CityCareConnect.for verifying your account OTP -  {otp}'
   
    email_from=settings.EMAIL_HOST
    send_mail(subject , message ,email_from ,[email])
    user_obj=CustomUser.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()

def send_password_reset_email(email,reset_token):
    uidb64 = urlsafe_base64_encode(bytes(email, 'utf-8'))
    
    reset_link=f'http://localhost:8000/api/resetpassword/?uidb64={uidb64}&token={reset_token}'
    subject='Password Reset Request'
    message = f'Hello!!\n You have requested to reset your password.Please click on the following link to reset your password:\n\nReset Link: {reset_link}'
    email_from=settings.EMAIL_HOST
    send_mail(subject , message ,email_from ,[email])
    
    # Assuming you want to save the reset token in the user object for verification later
    user_obj = CustomUser.objects.get(email=email)
    user_obj.reset_token = token_str  # Save the reset token in the user object
    user_obj.save()