from django.urls import path
from classrooms.views import ClassroomView, ClassroomDetailView


urlpatterns = [
    path("classrooms/", ClassroomView.as_view()),
    path("classrooms/<int:classroom_id>", ClassroomDetailView.as_view()),
]
