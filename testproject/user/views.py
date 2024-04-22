import random
import re
import time
import string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import UserSerializer, ReferralSerializer, UserProfileSerializer, InviteCodeSerializer
from user.models import AuthorizationUser, InviteCode, Referral


class UserRegistrationView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')

        # Validate the phone number format
        if not re.match(r'^\+7\d{10}$', phone_number):
            return Response({'error': 'Invalid phone number format'}, status=status.HTTP_400_BAD_REQUEST)

        authorization_code = random.randint(1000, 9999)
        request.session['temp_password'] = authorization_code
        characters = string.ascii_letters + string.digits
        invite_code_str = ''.join(random.choice(characters) for _ in range(6))

        try:
            user = AuthorizationUser.objects.get(phone_number=phone_number)
            return Response({'authorization_code': authorization_code}, status=status.HTTP_200_OK)
        except AuthorizationUser.DoesNotExist:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                user = AuthorizationUser.objects.get(phone_number=phone_number)
                invite_code = InviteCode.objects.create(code=invite_code_str, user=user)
                return Response({'authorization_code': authorization_code, 'invite_code': invite_code_str},
                                status=status.HTTP_201_CREATED)

            time.sleep(2)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeCheckView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        user_code = request.data.get('user_code')
        temp_password = request.session.get('temp_password')

        if temp_password and user_code == temp_password:
            return Response({'message': 'Welcome'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Incorrect code'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request):
        phone_number = request.data.get('phone_number')

        try:
            user = AuthorizationUser.objects.get(phone_number=phone_number)
        except AuthorizationUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        activated_codes = InviteCode.objects.filter(user=user)
        referred_users = [referral.user for referral in Referral.objects.filter(invite_code__in=activated_codes)]

        serializer = UserProfileSerializer(user)
        referred_users_serializer = UserSerializer(referred_users, many=True)

        return Response({'user': serializer.data, 'referred_users': referred_users_serializer.data})

    def put(self, request):
        phone_number = request.data.get('phone_number')
        invite_code_str = request.data.get('invite_code')

        try:
            user = AuthorizationUser.objects.get(phone_number=phone_number)
        except AuthorizationUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            invite_code = InviteCode.objects.get(code=invite_code_str)
        except InviteCode.DoesNotExist:
            return Response({'error': 'Invalid invite code'}, status=status.HTTP_400_BAD_REQUEST)

        if user.referral_set.filter(invite_code=invite_code).exists():
            return Response({'error': 'Invite code already used by the user'}, status=status.HTTP_400_BAD_REQUEST)

        referral = Referral.objects.create(user=user, invite_code=invite_code)
        user.referral_set.add(referral)
        serializer = UserProfileSerializer(user)
        return Response(status=status.HTTP_200_OK)

