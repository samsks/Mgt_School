from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Endpoints for Owner User Account
    path("accounts/schools/<int:school_id>/", views.AccountOwnerListView.as_view()),
    path("accounts/", views.AccountOwnerCreateView.as_view()),
    path("accounts/<int:account_id>", views.AccountDetailView.as_view()),
    # Endpoints for Teacher User Account
    path("teachers/", views.AccountTeacherView.as_view()),
    path("teachers/<int:account_id>", views.AccountTeacherDetailView.as_view()),
    # Endpoints for Students User Account
    path("students/", views.AccountStudentView.as_view()),
    path("students/<int:account_id>", views.AccountStudentDetailView.as_view()),
    # Endpoints for Authentication Accounts
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    # Class_Registration
    path("class_registrations/students/<int:student_id>", views.ClassRegistrationListView.as_view()),
    path("class_registrations/", views.ClassRegistrationCreateView.as_view()),
    path("class_registrations/<int:class_register_id>", views.ClassRegistrationDetailView.as_view()),
    # Test_Result
    path("test_results/students/<int:student_id>", views.TestResultListView.as_view()),
    path("test_results/", views.TestResultCreateView.as_view()),
    path("test_results/<int:test_result_id>", views.TestResultDetailView.as_view()),
    # Attendance
    path("attendance/students/<int:student_id>", views.AttendanceListView.as_view()),
    path("attendance/", views.AttendanceCreateView.as_view()),
    path("attendance/<int:attendance_id>", views.AttendanceDetailView.as_view()),
]
