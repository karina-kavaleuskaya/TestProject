from django.urls import path
from user.views import UserRegistrationView, CodeCheckView, UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('code-check/', CodeCheckView.as_view(), name='code-check/'),
    path('user-profile', UserProfileView.as_view(), name='user-profile')
]