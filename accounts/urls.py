from django.urls import path

from accounts.views import (
    UserRegistrationView,
    UserLoginView,
    logout_view
)

urlpatterns = [
    path("signup/", UserRegistrationView.as_view(), name="signup"),
    path("signin/", UserLoginView.as_view(), name="signin"),
    path("signout/", logout_view, name="signout"),
]