from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication

from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import (Quizzes, Questions, Play)
from .serializers import (QuizCreateSerializer, QuizListSerializer)
from .serializers import (QuestionCreateSerializer, QuestionListSerializer)
from .serializers import (PlayQuizSerializer, AllPlayListSerializer, UserPlayListSerializer, QuizAnalysisSerializer)

# Home View
class Home(generics.GenericAPIView):

    permission_classes = [IsAuthenticated,]
    authentication_classes = [BasicAuthentication, TokenAuthentication]

    def get(self, request):
        user = self.request.user
        if user.is_superuser:
            context = {
            'PROJECT NAME' : 'ONLINE QUIZE APP',
            'USER' : str(self.request.user),
            'USER PROFILE' : 'http://127.0.0.1:8000/profile/',
            'TOKEN GENERATION' : 'http://127.0.0.1:8000/token-generation/',
            'TOKEN REFRESH' : 'http://127.0.0.1:8000/token-refresh/',
            'TOKEN VERIFY' : 'http://127.0.0.1:8000/token-verify/',
            'CREATE USER' : 'http://127.0.0.1:8000/create-user/',
            'LIST USERS' : 'http://127.0.0.1:8000/list-user/',
            'UPDATE USER' : 'http://127.0.0.1:8000/update-user/<int:id>/',
            'DELETE USER' : 'http://127.0.0.1:8000/delete-user/<int:id>/',
            }
            
            return Response(context)
        else:
            context = {
            'PROJECT NAME' : 'ONLINE QUIZE APP',
            'USER' : str(self.request.user),
            'USER PROFILE' : 'http://127.0.0.1:8000/profile/',
            'TOKEN GENERATION' : 'http://127.0.0.1:8000/token-generation/',
            'TOKEN REFRESH' : 'http://127.0.0.1:8000/token-refresh/',
            'TOKEN VERIFY' : 'http://127.0.0.1:8000/token-verify/',
            }
            
            return Response(context)

# Quiz Creation view
class QuizCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Quizzes.objects.all()
    serializer_class = QuizCreateSerializer

# Quiz List view
class QuizListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Quizzes.objects.all()
    serializer_class = QuizListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ['title','category__name','date_created']

# Question Creation view
class QuestionCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Questions.objects.all()
    serializer_class = QuestionCreateSerializer
    
# Question List View  
class QuestionListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Questions.objects.all()
    serializer_class = QuestionListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['quiz__title','difficulty','date_created']
    search_fields = ['quiz__title','difficulty','date_created']
    
# Play Quiz
class PlayQuizView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Play.objects.all()
    serializer_class = PlayQuizSerializer

# All Playlist View
class AllPlayListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Play.objects.all()
    serializer_class = AllPlayListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ['quiz__title','score','available','date_played']

# user Playlist View
class UserPlayListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Play.objects.all()
    serializer_class = UserPlayListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ['quiz__title','score','available','date_played']


    def get_queryset(self):
        user = self.request.user
        queryset = Play.objects.filter(user_id=user.id)
        return queryset

# User total Score in quiz
class QuizAnalysisView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Play.objects.all()
    serializer_class = QuizAnalysisSerializer
  