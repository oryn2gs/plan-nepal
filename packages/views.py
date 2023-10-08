from typing import Any
from django.views import generic
from packages.utils import get_most_popular_packages

from packages.models import (
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
        context_data['testimonial'] = Testimonial.objects.get_random_testimonial()
      
        context_data['popular'] = get_most_popular_packages()
        
        return context_data
    

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