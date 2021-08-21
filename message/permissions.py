from rest_framework import permissions


class IsOwnerOrReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(obj.sender == request.user or request.user == obj.receiver)
        print(request.user)
        return obj.sender == request.user or request.user == obj.receiver
