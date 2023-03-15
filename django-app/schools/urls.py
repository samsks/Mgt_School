from django.urls import path
from .views import SchoolView, SchoolDetailView
from ttests.views import TestView, TestDetailView


urlpatterns = [
    # School
    path("schools/", SchoolView.as_view()),
    path("schools/<int:school_id>", SchoolDetailView.as_view()),
    # # Class_Registration
    # path("schools/<int:school_id>/class_registrations/", views.ClassRegistrationView.as_view()),
    # path("schools/<int:school_id>/class_registrations/<int:cls_register_id>", views.ClassRegistrationDetailView.as_view()),
    # # Attendance
    # path("schools/<int:school_id>/test_results/", views.TestResultView.as_view()),
    # path("schools/<int:school_id>/test_results/<int:test_result_id>", views.TestResultDetailView.as_view()),
    # # Test_Result
    # path("schools/<int:school_id>/attendance/", views.AttendanceView.as_view()),
    # path("schools/<int:school_id>/attendance/<int:attendance_id>", views.AttendanceDetailView.as_view()),
    # Test
    path("schools/<int:school_id>/courses/classes/classrooms/tests/", TestView.as_view()),
    path("schools/<int:school_id>/courses/classes/classrooms/tests/<int:test_id>", TestDetailView.as_view()),
]
