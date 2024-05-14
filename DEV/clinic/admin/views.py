from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from rest_framework.decorators import api_view
from .permissions import perm_required


@api_view(["GET"])
def base_app_view(request: HttpRequest) -> HttpResponse:
    """Renders the base app template

    Args:
        request (HttpRequest): the request data

    Returns:
        HttpResponse: the rendered app template
    """
    return render(request, "base.html")

@perm_required("admin")
@api_view(["GET"])
def admin_app_view(request: HttpRequest) -> HttpResponse:
    return render(request, "admin.html")
