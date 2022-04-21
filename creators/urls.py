

from django.urls import path
from .views import CreatorListView, CreatorDetailView


urlpatterns = [
    path("", CreatorListView.as_view()),
    path("<int:pk>", CreatorDetailView.as_view())
]
