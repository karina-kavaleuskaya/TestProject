from rest_framework import serializers
from user.models import AuthorizationUser, InviteCode, Referral


class InviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteCode
        fields = ('code', 'user')


class ReferralSerializer(serializers.ModelSerializer):
    invite_code = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='invite_code.code')

    class Meta:
        model = Referral
        fields = ('user', 'invite_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorizationUser
        fields = ('phone_number', 'id')


class UserProfileSerializer(serializers.ModelSerializer):
    referrals = ReferralSerializer(many=True, read_only=True)

    class Meta:
        model = AuthorizationUser
        fields = ('phone_number', 'referrals')
