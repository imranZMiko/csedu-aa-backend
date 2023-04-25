from rest_framework import serializers
from blogs.models import Tag

class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'slug')
        read_only_fields = ('name', 'slug')
