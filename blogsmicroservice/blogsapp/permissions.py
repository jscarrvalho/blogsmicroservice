from rest_framework.permissions import BasePermission

class IsAuthenticatedForManipulateResource(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        return request.user and request.user.is_authenticated

class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.author == request.user