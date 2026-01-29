from rest_framework.permissions import BasePermission

from .models import UserProfile


class HasUserProfile(BasePermission):
    message = "El usuario no tiene un perfil asociado."

    def has_permission(self, request, view):
        return hasattr(request.user, "profile")


class IsAdminOrManager(BasePermission):
    message = "Permisos insuficientes para esta acción."

    def has_permission(self, request, view):
        if not hasattr(request.user, "profile"):
            return False
        return request.user.profile.role in {
            UserProfile.ROLE_ADMIN,
            UserProfile.ROLE_MANAGER,
        }


class IsAdmin(BasePermission):
    message = "Permisos insuficientes para esta acción."

    def has_permission(self, request, view):
        if not hasattr(request.user, "profile"):
            return False
        return request.user.profile.role == UserProfile.ROLE_ADMIN


class IsManager(BasePermission):
    message = "Permisos insuficientes para esta acción."

    def has_permission(self, request, view):
        if not hasattr(request.user, "profile"):
            return False
        return request.user.profile.role == UserProfile.ROLE_MANAGER


class IsSeller(BasePermission):
    message = "Permisos insuficientes para esta acción."

    def has_permission(self, request, view):
        if not hasattr(request.user, "profile"):
            return False
        return request.user.profile.role == UserProfile.ROLE_SELLER


class IsAdminManagerOrSeller(BasePermission):
    message = "Permisos insuficientes para esta acción."

    def has_permission(self, request, view):
        if not hasattr(request.user, "profile"):
            return False
        return request.user.profile.role in {
            UserProfile.ROLE_ADMIN,
            UserProfile.ROLE_MANAGER,
            UserProfile.ROLE_SELLER,
        }


class IsSameFranchise(BasePermission):
    message = "No puedes acceder a recursos de otra franquicia."

    def has_object_permission(self, request, view, obj):
        if not hasattr(request.user, "profile"):
            return False
        return getattr(obj, "franchise_id", None) == request.user.profile.franchise_id
