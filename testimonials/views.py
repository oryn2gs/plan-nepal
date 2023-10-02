from django.shortcuts import HttpResponseRedirect
from testimonials.models import Testimonial
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST



@require_POST
def create_testimonial(request):
    referer = request.META.get('HTTP_REFERER') # get the previous url from header
    redirect_url = referer if referer else reverse('homepage')

    data = request.POST
    image = request.FILES

    try:
        Testimonial.objects.create(
                username = data.get("username"),
                content = data.get("content"),
                user_image = image.get("user_image"),
                city = data.get("city"),
                country = data.get("country")
            )
        messages.success(
            request, "Your testimonial has been added successfully")
        return HttpResponseRedirect(redirect_url)
    except Exception as e:
        messages.success(request, str(e))
        return HttpResponseRedirect(redirect_url)


    