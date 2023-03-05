from django.urls import path
from .views import SchoolView, SchoolDetailView
from teachers.views import TeacherView, TeacherDetailView
from students.views import StudentView, StudentDetailView
from courses.views import CourseView, CourseDetailView
from classes.views import ClassView, ClassDetailView
from classrooms.views import ClassroomView, ClassroomDetailView


urlpatterns = [
    path("schools/", SchoolView.as_view()),
    path("schools/<int:school_id>", SchoolDetailView.as_view()),
    path("schools/<int:school_id>/teachers/", TeacherView.as_view()),
    path("schools/<int:school_id>/teachers/<int:teacher_id>", TeacherDetailView.as_view()),
    path("schools/<int:school_id>/students/", StudentView.as_view()),
    path("schools/<int:school_id>/students/<int:student_id>", StudentDetailView.as_view()),
    path("schools/<int:school_id>/courses/", CourseView.as_view()),
    path("schools/<int:school_id>/courses/<int:course_id>", CourseDetailView.as_view()),
    path("schools/<int:school_id>/courses/classes/", ClassView.as_view()),
    path("schools/<int:school_id>/courses/classes/<int:class_id>", ClassDetailView.as_view()),
    path("schools/<int:school_id>/courses/classes/classrooms/", ClassroomView.as_view()),
    path("schools/<int:school_id>/courses/classes/<int:class_id>/classrooms/<int:classroom_id>", ClassroomDetailView.as_view()),
]
