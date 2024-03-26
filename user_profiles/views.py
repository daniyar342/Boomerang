from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from .services import *
from .serializers import *
from drf_spectacular.utils import extend_schema


# апи для регистрации user sellers wholeseller
class UserRegisterView(CreateUserApiView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer



# апи который проверяет код который был отправлен на указанный email и в ответ передает токен
class UserVerifyRegisterCode(generics.UpdateAPIView):
    serializer_class = VerifyCodeSerializer

    http_method_names = [
        "patch",
    ]

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get("code")
        return CheckCode.check_code(code=code)


class ForgetPasswordSendCodeView(generics.UpdateAPIView):
    serializer_class = SendCodeSerializer
    http_method_names = [
        "put",
    ]

    def put(self, request, *args, **kwargs):
        email_or_phone = request.data.get("email_or_phone")
        return ChangePassword.send_email_code(email_or_phone=email_or_phone)


class ForgetPasswordView(generics.UpdateAPIView):
    serializer_class = ForgetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ["patch"]

    def update(self, request, *args, **kwargs):
        response = ChangePassword.change_password_on_reset(self,request)
        print(request.user)
        # Проверяем статус ответа
        if response.status_code == status.HTTP_200_OK:
            return Response("Пароль успешно изменен", status=status.HTTP_200_OK)
        else:
            # Возвращаем ответ из метода change_password_on_reset, если пароль не был успешно изменен
            return response

# апи менят пароль в профиле
class UserResetPasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = [
        "patch",
    ]

    def update(self, request, *args, **kwargs):
        result = ChangePassword.change_password_on_profile(request=request)

        if result == "success":
            return Response("Пароль успешно изменен", status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class ListProfileApi(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer


class UpdateUserProfileApi(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = [
        "patch",
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    lookup_field = "id"


class DetailUserProfileApi(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "id"
