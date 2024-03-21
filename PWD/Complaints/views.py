from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied,NotFound
from .serializers import ComplaintSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Complaint
from User.models import CustomUser,Official
import jwt
from django.shortcuts import get_object_or_404


class ComplaintView(APIView):    
    #create complaint
    def post(self,request):
        jwt_token = request.COOKIES.get('jwt')
        if not jwt_token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(jwt_token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthneticated!!")
        
        user=CustomUser.objects.get(user_id=payload['user_id'])
        user_name=user.user_name
        user_mobile=user.phone_number

        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user,name=user_name,phone_number=user_mobile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #view complaints
    def get(self,request):
        jwt_token = request.COOKIES.get('jwt')
        if not jwt_token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(jwt_token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthneticated!!")
        
        user=CustomUser.objects.get(user_id=payload['user_id'])
        complaints=Complaint.objects.filter(user=user)
        serializer=ComplaintSerializer(complaints,many=True)
        return Response(serializer.data)
        
class ComplaintEdit(APIView):
    #updation by officials
    def put(self,request,complaint_id):
        jwt_token = request.COOKIES.get('jwt')
        if not jwt_token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(jwt_token, 'secret', algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthneticated!!")

        #check if user is staff
        official = get_object_or_404(Official, id=user_id)
        if not official:
            raise PermissionDenied("Don't have access !!")

        complaints = get_object_or_404(Complaint, pk=complaint_id)        
        serializer=ComplaintSerializer(complaints,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #delete 
    def delete(self,request,complaint_id):
        jwt_token = request.COOKIES.get('jwt')
        if not jwt_token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(jwt_token, 'secret', algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthneticated!!")
        
        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found!")
        
        complaint = get_object_or_404(Complaint, pk=complaint_id)
        complaint.delete()
        return Response({"message":"Complaint deleted sucessfully"},status=status.HTTP_204_NO_CONTENT)
        
        