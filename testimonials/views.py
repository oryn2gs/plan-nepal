from django.shortcuts import HttpResponseRedirect
from testimonials.models import Testimonial
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


@login_required
@require_POST
def create_testimonial(request):
    http_referer = request.META.get('HTTP_REFERER') 
    redirect_url = http_referer if http_referer else reverse('homepage')

    data = request.POST
    user = request.user
    try:
        testimonial = Testimonial.objects.create(
                user = user,
                content = data.get("content"),
            )
        if not testimonial:
            raise Exception("Something went wrong, please try again later")
        messages.success(
            request, "Your testimonial has been added successfully")
        return HttpResponseRedirect(redirect_url)
    except Exception as e:
        messages.success(request, str(e))
        return HttpResponseRedirect(redirect_url)


    