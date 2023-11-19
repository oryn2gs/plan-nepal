
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404
handler404 = 'src.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('packages.urls')),
    path('booking/', include('bookings.urls')),
    path('testimonial/', include('testimonials.urls')),
    path('accounts/', include('accounts.urls')),
    path('subscriptions/', include('subscriptions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
