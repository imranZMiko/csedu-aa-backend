from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from events.models import Event
from events.serializers import EventSerializer
from events.managers import EventManager


class ListCreateEventAPI(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return (permissions.IsAuthenticated(),)
        elif self.request.method == 'POST':
            if not self.request.user.is_authenticated:
                raise PermissionDenied('Authentication credentials were not provided.')
            elif not self.request.user.is_admin:
                raise PermissionDenied('Only admin users can create events.')
            return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        creator = self.request.user if self.request.user.is_admin else None
        event = EventManager().create(creator=creator, **serializer.validated_data)
        serializer.instance = event
