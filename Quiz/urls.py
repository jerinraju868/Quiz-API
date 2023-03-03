from django.contrib import admin
from django.urls import path

from App_Admin.views import (UserCreateView, UserListView, UserUpdateView, UserDeleteView)
from App_Login.views import (RegisterView, LoginView,CustomAuthToken, ProfileView, LogoutView, LogoutAllView)
from App.views import (CategoryCreateView, CategoryListView, QuizCreateView, QuizListView ,QuestionCreateView, QuestionListView)
from App.views import (PlayQuizView, AllPlayListView, UserPlayListView, QuizAnalysisView, AvailibelQuizListView)

from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenVerifyView)


urlpatterns = [

    # Quiz CRUD related urls
    # path('',Home.as_view()),

    path('category-create/', CategoryCreateView.as_view()),
    path('category-list/', CategoryListView.as_view()),

    path('quiz-create/', QuizCreateView.as_view()),
    path('quiz-list/', QuizListView.as_view()),

    path('question-create/', QuestionCreateView.as_view()),
    path('question-list/', QuestionListView.as_view()),
    
    path('quiz-play/',PlayQuizView.as_view()),
    path('all-playlist/',AllPlayListView.as_view()),
    path('my-playlist/',UserPlayListView.as_view()),
    path('quiz-availible/',AvailibelQuizListView.as_view()),
    
    path('quiz-analysis/',QuizAnalysisView.as_view()),

    # Admin Page 
    path('admin/', admin.site.urls),

    # User CRUD related url paths
    path('user-create/', UserCreateView.as_view()),
    path('user-list/', UserListView.as_view()),
    path('user-update/<int:pk>/',UserUpdateView.as_view()),
    path('user-delete/<int:pk>/',UserDeleteView.as_view()),

    # User related url paths
    path('register/',RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('custom-token/', CustomAuthToken.as_view()),
    path('', ProfileView.as_view()),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout-all'),


    path('token-generate/', TokenObtainPairView.as_view(), name='token-generate'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token-refresh/',TokenRefreshView.as_view(), name='token-refresh'),

    ]
