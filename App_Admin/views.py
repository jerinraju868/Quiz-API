from django.contrib.auth.models import User

from rest_framework import (generics, status)
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import (UserCreateSerializer, UserListSerializer, UserUpdateSerializer, UserDeleteSerializer)

#User Create View 
class UserCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]

    def create(self, request):
        user = UserCreateSerializer(data=self.request.data)
        if user.is_valid(raise_exception=True):
            user.save()
            context = {"Message":"Successfully User Created"}
            return Response(context, status=status.HTTP_201_CREATED)    
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
# User List View
class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    queryset =User.objects.all()
    serializer_class = UserListSerializer

# Update User View
class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

# Delete User View
class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer
