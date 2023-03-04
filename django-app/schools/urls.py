from django.urls import path
from .views import SchoolView, SchoolDetailView

urlpatterns = [
    path("schools/", SchoolView.as_view()),
    path("schools/<int:school_id>", SchoolDetailView.as_view()),
]
