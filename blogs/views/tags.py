from rest_framework import generics, permissions
from blogs.models import Tag
from blogs.serializers import TagListSerializer

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication to access the view
    ordering = ['-blogs_count']  # Order by blogs_count descending
