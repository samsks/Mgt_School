from django.urls import path
from ttests.views import TestView, TestDetailView


urlpatterns = [
    path("tests/", TestView.as_view()),
    path("tests/<int:test_id>", TestDetailView.as_view()),
]
