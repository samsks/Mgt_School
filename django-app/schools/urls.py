from django.urls import path
from .views import SchoolView, SchoolDetailView
from teachers.views import TeacherView, TeacherDetailView
from students import views
from courses.views import CourseView, CourseDetailView
from classes.views import ClassView, ClassDetailView
from classrooms.views import ClassroomView, ClassroomDetailView
from ttests.views import TestView, TestDetailView


urlpatterns = [
    # School
    path("schools/", SchoolView.as_view()),
    path("schools/<int:school_id>", SchoolDetailView.as_view()),
    # Teacher
    path("schools/<int:school_id>/teachers/", TeacherView.as_view()),
    path("schools/<int:school_id>/teachers/<int:teacher_id>", TeacherDetailView.as_view()),
    # Student
    path("schools/<int:school_id>/students/", views.StudentView.as_view()),
    path("schools/<int:school_id>/students/<int:student_id>", views.StudentDetailView.as_view()),
    # Class_Registration
    path("schools/<int:school_id>/class_registrations/", views.ClassRegistrationView.as_view()),
    path("schools/<int:school_id>/class_registrations/<int:cls_register_id>", views.ClassRegistrationDetailView.as_view()),
    # Attendance
    path("schools/<int:school_id>/test_results/", views.TestResultView.as_view()),
    path("schools/<int:school_id>/test_results/<int:test_result_id>", views.TestResultDetailView.as_view()),
    # Test_Result
    path("schools/<int:school_id>/attendance/", views.AttendanceView.as_view()),
    path("schools/<int:school_id>/attendance/<int:attendance_id>", views.AttendanceDetailView.as_view()),
    # Course
    path("schools/<int:school_id>/courses/", CourseView.as_view()),
    path("schools/<int:school_id>/courses/<int:course_id>", CourseDetailView.as_view()),
    # Class
    path("schools/<int:school_id>/courses/classes/", ClassView.as_view()),
    path("schools/<int:school_id>/courses/classes/<int:class_id>", ClassDetailView.as_view()),
    # Classroom
    path("schools/<int:school_id>/courses/classes/classrooms/", ClassroomView.as_view()),
    path("schools/<int:school_id>/courses/classes/classrooms/<int:classroom_id>", ClassroomDetailView.as_view()),
    # Test
    path("schools/<int:school_id>/courses/classes/classrooms/tests/", TestView.as_view()),
    path("schools/<int:school_id>/courses/classes/classrooms/tests/<int:test_id>", TestDetailView.as_view()),
]
