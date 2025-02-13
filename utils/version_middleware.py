"""
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class VersioningMiddleware(MiddlewareMixin):
     def process_request(self, request):

         request.app_version = request.headers.get('X-App-Version', '1.0')

class VersionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        version = request.headers.get('X-App-Version')
        if version:
            request.version = version
        else:
            request.version = None
        
        response = self.get_response(request)
        return response
        
        
"""
#Middleware that checks the version of the user's application, header 'X-App-Version' is set on the client side