from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets
from .serializers import UserSerializer, GroupSerializer
from django.shortcuts import render
from django.contrib.auth import authenticate

from .forms import LoginForm

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

def login(request):

    if request.method == "POST":
        login_form = LoginForm(request)
    else:
        login_form = LoginForm()

    context = {
        "login_form": login_form
    }

    return render(request, "login.html", context=context)
