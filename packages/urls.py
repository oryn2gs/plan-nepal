from django.urls import path
from packages.views import Homepage, PackageDetailPage

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('packages/<slug:slug>/', PackageDetailPage.as_view(), name='package-detail')
]