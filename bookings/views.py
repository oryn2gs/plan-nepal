from typing import Any
from django.shortcuts import (
    HttpResponseRedirect, 
    get_object_or_404, 
    HttpResponse, 
    render
    )
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic, View
from django.core.exceptions import EmptyResultSet

from packages.models import Package

from bookings.utils import _user_is_staff
from bookings.models import (
    Booking,
    Inquiry,
    InquiryAnswer
)




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
def post_inquiry(request) -> HttpResponseRedirect:
    redirect_url = reverse('faq-list')
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
        
        messages.success(request, "Your Inquiry has been posted, we\'ll notify you once our operator responds.")
        return HttpResponseRedirect(redirect_url)
   
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect(redirect_url, status = 400)



@user_passes_test(_user_is_staff)
@require_POST
def reply_inquiry(request) -> HttpResponseRedirect:

    http_referer = request.META.get("HTTP_REFERER")
    redirect_url = http_referer if http_referer else reverse('homepage')
    try:
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




@require_GET
def filter_inqury(request) -> HttpResponse:
    try:
        query = request.GET.get("query")
        print(query)

        if query.lower() == "all":
            results = Inquiry.objects.filter_inquiry_by_resolved_value(True)
        elif query.lower() == "unresolved":
            results = Inquiry.objects.filter_inquiry_by_resolved_value(False)
        else:
            results = Inquiry.objects.filter_inquiry_by_resolved_value(True).filter(inquiry_type__iexact=query)

        if not results:
            # dynamically add the query name
            raise EmptyResultSet("There is no content related to the tag.")
        

        html_fragment = render(
            request, 
            'bookings/faq-card.html', 
            {'faq_resolved': results}
            )
        return HttpResponse(html_fragment.content)

    except EmptyResultSet as empty_result_exp:
        html_fragment = render(
            request, 
            'bookings/faq-card.html', 
            {'error': str(empty_result_exp)})
        return HttpResponse(html_fragment.content)
    
    except Exception as e:
        html_fragment = render(
            request, 
            'bookings/faq-card.html', 
            {'error': str(e)})
        return HttpResponse(html_fragment.content)
  



