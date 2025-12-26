from rest_framework.permissions import BasePermission

class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.user != request.user.is_authenticated

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user.id