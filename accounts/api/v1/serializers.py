from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from ...models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "Passwords doesn't match"})

        try:
            validate_password(password=attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")

            if not user.is_verified:
                raise serializers.ValidationError({"detail": "User must be verified."})
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"detail": "User must be verified."})
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing the user's password
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "Passwords doesn't match"})

        try:
            validate_password(password=attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "email", "first_name", "last_name", "image", "bio")


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except:
            raise serializers.ValidationError({"details": "User does not exists."})

        if user_obj.is_verified:
            raise serializers.ValidationError(
                {"details": "User has already been activated."}
            )

        attrs["user"] = user_obj
        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer to reset the user's password
    """

    email = serializers.EmailField(required=True)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    Serializer to reset the user's password
    """

    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "Passwords doesn't match"})

        try:
            validate_password(password=attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)
