from rest_framework import generics, permissions, status
from rest_framework.response import Response
from events.models import Event
from users.models import User
from rest_framework.exceptions import NotFound, PermissionDenied

class EventManagersAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_event(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise NotFound('Event not found.')

    def check_user_permission(self, event, user):
        if not event.managers.filter(pk=user.pk).exists():
            raise PermissionDenied('You do not have permission to manage this event.')

    def post(self, request, pk):
        event = self.get_event(pk)
        self.check_user_permission(event, request.user)

        usernames = request.data.get('usernames')

        if not isinstance(usernames, list):
            return Response({'detail': 'Usernames must be provided as a list.'}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(username__in=usernames)

        if len(users) != len(usernames):
            non_existing_usernames = set(usernames) - set(users.values_list('username', flat=True))
            return Response({'detail': f'Users {non_existing_usernames} do not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        event.managers.add(*users)
        return Response({'detail': 'Managers added successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        event = self.get_event(pk)
        self.check_user_permission(event, request.user)

        username = request.data.get('username')

        if not username:
            return Response({'detail': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_to_remove = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        if user_to_remove == request.user:
            return Response({'detail': 'You cannot remove yourself from managers.'}, status=status.HTTP_400_BAD_REQUEST)

        if user_to_remove == event.creator:
            return Response({'detail': 'You cannot remove the creator from managers.'}, status=status.HTTP_400_BAD_REQUEST)

        if not event.managers.filter(pk=user_to_remove.pk).exists():
            return Response({'detail': 'User is not a manager of this event.'}, status=status.HTTP_400_BAD_REQUEST)

        event.managers.remove(user_to_remove)
        return Response({'detail': 'Manager removed successfully.'}, status=status.HTTP_200_OK)

