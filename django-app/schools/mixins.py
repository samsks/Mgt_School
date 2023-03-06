from django.shortcuts import get_object_or_404
from .models import School


class SchoolPermissionMixin:
    school_url_kwarg = None

    def check_custom_object_permission(self):
        assert self.school_url_kwarg is not None, (
            "'%s' should include a `school_url_kwarg` attribute"
            % self.__class__.__name__
        )

        school_id = self.kwargs[self.school_url_kwarg]
        school_obj = get_object_or_404(School, pk=school_id)

        self.check_object_permissions(self.request, school_obj)

    def get(self, request, *args, **kwargs):
        self.check_custom_object_permission()

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_custom_object_permission()
        return self.create(request, *args, **kwargs)
