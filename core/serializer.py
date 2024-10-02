from datetime import datetime, timedelta
from django.contrib.auth import password_validation as validator
from django.core import exceptions
from rest_framework import serializers
from .models import User, UserProfile, OTP
from home.utils import is_valid_email


class UserSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password", "palceholder": "Confirm Password"},
    )
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        )

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.pop("confirm_password")

        user = User(**data)

        if not is_valid_email(email):
            serializers.ValidationError("Invalid Email!")
        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "Confirm password doesn't match."}
            )

        errors = {}

        try:
            validator.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError({"error": errors})
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

    email = serializers.CharField()
    password = serializers.CharField(
        write_only=True, style={"input_type": "password", "placeholder": "Password"}
    )


class UserProfielSerailizer(serializers.ModelSerializer):
    user_name = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ("user_name", "profile", "cover_photo", "Description")

    def to_representation(self, instance):
        representation = super(UserProfielSerailizer, self).to_representation(instance)
        representation["user_name"] = (
            f"{instance.user.first_name} {instance.user.last_name}"
        )
        return representation

    def validate(self, data):
        expected_fields = ["user_name", "profile", "cover_photo", "Description"]
        required_keys = ["user_name"]
        fields: dict = self.initial_data
        errors = []
        required_key = []
        unexpected_key = []
        for field in fields.keys():
            if field not in expected_fields:
                unexpected_key.append(field)

        if unexpected_key:
            errors.append({"unexpected_fields": unexpected_key})

        if not self.partial:
            for field in required_keys:
                if field not in fields.keys():
                    required_key.append(field)

        if required_key:
            errors.append({"required_fields": required_key})

        if errors:
            raise serializers.ValidationError({"errors": errors})
        return data

    def update(self, instance, validated_data):
        user_name: str = validated_data.pop("user_name", None)
        if user_name:
            first_name, last_name = user_name.rsplit(" ", 1)
            instance.user.first_name = first_name
            instance.user.last_name = last_name
            instance.user.save()
        return super().update(instance, validated_data)


# class UserOTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTP
#         fields = ["otp"]

#     def is_otp_expired(self, user_otp, user):
#         otp_obj = OTP.objects.get(user=user)
#         gen_otp = otp_obj.otp
#         update_at = otp_obj.update_at

#         if gen_otp != user_otp:
#             return False

#         """expired time checking"""
#         current_time = datetime.now().strftime("%H:%M:%S")
#         expired_time = update_at + timedelta(minutes=5)
#         print(update_at.strftime("%H:%M:%S"), expired_time.strftime("%H:%M:%S"))
#         if current_time > expired_time.strftime("%H:%M:%S"):
#             return False
#         return True

#     def validate(self, data):
#         otp = data.get("otp")
#         user = self.context.get("user")
#         if (len(str(otp)) < 6 and len(str(otp)) > 6) or not self.is_otp_expired(
#             otp, user
#         ):
#             raise serializers.ValidationError(detail="Invalid otp")
#         return data
