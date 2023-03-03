from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import (Category,Quizzes, Questions, QuizPlay)

from .serializers import (CategorySerializer)
from .serializers import (QuizCreateSerializer, QuizListSerializer)
from .serializers import (QuestionCreateSerializer, QuestionListSerializer)
from .serializers import (PlayQuizSerializer, AllPlayListSerializer, UserPlayListSerializer)
from .serializers import QuizAnalysisSerializer
# Category Create View
class CategoryCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Category List View
class CategoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Quiz Creation view
class QuizCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quizzes.objects.all()
    serializer_class = QuizCreateSerializer

# Quiz List view
class QuizListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quizzes.objects.all()
    serializer_class = QuizListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ['title','category__name','date_created']


# Question Creation view
class QuestionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Questions.objects.all()
    serializer_class = QuestionCreateSerializer
    
# Question List View  
class QuestionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Questions.objects.all()
    serializer_class = QuestionListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['quiz__title','difficulty','date_created']
    search_fields = ['quiz__title','difficulty','date_created']
    

# Play Quiz View
class PlayQuizView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = QuizPlay.objects.all()
    serializer_class = PlayQuizSerializer

# All Playlist View
class AllPlayListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = QuizPlay.objects.all()
    serializer_class = AllPlayListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ['question__quiz__title','score','available','date_played']

# user Playlist View
class UserPlayListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = QuizPlay.objects.all()
    serializer_class = UserPlayListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ['question__quiz__title','score','available','date_played']

    def get_queryset(self):
        user = self.request.user
        queryset = QuizPlay.objects.filter(user_id=user.id)
        return queryset


# Quiz Availible View  
class AvailibelQuizListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, format=None):
        user = self.request.user
        
        questions = []
        for quiz in  Questions.objects.all():
            questions.append(quiz.id)
        
        playlist = []
        for play in QuizPlay.objects.filter(user=user.id):
            playlist.append(play.question.id)

        availible = list( set(questions) - set(playlist))
        
        context = {
            'All Quizes' : str(questions),
            'Played Quiz list' : str(playlist),
            'Availible Quizzes List': str(availible)}
        return Response(context)


class QuizAnalysisView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = QuizPlay.objects.all()
    serializer_class =QuizAnalysisSerializer
    
    def list(self, request, *args, **kwargs):
        user = self.request.user
        analysis = []
        quizzes = QuizPlay.objects.filter(user_id=user.id)
        if quizzes:
            for result in quizzes:
                questions = Questions.objects.filter(quiz_id=result.question.quiz.id).count()
                quiz = Quizzes.objects.filter(id=result.question.quiz.id)
                users = QuizPlay.objects.filter(question=result.question).count()

                total = QuizPlay.objects.filter(question_id=result.question.id).count()
                for q in quiz:
                    analysis.append({
                        "Quiz":q.title,
                        'Total Marks':result.score,
                        'Average Score' : result.score/result.attempt,
                        'No of time Quiz Taken' : result.attempt,
                        'Number of User attend the quiz' : total,
                        'Percantage of the user passed' : (users/total)*100
                                    })

        return Response({str(analysis)})
    