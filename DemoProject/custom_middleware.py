# Created by Karthik Ravinatha at 3:41 pm 06/06/23 using PyCharm
from django.utils.deprecation import MiddlewareMixin


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.exception_count = 0
        self.template_msg = {"message": "Data loaded Successfully"}

    def __call__(self, request):
        # Code block that is executed in each request before the view is called

        response = self.get_response(request)

        # Code block that is executed in each request after the view is called
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    # This code is executed just before the view is called
    def process_view(self, request, view_func, view_args, view_kwargs):
        """This is executed before a call to view"""
        self.request_count += 1
        print(f"Total request received {self.request_count}")

    # This code is executed if an exception is raised
    def process_exception(self, request, exception):
        self.exception_count += 1
        print(f"Exception Count: {self.exception_count}")

    def process_response(self, request, response):
        print("Process Response Called")
        return response


def custom_middleware(get_response):
    # One-time configuration and initialization.
    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print("Called before the view function")

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        print("Called after the view function")

        return response

    return middleware

    # def process_template_response(self, request, response):
    #     # This code is executed if the response contains a render() method
    #     print("Processed template response")
    #     return response
