from rest_framework import serializers
from events.models import Event
from users.serializers import SmallUserCardSerializer


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    """
    managers = SmallUserCardSerializer(many=True, read_only=True)
    guests = SmallUserCardSerializer(many=True, read_only=True)
    creator = SmallUserCardSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
