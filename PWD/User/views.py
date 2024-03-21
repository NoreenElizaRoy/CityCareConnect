from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OfficialSerializer,CustomUserSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import Official,CustomUser
import jwt,datetime

#user reg
class RegisterView(APIView):
    def post(self,request):
        serializer=CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
#both user and staff    
class LoginView(APIView):
        def post(self,request):
          email= request.data['email']
          password= request.data['password']            
            
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
               response= Response()
               response.set_cookie(
                key="jwt",
                value=token,
                httponly=False,
                samesite="None",
                secure=True,
                path="/" )
               response.data={ "jwt":token, "user": payload }
               return response
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
               return response
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
                     