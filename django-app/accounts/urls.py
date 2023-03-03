from django.urls import path
from .views import AccountView, AccountDetailView

urlpatterns = [
    path("accounts/", AccountView.as_view()),
    path("accounts/<int:account_id>", AccountDetailView.as_view()),
]
