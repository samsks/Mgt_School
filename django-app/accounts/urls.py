from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Endpoints for Owner User Account
    path("<int:school_id>/accounts/", views.AccountOwnerListView.as_view()),
    path("accounts/", views.AccountOwnerCreateView.as_view()),
    # path("accounts/<int:account_id>", views.AccountDetailView.as_view()), verificar
    # Endpoints for Teacher User Account
    path("teachers/", views.AccountTeacherView.as_view()),
    # Endpoints for Students User Account
    path("students/", views.AccountStudentView.as_view()),
    # path("new_students/", views.AccountStudentCreateView.as_view()),
    # Endpoints for Authentication Accounts
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
