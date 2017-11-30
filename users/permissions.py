from rest_framework import permissions
from django.urls import reverse
from users.models import UserProfile

class IsInClassroom(permissions.BasePermission):
    def has_permission(self, request, view):
        classroom_id = request.resolver_match.kwargs.get('classroom_id')
        if not classroom_id:
            raise Exception('IsInClassroom permission must be used with a url that contains "classroom_id"')
        return int(classroom_id) in UserProfile.objects.get(
            user=request.user
        ).get_user_object().classrooms.values_list('id', flat=True)


class CanViewUser(permissions.BasePermission):
    def has_permission(self, request, view):
        exception_urls = [reverse('me')]
        if request.META.get('PATH_INFO') in exception_urls:
            return True
        user_id = request.resolver_match.kwargs.get('user_id')
        if not user_id:
            raise Exception('CanViewUser permission must be used with a url that contains "user_id"')
        classrooms = set(UserProfile.objects.get(
            id=user_id
        ).get_user_object(
            model=True
        ).objects.filter(
            id=user_id
        ).values_list(
            'classrooms__id',
            flat=True
        ))
        request_user_classrooms = set(UserProfile.objects.get(
            user_id=request.user.id
        ).get_user_object().classrooms.values_list(
            'id',
            flat=True
        ))

        return len(classrooms.intersection(request_user_classrooms)) >= 1 or int(user_id) == request.user.id
