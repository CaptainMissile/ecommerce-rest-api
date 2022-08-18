from rest_framework import permissions

from apps.accounts.models import User

class IsVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        email = request.data['email']
        try:
            user = User.objects.get(email = email)

            return user.is_verified
        except:
            pass

        return False