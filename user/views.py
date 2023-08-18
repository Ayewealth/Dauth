from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView


from .permissions import *
from user.models import *
from .serializers import *

# Create your views here.


class CourseCreateListApiView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsStudent]

    def perform_create(self, serializer):
        user = self.request.user
        if user.groups.filter(name='Instructor').exists():
            # Handle instructor's action
            serializer.save(instructor=user)
        elif user.groups.filter(name='Student').exists():
            # Handle student's action
            # Give an error message to students
            raise PermissionDenied("You are not allowed to create courses.")

        return super().perform_create(serializer)
