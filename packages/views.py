from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from packages.utils import _get_most_popular_packages, _get_types_list
from packages.templatetags.custom_filters import filter_packages_by_type
from packages.models import (
    Package, 
    TourTimeline
    )
from accounts.forms import UserProfileForm
from testimonials.models import Testimonial

from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from bookings.forms import BookingForm


class Homepage(generic.ListView):
    paginate_by = 20
    context_object_name = 'packages'
    template_name = 'packages/homepage.html'

    def get_queryset(self) -> QuerySet[Any]:
        return Package.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data['testimonials'] = Testimonial.objects.get_random_testimonial()
        context_data['popular'] = _get_most_popular_packages()
        context_data['types'] = _get_types_list()
        context_data['type_filter'] = kwargs.get("type_filter")

        return context_data

    def get(self, request, *args, **kwargs):
        type_filter = request.GET.get("type_filter")
        self.object_list = self.get_queryset()
        queryset = self.get_queryset()

        if type_filter:
            queryset = queryset.filter(type__name__iexact=type_filter)

        context = self.get_context_data(
            object_list=queryset, type_filter=type_filter
            )

        return self.render_to_response(context)


class AboutUsPage(generic.View):
    template_name = "packages/about-us.html"

    def get(self, request) -> render:
        return render(request, self.template_name,{})


class PackageDetailPage(UserPassesTestMixin, generic.DetailView):
    model = Package
    context_object_name = 'package'
    template_name = 'packages/package-detail.html'
    slug_url_kwarg = 'package_slug'
    booking_form = BookingForm
    user_form = UserProfileForm

    def test_func(self):
        if self.request.method == 'POST':
            return self.request.user.is_authenticated # if method POST meaning booking creation user need to be authenticated
        return True
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        instance = self.get_object()

        context_data['tour_timeline'] = TourTimeline.objects.filter_instance_related_to_package(
            package_slug = instance.slug
            )
        
        if self.request.user.is_authenticated:
            user = self.request.user
            profile = user.profile
            initial_data = {
                "firstname": profile.firstname,
                "lastname": profile.lastname,
                "date_of_birth": profile.date_of_birth,
                "country": profile.country,
                "country_code": profile.country_code,
                "phone_number": profile.phone_number,
                "gender": profile.gender
            }
            context_data["user_profile_form"] = self.user_form(
                initial=initial_data
            )
        else: 
            context_data["user_profile_form"] = self.user_form()
        context_data["booking_form"] = self.booking_form()
        return context_data
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        profile = user.profile

        booking_form = self.booking_form(data=request.POST)
        user_form = self.user_form(
            instance=profile, data=request.POST
            )
        if booking_form.is_valid() and user_form.is_valid():
            user_form.save()
            booking = booking_form.save(commit=False)
            booking.user = user
            booking.package = self.object
            booking.save()
            messages.success(request, "Bookings created successfully.")
            from packages.emails import send_booking_confirmation_email
            from django.core.exceptions import ValidationError
            if not send_booking_confirmation_email(self.request, user, booking):
                raise ValidationError(
                    "Unable to send email at the moment, please try again", code="bad_request")

            return HttpResponseRedirect(reverse('package-detail', kwargs={
                'package_slug': self.object.slug
            }))
        
        context = self.get_context_data(object=self.object)  
        context["booking_form"] = booking_form
        context["user_profile_form"] = user_form
        return render(
            request, self.template_name, context)



@require_GET
def filter_packages(request) -> HttpResponse:
    try:
        query = request.GET.get("query")
        packages = Package.objects.all()
        results = filter_packages_by_type(packages, query)
        from django.core.exceptions import EmptyResultSet
        if not results:
            raise EmptyResultSet(
                "Unable to fetch content at the moment please try again later"
                )

        html_fragment = render(request, 'packages/package-card.html', {
            'packages': results,
            'type': query
            })
        return HttpResponse(html_fragment.content)
      
    except EmptyResultSet as empty_result_set:
        html_fragment = render(request, 'packages/package-card.html', {
            'error': str(empty_result_set)
            })
        return render(html_fragment.content)
    
    except Exception as e:
        html_fragment = render(request, 'packages/package-card.html', {
            'error': str(e)
            })
        return render(html_fragment.content)
  