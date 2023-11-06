
from accounts.forms import (
    UserRegistrationForm,
    UserLoginForm
    )

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

from accounts.forms import UserRegistrationForm


class UserRegistrationView(generic.CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('homepage')


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        messages.success(self.request, "Your account has been created successfully, and you\'re logged in.")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error in the registration form.")
        return super().form_invalid(form)



class UserLoginView(generic.View):
    template_name = "accounts/signin.html"
    success_url = reverse_lazy('homepage')
    form_class = UserLoginForm

    def get(self, request):
        form_class = self.form_class
        return render(request, self.template_name, {'form': form_class})

    def post(self, request):
        http_referer = request.META.get("HTTP_REFERER")
        redirect_url = http_referer if http_referer else self.success_url

        form = self.form_class(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login in successfully.")
                return HttpResponseRedirect(redirect_url)
        messages.error(request, "Invalid credentails")
        return render(request, self.template_name, {'form': self.form_class})


@login_required
# @require_POST
def logout_view(request):
    # !write a a test case
    http_referer = request.META.get("HTTP_REFERER")
    response_url = http_referer if http_referer else reverse_lazy('homepage')
    logout(request)
    messages.success(request, "Logout Successfully")
    return HttpResponseRedirect(response_url)








