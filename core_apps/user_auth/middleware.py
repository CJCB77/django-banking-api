"""
Django treats middleware as a callable that accepts a request object and returns a response object.
It identifies this by using duck typing.

Which basically means:
“If your object can be called like a function (__call__) and accepts get_response 
in __init__, I'll treat it as middleware
"""
class CustomHeaderMiddleware:
    def __init__(self, get_response):
        # A callable that when called with a request returns a response
        self.get_response = get_response
    
    def __call__(self, request):
        # You can do something before the view is called
        # here
        # Call the next middleware in the change or the view itself
        response = self.get_response(request)
        # We do something with the response here
        if request.user.is_authenticated:
            response['X-Django-User'] = request.user.email
        return response
        