from rest_framework import serializers
from events.models import EventAnnouncement
from users.serializers import SmallUserCardSerializer

class EventAnnouncementSerializer(serializers.ModelSerializer):
    posted_by = SmallUserCardSerializer()

    class Meta:
        model = EventAnnouncement
        fields = ['id', 'text', 'picture', 'event', 'posted_by']
