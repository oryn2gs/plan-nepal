from typing import Any
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic

from packages.models import Package

from bookings.utils import _user_is_staff
from bookings.models import (
    Booking,
    Inquiry,
    InquiryAnswer
    )

@login_required
@require_POST
def create_booking(request, package_slug:str) -> HttpResponseRedirect:

    if request.method.lower() == "post":
        data = request.POST
        user = request.user

        redirect_url = reverse('package-detail', kwargs={'package_slug': package_slug}) if package_slug else reverse('homepage')

        try:
            package = get_object_or_404(Package, slug=package_slug)
            booking_made = Booking.objects.create(
                user = user,
                package = package,
                kids = int(data.get("kids")),
                adults = int(data.get("adults")),
                arrival_time = data.get("arrival_time"),
                arrival_date = data.get("arrival_date"),
                airlines = data.get("airlines"),
                flight_number = data.get("flight_number"),
                airport_pickup= data.get("airport_pickup"),
                message = data.get("message"),
            )
            if booking_made:
                messages.success(request, "Bookings made succefully, we\'ve sent a confirmation message to your email")
                # ?  send Bookings emails
            else:
                raise Exception("Unable to create bookings at the moment please try again")
         
        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(redirect_url)



class FaqListView(generic.ListView):
    model = Inquiry
    context_object_name = 'inquiries'
    template_name = 'bookings/faq-list.html'

   
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)

        context_data['faq_resolved'] = Inquiry.objects.filter_inquiry_by_resolved_value(resolved=True)
        
        context_data['faq_unresolved'] = Inquiry.objects.filter_inquiry_by_resolved_value(resolved=False)
        # # add pagintaino later for unresolved 
        # ! create a filter tag for resolved

        return context_data
    

@login_required
@require_POST
def post_inquiry(request) -> JsonResponse:
    try:
        user = request.user
        data = request.POST
        fields = ["inquiry_type", "question"]
        for field in fields:
            if field not in data:
                raise Exception(f"Missing field {field}, please complete the form")
        inquiry_created = Inquiry.objects.create(
            user = user,
            inquiry_type = data.get("inquiry_type"),
            question = data.get("question")
        )
        if not inquiry_created:
            raise Exception("Some thing went wrong, please try again later.")
        return JsonResponse({
            "status": "success",
            "message": "Your Inquiry has been posted, we\'ll notify you once our operator responds."
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status = 400)
    



@user_passes_test(_user_is_staff)
@require_POST
def reply_inquiry(request) -> HttpResponseRedirect:
    try:
        http_referer = request.META.get("HTTP_REFERER")
        redirect_url = http_referer if http_referer else reverse('homepage')
        user = request.user
        data = request.POST
        fields = ["inquiry_id", "content"]
        for field in fields:
            if field not in data:
                raise Exception(f"This {field} is required, please complete the form")
            
        inquiry = get_object_or_404(Inquiry, id=data.get("inquiry_id"))
        
        inquiry_replied = InquiryAnswer.objects.create(
            user= user,
            inquiry = inquiry,
            content = data.get("content")
        )
        if not inquiry_replied:
            raise Exception("Something went wrong, please try again later.")
        
        messages.success(request, "Your answer to customer queries, has been added succefully.")
        return HttpResponseRedirect(redirect_url)
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect(redirect_url)








