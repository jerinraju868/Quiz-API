from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create User Serializer
class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    class Meta:
        model = User
        fields = ['email','password',]
        extra_kwargs = {'email':{'required':True}, 'password':{'write_only':True, 'required':True}
            }

    def create(self, validated_data):
        email = self.validated_data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exist. Try another one')
        else:
            user = User(email=email, username=email)
            password =  self.validated_data['password']
            user.set_password(password)
            user.save()
            return user
    
# User List Serializer
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'date_joined', 'last_login', 'is_superuser']

# Update User Serializer
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',  'password',]
        extra_kwargs = {'password':{'write_only':True}}

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

# Delete User Serializer
class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '_all__'