from django.urls import path

from accounts.views import (
    UserRegistrationView,
    UserLoginView,
)

urlpatterns = [
    path("signup/", UserRegistrationView.as_view(), name="signup"),
    path("signin/", UserLoginView.as_view(), name="signin"),
]