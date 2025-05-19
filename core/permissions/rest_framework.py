from rest_framework import permissions



class IsOwnerOrReadOnly(permissions.BasePermission):  # drf
    # Only Users can edit or delete their posts
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the User of a post
        return obj.created_by == request.user
