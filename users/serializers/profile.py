from rest_framework import serializers
from users.models import Profile, WorkExperience, Skill, SocialMediaLink, AcademicHistory, PresentAddress

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

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ('id', 'profile', 'platform_name', 'link')
        read_only_fields = ('id', 'profile')

    def validate(self, data):
        if self.instance and self.instance.profile.user != self.context['request'].user:
            raise serializers.ValidationError('You can only update your own social media links.')
        return data

class PresentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentAddress
        fields = ('id', 'city', 'country', 'profile')
        read_only_fields = ('id', 'profile')

    def validate(self, data):
        if self.instance and self.instance.profile.user != self.context['request'].user:
            raise serializers.ValidationError('You can only update your own present address.')
        return data

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'proficiency', 'description', 'profile')
        read_only_fields = ('id', 'profile')

    def validate(self, data):
        if self.instance and self.instance.profile.user != self.context['request'].user:
            raise serializers.ValidationError('You can only update your own skills.')
        return data

class AcademicHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicHistory
        fields = ('id', 'profile', 'institution_name', 'concentration', 'start_date', 'graduation_date', 'is_currently_studying', 'result')
        read_only_fields = ('id', 'profile')

    def validate(self, data):
        if self.instance and self.instance.profile.user != self.context['request'].user:
            raise serializers.ValidationError('You can only update your own academic histories.')
        return data

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ('id', 'profile', 'company_name', 'branch', 'position', 'starting_date', 'ending_date', 'currently_working', 'description')
        read_only_fields = ('id', 'profile')

    def validate(self, data):
        if self.instance and self.instance.profile.user != self.context['request'].user:
            raise serializers.ValidationError('You can only update your own work experiences.')
        return data