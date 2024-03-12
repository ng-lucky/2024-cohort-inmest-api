from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from .serializers import *
from rest_framework import status
from inmest_api.utils import *

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get("username")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")
    new_user = IMUser.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
        )
    new_user.set_password(password)
    new_user.save()
    # new_user.generate_auth_token()
    serializer = AuthSerializer(new_user, many=False)
    return Response({"message": "Account successfully created", "result": serializer.data})

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    #1. Receive inputs/data from client and validate inputs
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"detail": "My friend behave yourself and send me username and password"}, status.HTTP_400_BAD_REQUEST)
    #2. Check user existence

    try:
        user = IMUser.objects.get(username=username)
        #3. User authentications
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            #4. Login user
            login(request, user)
            serializer = AuthSerializer(user, many=False)
            return Response({"result": serializer.data }, status.HTTP_200_OK)

        else:
            if user.temporal_login_fails >= 3:
                user.permanent_login_fails += 1

            user.temporal_login_fails += 1
            
            return Response({"detail": "Invalid credentials"}, status.HTTP_400_BAD_REQUEST)

    except IMUser.DoesNotExist:
        return Response({"detail": "Username does not exist"}, status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        #1. receive the username (email)
        username = request.data.get("username")
        if not username:
            return generate_400_response("Please provide valid username")
        #2. Check if the user exists
        try:
            user = IMUser.objects.get(username=username)
            otp_code = generate_unique_code()
            #3. send OTP code
            user.unique_code = otp_code
            user.save()
            #send email or sms at this point

            #4. Respond to the user
            return Response({"detail": "Please check your email for an OTP code"}, status.HTTP_200_OK)
            
        except IMUser.DoesNotExist:
            return generate_400_response("Username does not exist")
        

class UserViewSet(viewsets.ModelViewSet):
  
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password', None)
        player_id = request.data.get('player_id', None)
    
        user = authenticate(email=email, password=password)
        login(request, user)


class ResetPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
      
        unique_code = request.data.get('unique_code')
        new_password = request.data.get('new_password')
        username = request.data.get('username')

        if not unique_code:
            return generate_400_response("Unique Code is required")
        if username == None or username == "":
            return generate_400_response("Email is required")
        if new_password is None:
            return generate_400_response("Provide password")

        try:
            myuser = IMUser.objects.get(unique_code=unique_code, username=username)
            myuser.unique_code = ""
            myuser.temporal_login_fails = 0
            myuser.permanent_login_fails = 0
            myuser.set_password(new_password)
            myuser.is_active = True
            myuser.is_blocked = False
            myuser.save()

            user = AuthSerializer(myuser, context={'request': request})
            return Response({'results': user.data, 'response_code': '100'}, status=200)

        except IMUser.DoesNotExist:
            return Response({'detail': "Invalid OTP Code", 'response_code': '101'}, status=400)   



class CurrentUserProfile(APIView):

    def get(self, request, *args, **kwargs):
        """
        Fetches a user's profile
        """
        user = UserSerializer(request.user, many=False, context={'request': request})
        return Response({'results': user.data, 'response_code': '100'}, status=200)

    def put(self, request, *args, **kwargs):
        """
        Updates a user's profile

        """
        user = request.user
        first_name = request.data.get("first_name")
        profile = request.data
        # profile.profile_picture = request.data.get("user_avatar")

        try:
            serializer = UserSerializer(user, context={'request': request}, data=profile, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'results': serializer.data, 'response_code': '100'}, status=200)
            return Response({'results': serializer.errors, 'response_code': '101'}, status=400)
        except:
            serializer = UserSerializer(user, context={'request': request}, data=profile, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'results': serializer.data, 'response_code': '100'}, status=200)
            serializer = UserSerializer(profile, context={'request': request})
            return Response({'detail': serializer.errors, 'response_code': '100'}, status=400)
    
class ChangePassword(APIView):
    """
    Change password if logged in   
    """

    def post(self, request, *args, **kwargs):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        username = request.user.username
        if old_password is None:
            return Response({'detail': "Please provide old password", 'response_code': '101'},
                            status=400)
        if new_password is None:
            return Response({'detail': "Please provide new password", 'response_code': '101'},
                            status=400)
        if old_password == new_password:
            return Response({'detail': "Old and new passwords must not be same", 'response_code': '101'},
                            status=400)

        user = authenticate(username=username, password=old_password)

        if user is not None:
            myuser = request.user
            myuser.set_password(new_password)
            myuser.save()

            user = UserSerializer(myuser, context={'request': request})
            return Response({'results': user.data, 'response_code': '100'}, status=200)
        else:
            return Response({'detail': "Your old password is incorrect", 'response_code': '101'},
                            status=400)