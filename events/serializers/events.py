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
    is_manager = serializers.SerializerMethodField(read_only=True)
    is_subscriber = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

    def get_is_manager(self, obj):
        """
        Returns True if the request user is a manager of the event, False otherwise.
        """
        request_user = self.context['request'].user
        return request_user.is_authenticated and obj.managers.filter(pk=request_user.pk).exists()

    def get_is_subscriber(self, obj):
        """
        Returns True if the request user is a subscriber to the event, False otherwise.
        """
        request_user = self.context['request'].user
        return request_user.is_authenticated and obj.guests.filter(pk=request_user.pk).exists()
