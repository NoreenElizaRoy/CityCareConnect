from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import OfficialSerializer,CustomUserSerializer,VerifyAccountSerializer,UserProfileSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
from .models import Official,CustomUser
import jwt,datetime
from .email import *
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render 
from django.utils.http import  urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

#user reg
class RegisterView(APIView):
    def post(self,request):
        serializer=CustomUserSerializer(data=request.data)
        if serializer.is_valid():
          email = serializer.validated_data['email']
          password = serializer.validated_data['password']
          otp = generate_otp()
          user = CustomUser.objects.create(email=email,password=password,is_verified=False,otp=otp)
          send_otp_via_email(email,otp)
          return Response({'message':'Registartion successful.Check your eamil for verification'},status=status.HTTP_201_CREATED,headers={'Location':'/veriftotp'})
          
          return HttpResponseRedirect('/verifyotp')
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
def generate_otp():
     return random.randint(1000,9999)
#both user and staff   

class LoginView(APIView):
        def post(self,request):
          email= request.data.get('email')
          password= request.data.get('password')

          if not email or not password:
            raise AuthenticationFailed("Email and password are required.")
          
          try:  
            custom_user=CustomUser.objects.filter(email=email).first()
            if custom_user and custom_user.check_password(password):                    
              payload = {
                 "user_id": custom_user.user_id,
                 "email" : custom_user.email,
                 "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                 "iat" : datetime.datetime.utcnow(),
                 "is_staff":False
              }
              token = jwt.encode(payload, "secret",algorithm="HS256")
              response= Response(data={"jwt":token,"user":payload})
              response.set_cookie(
              key="jwt",
              value=token,
              httponly=False,
              samesite="None",
              secure=True,
              path="/" )              
              return response
            else:
                raise AuthenticationFailed("Invalid password!!!")  
          except CustomUser.DoesNotExist:
            pass
                
          try:
              #check if user is an official``
            official=Official.objects.filter(email=email).first()
            if official and official.check_password(password):     
                  
               payload = {
                 "user_id": official.id,
                 "email" : official.email,
                 "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                 "iat" : datetime.datetime.utcnow(),
                 "is_staff":True}
               token = jwt.encode(payload, "secret",algorithm="HS256")
               response= Response()
               response.set_cookie(
                key="jwt",
                value=token,
                httponly=False,
                samesite="None",
                secure=True,
                path="/" )
               response.data={ "jwt":token, "user": payload }
               return 
            else:
                raise AuthenticationFailed("Invalid password")  
            
          except Official.DoesNotExist:
            pass
          raise AuthenticationFailed("Invalid email or password")          


#retrive only user from cookie
class UserView(APIView): 
     def get(self,request):       
        token=request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
             payload = jwt.decode(token, 'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = CustomUser.objects.filter(user_id=payload['user_id']).first()
        serializer = CustomUserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
     def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
             'message':'Success'
        }
        return response
     
#Registartion for staff
class StaffRegistration(APIView):
     def post(self,request):
          serializer = OfficialSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save(is_staff=True)
          return Response(serializer.data)

class UserEditProfileView(APIView):
    def get(self,request):
        token=request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("User is not authenticated")
        try:
            payload=jwt.decode(token,"secret",algorithm=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("User is not authenticated")
        user=CustomUser.objects.get(user_id=payload['user_id'])
        serializer=CustomUserSerializer(user) 
        return Response(serializer.data)   
    
    def put(self,request):
        token=request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("User not authenticated")
        try:
            payload=jwt.decode(token,'secret',algorithm=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("User not authenticated")
        user=CustomUser.objects.get(user_id=payload['user_id'])
        serializer=UserProfileSerializer(user,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

class VerifyOTP(APIView):
    def post(self,request):
       
          data=request.data          
          serializer = VerifyAccountSerializer(data = data)
          if serializer.is_valid():
               email = serializer.data['email']
               otp = serializer.data['otp']
               try:
                   user = CustomUser.objects.get(email=email)
                   if user.otp == otp:
                    user.is_verified = True
                    user.save()
                    return Response({'message': 'Email verified successfully.'})
                   else:
                    return Response({'message': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
               except CustomUser.DoesNotExist:
                   return Response({'message': 'User not found.'})
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordView(APIView):
    def post(self,request):
        email=request.data.get('email')
        if not email:
          return Response({'error':'Email is required'},status=status.HTTP_400_BAD_REQUEST)
        try:
          user=CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error':'User with this email dose not exist'},status=status.HTTP_404_NOT_FOUND)  
        uidb64, reset_token = self.generate_reset_token(user)
        reset_token=self.generate_reset_token(user)
        token_str=f"{uidb64}-{reset_token}"
        send_password_reset_email(email,token_str)
        return Response({'message': 'Password reset email sent successfully'}, status=status.HTTP_200_OK)

    def generate_reset_token(self,user):
       uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
       token = default_token_generator.make_token(user)
       return uidb64.decode(), token

class ResetPasswordView(APIView):
    def post(self,request):
        uidb64=request.data.get('uidb64')
        reset_token=request.data.get('reset_token')
        password=request.data.get('password')
        if not uidb64 or not reset_token or not password:
          return Response({'error': 'Reset token and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try :
          uid = urlsafe_base64_decode(uidb64)
          user = CustomUser.objects.get(pk=uid)
          if default_token_generator.check_token(user, reset_token):
                user.set_password(password)
                user.save()
                return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
          else:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({'error': 'Invalid user or token'}, status=status.HTTP_400_BAD_REQUEST)

            
