from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import SAFE_METHODS, BasePermission



class IsAdmin(BasePermission):
    message = "You must be the Admin of this web site"
    def has_permission(self, request, view):
        if not isinstance(request.user, AnonymousUser):
            return request.user.role == "admin"