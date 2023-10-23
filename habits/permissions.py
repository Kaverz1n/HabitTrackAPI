from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    '''
    Ограничение на то, что лишь создатели привычки могут
    редактировать, просматрировать (если is_public = False),
    и удалять привычку
    '''

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user == obj.user or user.is_superuser:
            return True
