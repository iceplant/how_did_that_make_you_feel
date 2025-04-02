from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
 
# import view sets from the REST framework
from rest_framework import viewsets, permissions, status
 
# import the TodoSerializer from the serializer file
from .serializers import EntrySerializer, UserRegisterSerializer, UserLoginSerializer, UserSerializer
 
# import the Todo model from the models file
from .models import Entry
import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response 


# from django.views.decorators.csrf import csrf_exempt


from .validations import custom_validation, validate_email, validate_password

# create a class for the Todo model viewsets
# @csrf_exempt
class EntryView(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        # Return only entries belonging to the logged-in user
        return Entry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the logged-in user with the new entry
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # Ensure the logged-in user is the owner of the entry
        entry = self.get_object()
        if entry.user != request.user:
            raise PermissionDenied("You do not have permission to update this entry.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Ensure the logged-in user is the owner of the entry
        entry = self.get_object()
        if entry.user != request.user:
            raise PermissionDenied("You do not have permission to delete this entry.")
        return super().destroy(request, *args, **kwargs)

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            clean_data = custom_validation(request.data)
            serializer = UserRegisterSerializer(data=clean_data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.create(clean_data)
                if user:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            if user is None:  # Handle invalid credentials
                print("User is none!!!")
                return Response(
                    {"error": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)
class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF cookie set"})


