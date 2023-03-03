from django.contrib import admin
from .  import models

@admin.register(models.Category)
class CatAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['id', 'name']

@admin.register(models.Quizzes)
class QuizAdmin(admin.ModelAdmin):
    fields = ['user', 'category','title',]
    list_display = ['id', 'title','category_id','user_id']
 
@admin.register(models.Questions)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['quiz', 'difficulty','question','option_one','option_two','option_three','correct_answer',]
    list_display = ['id','question','quiz_id', 'difficulty','option_one','option_two','option_three','correct_answer', 'date_created']
    
@admin.register(models.QuizPlay)
class PlayAdmin(admin.ModelAdmin):
    fields = ['user', 'question','answered',]
    list_display = ['user_id','question_id','answered','score','attempt','date_played']


