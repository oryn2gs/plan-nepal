
from typing import Any

from accounts.emails import send_reset_password_email

from accounts.utils import verify_token
from accounts.forms import (
    UserRegistrationForm,
    UserLoginForm,
    RequestResetPasswordForm,
    PasswordResetForm,
    )

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.http import HttpRequest, HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
User = get_user_model()



class UserRegistrationView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        messages.success(
            self.request, 
            "Your account has been created successfully, and you\'re logged in.")
        return super().form_valid(form)
    

class UserLoginView(generic.FormView):
    template_name = "accounts/signin.html"
    success_url = reverse_lazy('homepage')
    form_class = UserLoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)
        login(self.request, user)
        messages.success(self.request, "Logged in successfully.")
        return HttpResponseRedirect(self.success_url)


class LogoutView(LoginRequiredMixin, generic.View):

    def post(self, request) -> HttpResponseRedirect:
        http_referer = request.META.get("HTTP_REFERER")
        response_url = http_referer if http_referer else reverse_lazy('homepage')
        logout(request)
        messages.success(request, "Logout Successfully")
        return HttpResponseRedirect(response_url)


class RequestResetPasswordView(generic.FormView):
    form_class = RequestResetPasswordForm
    template_name = "accounts/request-reset-password.html"
    success_url = reverse_lazy('reset-password-done')

    def form_valid(self, form: RequestResetPasswordForm) -> Any:
        email = form.cleaned_data.get("email")
        user = get_object_or_404(User, email=email)
        
        if not send_reset_password_email(self.request, user):
            raise ValidationError(
                    "Unable to send email at the moment, please try again", code="bad_request")
        else:
            messages.success(
                self.request,
                "We\'ve sent a email with link to reset your password")
            return super().form_valid(form)
 
    
class RequestResetPasswordDoneView(generic.View):
    template_name = "accounts/reset-password-done.html"

    def get(self, request) -> render:
        return render(request, self.template_name, {})


class ResetPasswordConfirmView(generic.FormView):
    template_name = "accounts/reset-password-confirm.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> Any:
        try:
            instance = self.get_user(slug=kwargs.get("slug"))
            if not verify_token(instance, kwargs.get("token")):
                raise ValueError("Verification Token is Invalid or Expired, Please try again.")
            
            self.request.session["slug"] = instance.slug
            messages.success(self.request, "Token verification successful")
            return HttpResponseRedirect(reverse('reset-password-complete'))

        except ValueError as e :
            messages.error(request, str(e))
            return HttpResponse(status=404)

    def get_user(self, slug:str = "") -> User:
        try:
            slug = force_str(urlsafe_base64_decode(slug))
        except Exception as e:
            raise ValueError("There was a issue decoding account id, Please try again later.")
        try:
            instance = get_object_or_404(User, slug=slug)
        except Http404 as e :
            messages.error(self.request, "User with that slug doesn\'t exists")
            return HttpResponse(status=404)
        return instance
    
    
class ResetPasswordCompleteView(generic.FormView):
    template_name = "accounts/reset-password-complete.html"
    success_url = reverse_lazy('signin')
    form_class = PasswordResetForm

    def form_valid(self, form: PasswordResetForm) -> HttpResponse:
        slug = self.request.session["slug"]
        try:
            instance = get_object_or_404(User, slug=slug)
        except Http404 as e:
            messages.error(self.request, "User not found")
            return HttpResponse(status=404)
        password = form.cleaned_data.get("password")
        instance.set_password(password)
        instance.save()
        return super().form_valid(form)


