from django.urls import path
from .views import AccountView, AccountDetailView
from rest_framework_simplejwt import views

urlpatterns = [
    path("accounts/", AccountView.as_view()),
    path("accounts/<int:account_id>", AccountDetailView.as_view()),
    path("login/", views.TokenObtainPairView.as_view()),
    path("refresh/", views.TokenRefreshView.as_view()),
]
