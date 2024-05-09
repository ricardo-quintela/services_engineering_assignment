from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group

from rest_framework import permissions, viewsets
from .serializers import UserSerializer, GroupSerializer

from .forms import AuthForm

class UserViewSet(viewsets.ModelViewSet):
    """To see the created users
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

def login_view(request: HttpRequest) -> HttpResponse:
    """Logs a user in

    Args:
        request (HttpRequest): the request

    Returns:
        HttpResponse: the rendered login template
    """

    if request.method == "POST":
        login_form = AuthForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request=request, user=user)

    else:
        login_form = AuthForm()


    context = {
        "login_form": login_form
    }

    return render(request, "login.html", context=context)


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """Logs a user out and redirects to the home page

    Args:
        request (HttpRequest): the request

    Returns:
        HttpResponseRedirect: a redirect to the landing page
    """
    logout(request)
    return redirect("/")
