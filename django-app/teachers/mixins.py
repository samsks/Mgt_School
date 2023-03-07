from django.shortcuts import get_object_or_404
from .models import Teacher


class TeacherPermissionMixin:
    teacher_url_kwarg = None

    def check_custom_object_permission(self):
        assert self.teacher_url_kwarg is not None, (
            "'%s' should include a `teacher_url_kwarg` attribute"
            % self.__class__.__name__
        )

        teacher_id = self.kwargs[self.teacher_url_kwarg]
        teacher_obj = get_object_or_404(Teacher, pk=teacher_id)

        self.check_object_permissions(self.request, teacher_obj)

    def get(self, request, *args, **kwargs):
        self.check_custom_object_permission()

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_custom_object_permission()
        return self.create(request, *args, **kwargs)
