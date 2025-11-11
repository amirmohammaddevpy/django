from rest_framework.permissions import BasePermission ,SAFE_METHODS
from django.contrib.auth.models import User
class Permission(BasePermission):
    def has_objects_permission(self,request,obj,):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ['PUT','DELETE']:
            return request.user == obj.user

class CreateAPIPermission(BasePermission):
    def has_permission(self,request,view):
        if request.user == User.is_active:
            return True