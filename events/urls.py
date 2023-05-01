from django.urls import path
from events import views

urlpatterns = [
    # Endpoint for listing all events and creating new events
    path('', views.ListCreateEventAPI.as_view(), name='list_create_event_api'),
    # API endpoint to add managers to an event or remove a manager from an event
    path('<int:pk>/managers/', views.EventManagersAPI.as_view(), name='add_or_remove_event_managers'),
]

