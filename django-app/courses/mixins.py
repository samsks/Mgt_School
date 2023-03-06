from django.shortcuts import get_object_or_404
from .models import Course


class CoursePermissionMixin:
    course_url_kwarg = None

    def check_custom_object_permission(self):
        assert self.course_url_kwarg is not None, (
            "'%s' should include a `course_url_kwarg` attribute"
            % self.__class__.__name__
        )

        course_id = self.kwargs[self.course_url_kwarg]
        course_obj = get_object_or_404(Course, pk=course_id)

        self.check_object_permissions(self.request, course_obj)

    def get(self, request, *args, **kwargs):
        self.check_custom_object_permission()

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_custom_object_permission()
        return self.create(request, *args, **kwargs)
