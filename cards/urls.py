from django.urls import path
from .views import CardListCreateView, CardRetrieveUpdateDeleteView


urlpatterns = [
    path('cards/', CardListCreateView.as_view(), name='card-list-create'),
    path('cards/<int:pk>/', CardRetrieveUpdateDeleteView.as_view(), name='card-retrieve-update-delete'),
]
