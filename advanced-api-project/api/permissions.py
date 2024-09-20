from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.permissions import SAFE_METHODS  # Import SAFE_METHODS directly

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow access if user owns the book or request is read-only
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user