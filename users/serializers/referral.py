from rest_framework import serializers
from users.models import Referral

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['referrer', 'referral_code', 'created_at']
        read_only_fields = ['referrer', 'referral_code', 'created_at']
