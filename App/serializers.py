from rest_framework import serializers
from .models import Quizzes,  Questions,Play
from rest_framework.response import Response

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
        fields = ['id','user','quiz','difficulty','question','option_one','option_two','option_three','correct_answer','availible','date_created']

    def to_representation(self, instance):
        rep = super(QuestionListSerializer, self).to_representation(instance)
        # rep['quiz'] = instance.quiz.title
        rep['user'] = instance.quiz.user.username
        return rep
    

# Play Quiz Serializer
class PlayQuizSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(read_only=True)
    class Meta:
        model = Play
        fields = ['quiz', 'question','answered','score']


    def create(self, validated_data):
        user = self.context['request'].user  
        quiz = self.validated_data['quiz']
        question = self.validated_data['question']
        score = self.validated_data.pop('score', None)
        if Questions.objects.filter(quiz=quiz, question=question):
            if Play.objects.filter(question=question,user=user).exists():
                raise serializers.ValidationError({"Error":"Already answered this question"})
            else:
                if self.validated_data['answered'] == question.correct_answer:
                    score = 1
                    play = Play.objects.create(**validated_data,score=score,user=user)
                    play.save()
                    return play
                else:
                    play = Play.objects.create(**validated_data,user=user)
                    play.save()
                    return play
        else:
            raise serializers.ValidationError({"Error":"Question is not found in corresponding quiz."})

        
# All play list serializer   
class AllPlayListSerializer(serializers.ModelSerializer):
    correct_answer = serializers.ReadOnlyField()
    class Meta:
        model = Play
        fields = ['user', 'quiz','score','question','answered','correct_answer',]
    
    def to_representation(self, instance):
        rep = super(AllPlayListSerializer, self).to_representation(instance)
        rep['user'] = instance.user.username
        rep['question'] = instance.question.question
        rep['quiz'] = instance.question.quiz.title
        rep['correct_answer'] = instance.question.correct_answer
        return rep
    
    def validate(self, data):
        if data.answered == data.question.correct_answer:
            data.score += 1
        return data

# User Play list Serializer 
class UserPlayListSerializer(serializers.ModelSerializer):
    correct_answer = serializers.ReadOnlyField()

    class Meta:
        model = Play
        fields = [ 'quiz','score','question','answered','correct_answer',]
    
    def to_representation(self, instance):
        rep = super(UserPlayListSerializer, self).to_representation(instance)
        rep['question'] = instance.question.question
        rep['quiz'] = instance.question.quiz.title
        rep['correct_answer'] = instance.question.correct_answer
        return rep


# Quiz Analysis
class QuizAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ['quiz','score']
    
    def to_representation(self, instance):
        rep = super(QuizAnalysisSerializer, self).to_representation(instance)
        rep['quiz'] = instance.quiz.title
        return rep