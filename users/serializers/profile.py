from rest_framework import serializers
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'profile_picture', 'date_of_birth', 'sex', 'batch_number', 'hometown']
        read_only_fields = ['id']
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise serializers.ValidationError('Cannot update profile of another user')
        return super().update(instance, validated_data)
