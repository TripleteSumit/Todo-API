import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from core.models import User, OTP, UserProfile
from .serializer import (
    UserSignupSerializer,
    UserLoginSerializer,
    UserProfielSerailizer,
)
from home.utils import get_token, send_mail_for_login_otp


class UserSignupView(APIView):
    serializer_class = None

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"status": "success", "msg": "User account created."},
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response(
                data={
                    "status": "failed",
                    "msg": "Invalid email and password. Try again",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.login_count = (0 if not user.login_count else user.login_count) + 1
        user.save()
        return Response(
            data={
                "status": "success",
                "msg": "Login successfull",
                "data": get_token(user),
            },
            status=status.HTTP_200_OK,
        )


class UserProfileView(APIView):
    serializer_class = UserProfielSerailizer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_obj = get_object_or_404(UserProfile, user=request.user)
        serializer = self.serializer_class(user_obj, context={"request": request})
        return Response(
            data={
                "status": "success",
                "message": "user profile fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        user_obj = get_object_or_404(UserProfile, user=request.user)
        seralizer = self.serializer_class(
            instance=user_obj,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        seralizer.is_valid(raise_exception=True)
        seralizer.save()
        return Response(
            data={
                "status": "success",
                "msg": "User Profile Is Updated",
                "data": seralizer.data,
            },
            status=status.HTTP_200_OK,
        )


# class UserOTPView(APIView):
#     serializer_class = OTP

#     def get(self, request):
#         def gen_otp(email):
#             otp = random.randint(100000, 999999)
#             errors = []
#             try:
#                 user_obj = get_object_or_404(User, email=email)
#                 OTP.objects.update_or_create(user=user_obj, defaults={"otp": otp})
#             except ValidationError as e:
#                 return errors.append(e.messages)
#             return otp, errors

#         email = request.query_params.get("email")
#         if not email:
#             return Response(
#                 data={"email": "Email is required query parameter."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         otp, errors = gen_otp(email)
#         if errors:
#             return Response(
#                 data={"status": "failed", "message": "Email id doesn't exists"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         data = {"otp": otp, "mail": email}
#         send_mail_for_login_otp(data)
#         print(otp)
#         return Response(
#             data={"status": "success", "message": "Check your email."},
#             status=status.HTTP_200_OK,
#         )

#     def post(self, request):
#         email = request.data.get("email")

#         if not email:
#             return Response(
#                 data={"email": "Email is a required field."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         user_obj = get_object_or_404(User, email=email)
#         serializer = UserOTPSerializer(data=request.data, context={"user": user_obj})
#         serializer.is_valid(raise_exception=True)
#         return Response(
#             data={"status": "success", "message": "OTP is successfully validate."},
#             status=status.HTTP_200_OK,
#         )
