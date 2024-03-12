from django.urls import path
from .views import *

urlpatterns = [
    path('users/signup/', signup),
    path('users/login/', user_login),
    path('users/forgot_password/', ForgotPasswordAPIView.as_view()),
    path('users/reset_password/', ResetPassword.as_view()),
    path('users/change_password/', ChangePassword.as_view()),
    path('users/me/', CurrentUserProfile.as_view()),
]