from django.urls import path
from .views import UserSignupView, UserLoginView, UserProfileView

urlpatterns = [
    path("auth/signup/", view=UserSignupView.as_view(), name="user-signup"),
    path("auth/login/", view=UserLoginView.as_view(), name="user-login"),
    path("profile/", view=UserProfileView.as_view(), name="user-profile"),
    # path("otp/", view=UserOTPView.as_view(), name="get-and-validate-login-otp"),
]
