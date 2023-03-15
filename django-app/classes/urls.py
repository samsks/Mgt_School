from django.urls import path
from classes.views import ClassView, ClassDetailView


urlpatterns = [
    path("classes/", ClassView.as_view()),
    path("classes/<int:class_id>", ClassDetailView.as_view()),
]
