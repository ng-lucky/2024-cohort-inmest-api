from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action

# Create your views here.

def signup(request):
    username = request.POST["username"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    phone_number = request.POST["phone_number"]
    password = request.POST["password"]


    new_user = IMUser.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
        )
    new_user.set_password(password)
    new_user.save()


class UserViewSet(viewsets.ModelViewSet):
  
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password', None)
        player_id = request.data.get('player_id', None)
    
        user = authenticate(email=email, password=password)
        login(request, user)

        