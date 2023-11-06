from django.shortcuts import redirect
from django.urls import reverse

class BlockAuthenticatedUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # code to be excuted before processing request
        restricted_view_list = ['/accounts/signin/', "/accounts/signup/"]

        if request.path in restricted_view_list and request.user.is_authenticated:
            referer = request.META.get('HTTP_REFERER', None)
            
            redirect_url = referer if referer else reverse('homepage')
            
            return redirect(redirect_url)

        response = self.get_response(request)
        # code to be excuted after processing request
        return response
