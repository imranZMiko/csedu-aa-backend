from django.urls import path
from events import views

urlpatterns = [
    # Endpoint for listing all events and creating new events
    path('', views.ListCreateEventAPI.as_view(), name='list_create_event_api'),
]
