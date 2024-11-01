from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

from . models import Profile
from . serializers import *

# register view
class Register(APIView):
    def post(self,request):
         # Check if user is already authenticated
        if request.user.is_authenticated:
            dashboard_url = reverse('dashboard')
            return Response({"redirect_url": dashboard_url}, status=status.HTTP_200_OK)
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Include the next URL in the response for client-side handling
                next_url = request.GET.get("next", None)
                return Response({"data": serializer.data, "next_url": next_url}, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# login view
class Login(APIView):
    def post(self,request):
         # Check if user is already authenticated
        if request.user.is_authenticated:
            dashboard_url = reverse('dashboard')
            return Response({"redirect_url": dashboard_url}, status=status.HTTP_200_OK)
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                 # Provide next URL in JSON response to handle redirect on client
                next_url = request.GET.get("next", None)
                return Response({"message": "Login Successful", "next_url": next_url}, status=status.HTTP_200_OK)
            return Response({"Message":"Login Failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# logout view
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            logout(request)
            return Response({"Message":"Logout Successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# dashboard view
class Dashboard(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            profile = request.user.profile
            return Response({"Profile":profile.fullname}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# update view        
class UpdateProfile(APIView):
    permission_classes =[IsAuthenticated]
    def get(self,request):
        try:
            profile = request.user.profile
            serializer = UpdateProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self,request):
        try:
            profile = request.user.profile
            serializer = UpdateProfileSerializer(profile,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        