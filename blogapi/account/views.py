from django.contrib.auth import user_logged_in
from django.template.context_processors import request
from rest_framework.permissions  import AllowAny,IsAuthenticated
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import RegisterSerializers ,LoginSerializer ,ProfileSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

# Create your views here.

class ProfileUser(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user

class RegisterView(APIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers


class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self,request):
        try:
            refresh = request.data['refresh']
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(status=205)
        except Exception as e:
            return Response(status=400)
        

class LoginView(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)