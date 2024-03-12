from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OfficialSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import Official
import jwt,datetime

class RegisterView(APIView):
    def post(self,request):
        serializer=OfficialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
        def post(self,request):
            email= request.data['email']
            password= request.data['password']            
            user=Official.objects.filter(email=email).first()

            if user is None:
                 raise AuthenticationFailed("User not found")
            
            if not user.check_password(password):
                 raise AuthenticationFailed("Incorrect password")
            
            payload = {
                 "id": user.id,
                 "email" : user.email,
                 "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                 "iat" : datetime.datetime.utcnow(),
            }
            token = jwt.encode(payload, "secert",algorithm="HS256")

            response= Response()
            response.set_cookie(
                key="jwt",
                value=token,
                httponly=False,
                samesite="None",
                secure=True,
                path="/"
            )
            response.data={ "jwt":token, "user": payload }
            return response