from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

# User Registration
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    class Meta:
        model = User
        fields = ['email','password']
        extra_kwargs = {'email':{'required':True},'password':{'write_only':True, 'required':True}}
    
    def create(self, validated_data):
        email = self.validated_data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already taken. Please try another one")
        else:
            user = User.objects.create(email=email, username=email)
            user.set_password(validated_data['password'])
            user.save()
            return user

# User login
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(label=_("Password"),style={'input_type': 'password'},trim_whitespace=False,max_length=128,write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),username=email, password=password)
            if not user:
                raise serializers.ValidationError("login failed", code='authorization')
        else:
            raise serializers.ValidationError("Username and Password required", code='authorization')
        data['user'] = user
        return data