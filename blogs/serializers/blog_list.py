from rest_framework import serializers
from bs4 import BeautifulSoup
from blogs.models import Blog

class BlogListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    content_head = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ('id', 'user', 'title', 'content_head', 'created_at', 'updated_at')

    def get_user(self, obj):
        # Return a serialized representation of the user (username, first_name, last_name)
        user = obj.user
        return {
            'username': user.username,
            'first_name': user.profile.first_name,
            'last_name': user.profile.last_name
        }

    def get_content_head(self, obj):
        # Extract text from HTML content and generate a summary
        content = obj.content
        soup = BeautifulSoup(content, 'html.parser')  # Parse HTML content
        text = soup.get_text()  # Extract text from HTML
        words = text.split()  # Split the text by space
        summary = ' '.join(words[:10])  # Extract the first 10 words as the summary
        return summary
