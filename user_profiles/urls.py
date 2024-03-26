from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("refresh-token/", TokenRefreshView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        "send-code-to-email/",
        ForgetPasswordSendCodeView.as_view(),
        name="send_password_reset_code",
    ),
    path(
        "verify-register-code/",
        UserVerifyRegisterCode.as_view(),
        name="verify_register_code",
    ),
    path("forget-password/reset/", ForgetPasswordView.as_view(), name="reset_password"),
    path(
        "reset-password-profile/",
        UserResetPasswordView.as_view(),
        name="reset_password",
    ),
    path("profiles/", ListProfileApi.as_view(), name=""),
    path("profile/<int:id>/", DetailUserProfileApi.as_view(), name=""),
    path("profile/update/<int:id>/", UpdateUserProfileApi.as_view(), name=""),
]
