from django.urls import path

from accounts.views import (
    UserRegistrationView,
    UserLoginView,
    LogoutView,
    RequestResetPasswordView,
    RequestResetPasswordDoneView,
    ResetPasswordConfirmView,
     ResetPasswordCompleteView
)

urlpatterns = [
    path("signup/", UserRegistrationView.as_view(), name="signup"),
    path("signin/", UserLoginView.as_view(), name="signin"),
    path("signout/", LogoutView.as_view(), name="signout"),

    path("request-reset-password/", 
         RequestResetPasswordView.as_view(), 
         name="request-reset-password"),
    path("reset-password-done/", 
         RequestResetPasswordDoneView.as_view(), 
         name="reset-password-done"),
    path("reset-password-confirm/<str:slug>/<str:token>/", 
         ResetPasswordConfirmView.as_view(), 
         name="reset-password-confirm"),
    
    path("reset-password-complete/", 
         ResetPasswordCompleteView.as_view(), 
         name="reset-password-complete"),


]