from rest_framework import permissions


class IsAllowedToTrackOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, order_obj):
        if request.user.is_superuser or request.user.role == 2:
            return True

        if order_obj.store.owner.id == request.user.id:
            return True

        if request.user.id == order_obj.user.id:
            return True

        return False
    

class IsAllowedToChangeOrderStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 2:
            return True
        
        return False

