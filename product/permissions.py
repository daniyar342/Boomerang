from rest_framework.permissions import BasePermission


class IsAnonymoused(BasePermission):
    """
    Allows access only to not authenticated users.
    """

    message = "permission denied, at first you must logout"

    def has_permission(self, request, view):
        return bool(request.user.is_anonymous)



class IsSellerOfProduct(BasePermission):
    """
    Allow access only user that seller of product
    """

    message = "permission denied, you are not seller of this product"

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user