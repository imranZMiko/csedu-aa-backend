from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.core.exceptions import PermissionDenied
from mailing.models import SystemMail, UserMail
from mailing.serializers import SystemMailSerializer, UserMailSerializer

class SystemMailList(ListAPIView):
    queryset = SystemMail.objects.all()
    serializer_class = SystemMailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class SystemMailDetail(RetrieveAPIView):
    queryset = SystemMail.objects.all()
    serializer_class = SystemMailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserMailList(ListAPIView):
    queryset = UserMail.objects.all()
    serializer_class = UserMailSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class UserMailDetail(RetrieveAPIView):
    queryset = UserMail.objects.all()
    serializer_class = UserMailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        obj = super().get_object()
        if not obj.sender == self.request.user:
            raise PermissionDenied('You are not authorized to access this mail.')
        return obj
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class UserSentMailList(ListAPIView):
    serializer_class = UserMailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserMail.objects.filter(sender=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
