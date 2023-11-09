from django.urls import path
from subscriptions.views import SubscriptionCreateView


urlpatterns = [
    path("add/", SubscriptionCreateView.as_view(), name="create-subs"),
]

