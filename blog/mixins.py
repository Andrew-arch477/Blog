from django.core.exceptions import PermissionDenied

class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise PermissionDenied("It's not yours! Dont touch it!")
        return super().dispatch(request, *args, **kwargs)

class UserIsWriterMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'writer':
            raise PermissionDenied("You must be a Writer to access this page.")
        return super().dispatch(request, *args, **kwargs)

class UserIsAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied("You must be an Admin to access this page.")
        return super().dispatch(request, *args, **kwargs)