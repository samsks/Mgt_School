from django.urls import path
from occurrences.views import OccurrenceView, OccurrenceDetailView


urlpatterns = [
    path("occurrences/", OccurrenceView.as_view()),
    path("occurrences/<int:occurrence_id>", OccurrenceDetailView.as_view()),
]
