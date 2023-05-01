from django.urls import path
from events import views

urlpatterns = [
    # Endpoint for listing all events and creating new events
    path('', views.ListCreateEventAPI.as_view(), name='list_create_event_api'),
    # The `pk` parameter in the URL is the primary key of the event to retrieve/update/delete
    path('<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
    # API endpoint to add managers to an event or remove a manager from an event
    path('<int:pk>/managers/', views.EventManagersAPI.as_view(), name='add_or_remove_event_managers'),
    # URL pattern for subscribing or unsubscribing a user to an event
    path('<int:event_id>/subscribe/', views.EventSubscriptionView.as_view(), name='event-subscription'),
]

