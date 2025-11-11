from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from .serializers import SerializerView
from .models import Blog
from .permissions import Permission ,CreateAPIPermission
# Create your views here.

class ListView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = SerializerView

class DetailView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = SerializerView
    permission_classes = [Permission]

class CreateAPI(CreateAPIView):
    queryset=Blog.objects.all()
    serializer_class = SerializerView
    permission_classess = [CreateAPIPermission]