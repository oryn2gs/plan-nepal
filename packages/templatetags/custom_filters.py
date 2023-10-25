from django import template
from django.db.models import Q
from packages.models import Package
import re

register = template.Library()

@register.filter
def filter_packages_by_destination(packages:object, destination_name: str = "") -> object:
    
    queryset = packages.filter(
        Q(destination__name__iexact=destination_name) & Q(active=True)
        )

    return queryset


@register.filter
def filter_packages_by_type(packages:object, type_name: str = None) -> object:
    
    if re.match(type_name, "all", re.IGNORECASE):
        queryset = packages
    else: 
        queryset = packages.filter(
            Q(type__name__iexact=type_name) & Q(active=True)
            )

    return queryset