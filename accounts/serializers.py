from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password as valid_password_check
from rest_framework import serializers
from accounts.models import User, OtpCode

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'gender',
            'email',
            'password'
        ]

    def validate_password(self, passkeyword):
        try:
            valid_password_check(password=passkeyword)
            return passkeyword
        except DjangoValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

    def validate(self, attrs):
        super().validate(attrs)
        try:
            User.objects.get(user_type=User.HR)
            raise serializers.ValidationError(
                {"error": "A human resource user is already registered"})
        except User.DoesNotExist:
            return attrs
        return

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        self.user = user
        return user


class OTPValidationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    def validate_otp(self, code):
        try:
            otp = OtpCode.objects.get(code=code)
            if otp.is_valid:
                self.user = otp.user
                return code
            else:
                otp.delete()
                raise serializers.ValidationError("OTP has expired")
        except OtpCode.DoesNotExist:
            raise serializers.ValidationError("OTP is not valid")


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, input_email):
        try:
            user = User.objects.get(email=input_email)
            self.user = user
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exists")


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, input_email):
        try:
            user = User.objects.get(email=input_email)
            self.user = user
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exists")

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)
    def validate_new_password(self,password):
        try:
            valid_password_check(password=password)
            return password
        except DjangoValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )