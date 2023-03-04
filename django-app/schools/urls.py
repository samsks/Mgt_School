from django.urls import path
from .views import SchoolView, SchoolDetailView
from teachers.views import TeacherView, TeacherDetailView


urlpatterns = [
    path("schools/", SchoolView.as_view()),
    path("schools/<int:school_id>", SchoolDetailView.as_view()),
    path("schools/<int:school_id>/teachers/", TeacherView.as_view()),
    path("schools/<int:school_id>/teachers/<int:teacher_id>", TeacherDetailView.as_view()),
]
