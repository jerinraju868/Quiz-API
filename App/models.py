from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['id']
        
    name = models.CharField(max_length=500, verbose_name='Category Name', unique=True)
    
    def __str__(self):
        return self.name

class Quizzes(models.Model):
    class Meta:
        # verbose_name = 'Quiz'
        # verbose_name_plural = 'Quizzes'
        ordering = ['id']

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Created by')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Category')
    title = models.CharField(max_length=500, verbose_name='Quiz title', unique=True) 
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Questions(models.Model):
    class Meta:
        # verbose_name = 'Question'
        # verbose_name_plural = 'Questions'
        ordering = ['id']

    quiz = models.ForeignKey(Quizzes, on_delete=models.DO_NOTHING, verbose_name='Quiz Title')
    difficulty = models.IntegerField(choices=((1,'Beginner'),(2,'Intermediate'),(3,'Advance'),(4,'Expert')), default=1, verbose_name='Difficulty')
    question = models.CharField(max_length=1000, verbose_name='Question', unique=True)
    option_one = models.CharField(max_length=250,verbose_name='Option 1')
    option_two = models.CharField(max_length=250,verbose_name='Option 2')
    option_three = models.CharField(max_length=250,verbose_name='Option 3', blank=True)
    correct_answer = models.CharField(max_length=250)
    availible = models.BooleanField(default=True, verbose_name='Availible')
    date_created = models.DateField(auto_now_add=True, verbose_name='Created at')
    date_updated = models.DateField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return self.question

class Play(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    quiz = models.ForeignKey(Quizzes,on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Questions,on_delete=models.DO_NOTHING)
    answered = models.CharField(max_length=250)
    score = models.IntegerField(default=0, verbose_name='Current Score')
    available = models.IntegerField(default=0)
    average = models.FloatField(default=0)
    attempts = models.IntegerField(default=1)
    percentage = models.FloatField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.user.username
