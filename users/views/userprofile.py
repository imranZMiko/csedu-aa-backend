from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth import get_user_model
from users.models import Profile
from users.serializers import ProfileSerializer, UserSerializer
from rest_framework import status
from users.models import User, Profile
from users.serializers import UserSerializer, ProfileSerializer


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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
