from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from users.models import Referral

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    referral = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email_address', 'password', 'referral', 'referred_by']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'validators': []},
        }

    def create(self, validated_data):
        referral = validated_data.pop('referred_by', None)
        if referral:
            raise serializers.ValidationError('Cannot contain referred_by field')
        referral_code = validated_data.pop('referral')
        try:
            referral = Referral.objects.get(referral_code = referral_code)
            referral_user = referral.referrer
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Invalid referral')
        user = User(**validated_data, referred_by=referral_user)
        user.set_password(validated_data['password'])
        user.save()
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
