from rest_framework.permissions import BasePermission

class IsAuthenticatedForManipulateResource(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        return request.user and request.user.is_authenticated