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

    def category(sefl, obj):
        return obj.category.id


@admin.register(models.Questions)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['quiz', 'difficulty','question','option_one','option_two','option_three','correct_answer','availible']
    list_display = ['id','question','quiz_id','category', 'difficulty','option_one','option_two','option_three','correct_answer','availible', 'date_created']

    def category(self, obj):
        return obj.quiz.category.id
    
@admin.register(models.Play)
class PlayAdmin(admin.ModelAdmin):
    fields = ['user', 'quiz','question','answered',]
    list_display = ['user_id', 'quiz_id','question_id','answered','score','available','average','attempts','percentage','date_played']


