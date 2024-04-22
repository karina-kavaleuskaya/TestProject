from django.db import models


class AuthorizationUser(models.Model):
    phone_number = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InviteCode(models.Model):
    code = models.CharField(max_length=6, unique=True, null=True)
    user = models.ForeignKey(AuthorizationUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Referral (models.Model):
    invite_code = models.ForeignKey(InviteCode, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(AuthorizationUser, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)





