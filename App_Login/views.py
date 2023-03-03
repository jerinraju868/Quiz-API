from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from App.models import Quizzes

from rest_framework.response import Response
from rest_framework import (generics, status)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from rest_framework_simplejwt.tokens import (RefreshToken, OutstandingToken, BlacklistedToken)
from rest_framework.authentication import (BasicAuthentication, SessionAuthentication, TokenAuthentication)

from .serializers import (RegisterSerializer, LoginSerializer)

# User Register View
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request):
        user = RegisterSerializer(data=self.request.data)
        if user.is_valid(raise_exception=True):
            user.save()
            context = {"Message":"Registration Succesfull. Please generate token to login."}
            return Response(context, status=status.HTTP_201_CREATED)    
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"status": status.HTTP_200_OK, "Token": token.key})

# Profile View for the current user
class ProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, format=None):
        user = self.request.user
        quizes = []
        for quiz in  Quizzes.objects.filter(user_id=user.id):
            quizes.append(quiz.title)
      
        context = {
            'User' : str(self.request.user), # current login username
            'Email' :str(self.request.user.email), # email of the current user
            'Quize List' : str(quizes),
        }
        return Response(context)
    
# Custom Token Generate
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'user_id': user.pk,'email': user.email, 'username':user.username})

# Logout View
class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# Logoutall VIew
class LogoutAllView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)

