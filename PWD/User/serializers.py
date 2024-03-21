from rest_framework import serializers
from .models import Official,CustomUser



class OfficialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Official
        fields = ['id','username','email','password',]
        extra_kwargs ={
            'password': {'write_only':True}   #pswd only for database
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)  # Ensure password is set correctly
        instance.save()
        return instance
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs ={
            'password': {'write_only':True}   #pswd only for database
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)  # Ensure password is set correctly
        instance.save()
        return instance