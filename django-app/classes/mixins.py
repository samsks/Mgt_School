from django.shortcuts import get_object_or_404
from .models import Class


class ClassPermissionMixin:
    class_url_kwarg = None

    def check_custom_object_permission(self):
        assert self.class_url_kwarg is not None, (
            "'%s' should include a `class_url_kwarg` attribute"
            % self.__class__.__name__
        )

        class_id = self.kwargs[self.class_url_kwarg]
        class_obj = get_object_or_404(Class, pk=class_id)

        self.check_object_permissions(self.request, class_obj)

    def get(self, request, *args, **kwargs):
        self.check_custom_object_permission()

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_custom_object_permission()
        return self.create(request, *args, **kwargs)
