from django.urls import path
from packages.views import (
    Homepage, 
    AboutUsPage,
    PackageDetailPage, 
    filter_packages
    )

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('about-us/', AboutUsPage.as_view(), name='about-us'),
    path('packages/filter/', filter_packages, name='packages-filter'),
    path('packages/<slug:package_slug>/', PackageDetailPage.as_view(), name='package-detail'),
]