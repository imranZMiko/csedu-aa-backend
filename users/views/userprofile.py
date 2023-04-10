from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth import get_user_model
from users.models import Profile
from users.serializers import ProfileSerializer, UserSerializer
from rest_framework import status
from users.models import User, Profile
from users.serializers import UserSerializer, ProfileSerializer
from rest_framework.pagination import PageNumberPagination


User = get_user_model()

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            raise Http404
        return profile

class SelfProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404
        return user
    
class SelfUserDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = User.objects.all()
        batch_number = self.request.query_params.get('batch', None)
        company = self.request.query_params.get('company', None)
        country = self.request.query_params.get('city', None)
        city = self.request.query_params.get('country', None)
        hometown = self.request.query_params.get('hometown', None)

        if batch_number:
            queryset = queryset.filter(profile__batch_number=batch_number)
        if company:
            queryset = queryset.filter(profile__work_experiences__company_name=company)
        if country:
            queryset = queryset.filter(profile__present_address__country=country)
        if city:
            queryset = queryset.filter(profile__present_address__city=city)
        if hometown:
            queryset = queryset.filter(profile__hometown=hometown)

        return queryset





