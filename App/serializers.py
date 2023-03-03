from rest_framework import serializers
from .models import Category, Quizzes,  Questions,QuizPlay
from django.db.models import Avg, Sum
from rest_framework.response import Response

# Category serialiser
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


# Quiz Create Serializer
class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizzes
        fields = ['category', 'title']

    def create(self, validated_data):
        user = self.context['request'].user
        quiz = Quizzes.objects.create(user=user, **validated_data)
        return quiz

# Quiz List Serializer      
class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizzes
        fields = ['id','category', 'title','user']
    
    def to_representation(self, instance):
        rep = super(QuizListSerializer, self).to_representation(instance)
        rep['user'] = instance.user.username
        # rep['category'] = instance.category.name
        return rep


# Question Create Serializer
class QuestionCreateSerializer(serializers.ModelSerializer):
    difficulty = serializers.ChoiceField(choices=((1,'Beginner'),(2,'Intermediate'),(3,'Advance'),(4,'Expert')))
    class Meta:
        model = Questions
        fields = ['quiz','difficulty', 'question', 'option_one', 'option_two', 'option_three', 'correct_answer']

    def create(self, validated_data):
        question = Questions.objects.create(**validated_data)
        question.save()
        return question

# Question List Serializer
class QuestionListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField()
    class Meta:
        model = Questions
        fields = ['id','user','quiz','difficulty','question','option_one','option_two','option_three','correct_answer','date_created']

    def to_representation(self, instance):
        rep = super(QuestionListSerializer, self).to_representation(instance)
        # rep['quiz'] = instance.quiz.title
        rep['user'] = instance.quiz.user.username
        return rep
    

# Play Quiz Serializer
class PlayQuizSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(read_only=True)
    class Meta:
        model = QuizPlay
        fields = ['question','answered','score']

    def create(self, validated_data):
        user = self.context['request'].user  
        question = self.validated_data['question']
        score = self.validated_data.pop('score', None)
        if Questions.objects.filter(question=question):
            if QuizPlay.objects.filter(question=question,user=user).exists():
                raise serializers.ValidationError({"Error":"Already answered this question"})
            else:
                if self.validated_data['answered'] == question.correct_answer:
                    score = 1
                    play = QuizPlay.objects.create(**validated_data,score=score,user=user)
                    play.save()
                    return play
                else:
                    play = QuizPlay.objects.create(**validated_data,user=user)
                    play.save()
                    return play
        else:
            raise serializers.ValidationError({"Error":"Question is not found in corresponding quiz."})

        
# All play list serializer   
class AllPlayListSerializer(serializers.ModelSerializer):
    correct_answer = serializers.ReadOnlyField()
    class Meta:
        model = QuizPlay
        fields = ['user', 'score','question','answered','correct_answer',]
    
    def to_representation(self, instance):
        rep = super(AllPlayListSerializer, self).to_representation(instance)
        rep['user'] = instance.user.username
        rep['question'] = instance.question.question
        rep['correct_answer'] = instance.question.correct_answer
        return rep

# User Play list Serializer 
class UserPlayListSerializer(serializers.ModelSerializer):
    correct_answer = serializers.ReadOnlyField()
    class Meta:
        model = QuizPlay
        fields = ['score','question','answered','correct_answer',]
    
    def to_representation(self, instance):
        rep = super(UserPlayListSerializer, self).to_representation(instance)
        rep['question'] = instance.question.question
        rep['correct_answer'] = instance.question.correct_answer
        return rep


class QuizAnalysisSerializer(serializers.ModelSerializer):
    # percentage = serializers.SerializerMethodField()
    class Meta:
        model = QuizPlay
        fields = ['question', 'score', 'attempt']



