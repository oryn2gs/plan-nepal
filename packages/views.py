from typing import Any
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.contrib import messages

from packages.utils import _get_most_popular_packages, _get_types_list
from packages.templatetags.custom_filters import filter_packages_by_type
from packages.models import (
    Type,
    Package, 
    TourTimeline
    )
from testimonials.models import Testimonial


    
class Homepage(generic.ListView):
    model = Package
    context_object_name = 'packages'
    template_name = 'packages/homepage.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data['testimonials'] = Testimonial.objects.get_random_testimonial()
      
        context_data['popular'] = _get_most_popular_packages()
        context_data['types'] = _get_types_list()
        #!paginnated packages
        return context_data


class AboutUsPage(generic.View):
    template_name = "packages/about-us.html"

    def get(self, request) -> render:
        return render(request, self.template_name,{})

    

class PackageDetailPage(generic.DetailView):
    model = Package
    context_object_name = 'package'
    template_name = 'packages/package-detail.html'
    slug_url_kwarg = 'package_slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        instance = self.get_object()

        context_data['tour_timeline'] = TourTimeline.objects.filter_instance_related_to_package(
            package_slug = instance.slug
            )
        return context_data
    



@require_GET
def filter_packages(request) -> HttpResponse:
    try:
        query = request.GET.get("query")
        packages = Package.objects.all()
        results = filter_packages_by_type(packages, query)
        from django.core.exceptions import EmptyResultSet
        if not results:
            raise EmptyResultSet("Unable to fetch content at the moment please try again later")

        html_fragment = render(
            request, 
            'packages/package-card.html', 
            {'packages': results}
            )
        return HttpResponse(html_fragment.content)
    
    
    except EmptyResultSet as empty_result_set:
        html_fragment = render(request, 'packages/package-card.html', {'error': str(empty_result_set)})
        return render(html_fragment.content)
    
    except Exception as e:
        html_fragment = render(request, 'packages/package-card.html', {'error': str(e)})
        return render(html_fragment.content)
  