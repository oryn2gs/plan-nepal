from django.urls import path
from bookings.views import (
    create_booking, 
    FaqListView,
    post_inquiry,
    reply_inquiry,
    )

urlpatterns = [
    path('create-booking/<slug:package_slug>/', create_booking, name="create-booking"),
    
    path('faq/', FaqListView.as_view(), name="faq-list"),
    path('faq/post/', post_inquiry, name="post-inquiry"),
    path('faq/replies/', reply_inquiry, name="reply-inquiry"),
]