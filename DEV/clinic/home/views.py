from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page_view(request: HttpRequest) -> HttpResponse:
    """The website's home page

    Args:
        request (HttpRequest): the request

    Returns:
        HttpResponse: the rendered home page
    """
    context = {}
    return render(request, "home.html", context)
