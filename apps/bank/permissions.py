from rest_framework import permissions


class IsBankManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 1:
            return True
        
        return False


class IsBankAccountOwnerOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, acc_obj):
        if request.user.is_superuser or request.user.role == 1:
            return True

        if acc_obj.account_no == request.user.profile.bank_account:
            return True

        return False