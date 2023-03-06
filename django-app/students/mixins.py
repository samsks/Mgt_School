from django.shortcuts import get_object_or_404
from .models import Student


class StudentPermissionMixin:
    student_url_kwarg = None

    def check_custom_object_permission(self):
        assert self.student_url_kwarg is not None, (
            "'%s' should include a `student_url_kwarg` attribute"
            % self.__class__.__name__
        )

        student_id = self.kwargs[self.student_url_kwarg]
        student_obj = get_object_or_404(Student, pk=student_id)

        self.check_object_permissions(self.request, student_obj)

    def get(self, request, *args, **kwargs):
        self.check_custom_object_permission()

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_custom_object_permission()
        return self.create(request, *args, **kwargs)
