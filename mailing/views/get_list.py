from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.core.exceptions import PermissionDenied, ValidationError
from mailing.models import SystemMail, UserMail
from mailing.serializers import SystemMailSerializer, UserMailSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class SystemMailList(ListAPIView):
    serializer_class = SystemMailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = SystemMail.objects.all()

        page_size = self.request.query_params.get('page_size', None)
        
        if page_size :
            self.pagination_class = PageNumberPagination
            self.pagination_class.page_size = int(page_size)
        else:
            self.pagination_class = None

        return queryset

class SystemMailDetail(RetrieveAPIView):
    queryset = SystemMail.objects.all()
    serializer_class = SystemMailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserMailList(ListAPIView):
    serializer_class = UserMailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        queryset = UserMail.objects.all()

        page_size = self.request.query_params.get('page_size', None)
        
        if page_size :
            self.pagination_class = PageNumberPagination
            self.pagination_class.page_size = int(page_size)
        else:
            self.pagination_class = None

        return queryset

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
        queryset = UserMail.objects.filter(sender=self.request.user)

        page_size = self.request.query_params.get('page_size', None)
        
        if page_size :
            self.pagination_class = PageNumberPagination
            self.pagination_class.page_size = int(page_size)
        else:
            self.pagination_class = None

        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
