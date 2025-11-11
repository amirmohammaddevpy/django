from django.contrib.auth import authenticate , login
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True,)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':"Password fields didn't match."})
        raise attrs
    
    def create(self,validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password2'])
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self,attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username,password=password)

        if not user:
            return serializers.ValidationError({'error':'Invalid credentials'})
        
        token = RefreshToken.for_user(user)

        return {
            "username":user.username,
            "access":str(token.access_token),
            "refresh":str(token),
            }
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']