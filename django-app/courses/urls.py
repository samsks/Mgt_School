from django.urls import path
from courses.views import CourseView, CourseDetailView


urlpatterns = [
    path("courses/", CourseView.as_view()),
    path("courses/<int:course_id>", CourseDetailView.as_view()),
]
