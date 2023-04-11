from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from users.models import Referral, Profile, WorkExperience

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    batch_number = serializers.CharField(required=True, write_only=True)
    sex = serializers.ChoiceField(choices=Profile.SEX_CHOICES, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email_address', 'password', 'referral_code', 'referred_by', 'first_name', 'last_name', 'batch_number', 'sex']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'validators': []},
        }

    def create(self, validated_data):
        referral = validated_data.pop('referred_by', None)
        email_address = validated_data.pop('email_address', None)
        if referral:
            raise serializers.ValidationError('Cannot contain referred_by field')
        referral_code = validated_data.pop('referral_code')
        try:
            referral = Referral.objects.get(referral_code = referral_code)
            referral_user = referral.referrer
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Invalid referral')
        if email_address != referral.referred_email:
            raise serializers.ValidationError('The referral should be used with the same email it was created for.')
        
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        batch_number = validated_data.pop('batch_number', None)
        sex = validated_data.pop('sex', None)

        user = User(**validated_data, referred_by=referral_user, email_address = email_address)
        user.set_password(validated_data['password'])
        user.save()
        # Create a profile instance for the newly created user

        Profile.objects.create(user=user, first_name=first_name, last_name=last_name, batch_number=batch_number, sex=sex)
        return user

    def update(self, instance, validated_data):
        referral = validated_data.pop('referred_by', None)
        if referral:
            raise serializers.ValidationError('Cannot update referred_by field')
        user = self.context['request'].user
        if instance != user:
            raise serializers.ValidationError('Cannot update user of another user')
        instance.username = validated_data.get('username', instance.username)
        instance.email_address = validated_data.get('email_address', instance.email_address)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class UserCardSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')
    batch_number = serializers.IntegerField(source='profile.batch_number')
    country = serializers.CharField(source='profile.present_address.country')
    city = serializers.CharField(source='profile.present_address.city')
    current_company = serializers.SerializerMethodField()
    sex = serializers.CharField(source='profile.sex')
    profile_picture = serializers.URLField(source='profile.profile_picture', allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email_address', 'first_name', 'last_name', 'batch_number', 'country', 'city', 'current_company', 'sex', 'profile_picture']

    def get_current_company(self, obj):
        current_work_experience = WorkExperience.objects.filter(profile__user=obj, currently_working=True).first()
        if current_work_experience:
            return current_work_experience.company_name
        else:
            return None

