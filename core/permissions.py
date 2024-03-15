from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminForPOST(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return False
    

class IsCoursePriceOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.course.author


class IsSectionAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.course.author
    

class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
    

class IsSectionItemOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.section.course.author