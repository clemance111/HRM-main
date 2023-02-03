from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from accounts.models import User, Employee, OtpCode
from accounts.email import Email
from accounts.utils import generate_otp
from accounts.serializers import CreateUserSerializer, OTPValidationSerializer, ResendOTPSerializer, ForgotPasswordSerializer, ResetPasswordSerializer


class UserViewset(ModelViewSet):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        otp = generate_otp(4)
        otp_instance = OtpCode.objects.create(
            user=serializer.user, code=otp, otp_type=OtpCode.REGISTRATION)
        Email(to=[serializer.user.email], subject="Verification email",
              message=f"Greetings please use this OTP for account verification {otp_instance.code}").send()
        return serializer.user


class CheckOTPView(APIView):
    def post(self, request):
        serializer = OTPValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=200)


class ResendOTPView(APIView):
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        otp_code = generate_otp(4)
        OtpCode.objects.filter(user=user, code=otp_code).delete()
        otp_instance = OtpCode.objects.create(user=user, code=otp_code)
        Email([user.email], "We sent you an OTP",
              message=f"We resent you this OTP for verification please use it before 5minuts {otp_instance.code}").send()
        return Response({"message": "OTP was resent"}, status=201)


class ActivateAccountAPI(APIView):
    def post(self, request):
        serializer = OTPValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.active = True
        user.save()
        return Response(status=200)


class ForgotPasswordAPI(APIView):
    def post(self, request):
        email_serializer = ForgotPasswordSerializer(data=request.data)
        email_serializer.is_valid(raise_exception=True)
        user = email_serializer.user
        otp = generate_otp(6)
        otp_instance = OtpCode.objects.create(
            user=user, otp_type=OtpCode.RESET_PASSWORD, code=otp)
        Email(to=[user.email], subject="Passowrd reset",
              message=f"Greetings please use this OTP for password reset verification {otp_instance.code}").send()
        return Response({"message": "We sent an OTP to your email"})

class ResendPasswordResetOTP(APIView):
    def post(self,request):
        email_serializer = ForgotPasswordSerializer(data=request.data)
        email_serializer.is_valid(raise_exception=True)
        user = email_serializer.user
        OtpCode.objects.filter(user=user,otp_type=OtpCode.RESET_PASSWORD).delete()
        otp = generate_otp(6)
        otp_instance = OtpCode.objects.create(
            user=user, otp_type=OtpCode.RESET_PASSWORD, code=otp)
        Email(to=[user.email], subject="Passowrd reset",
              message=f"Greetings please use this OTP for password reset verification {otp_instance.code}").send()
        return Response({"message": "We sent an OTP to your email"})

class ResetPasswordAPI(APIView):
    def post(self, request, otp=None):
        try:
            instance = OtpCode.objects.get(
                code=otp, otp_type=OtpCode.RESET_PASSWORD)
            if not instance.is_valid:
                raise NotFound(detail="The OTP provided has expired")
        except OtpCode.DoesNotExist:
            raise NotFound(detail="THe OTP provided was not found")
        user = instance.user
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data.get("new_password"))
        user.save()
        return Response({"message": "Your password has been changed successfully"}, status=200)
