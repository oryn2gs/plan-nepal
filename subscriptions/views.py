from subscriptions.models import Subscription
from subscriptions.forms import SubscriptionsForm

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import messages


class SubscriptionCreateView(generic.CreateView):
    form_class = SubscriptionsForm

    def post(self, request, *args, **kwargs):
        http_referer = request.META.get("HTTP_REFERER")
        response_url = http_referer if http_referer else reverse_lazy('homepage')

        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                "Subscription added successfully"
                )
            return HttpResponseRedirect(response_url)
        
        try:
            email = request.POST.get("email")
            obj = get_object_or_404(Subscription, email=email)
            obj.active = True
        except Http404:
            pass
 
        messages.error(
            request, str(form.errors))
        return HttpResponseRedirect(response_url)
