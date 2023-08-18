from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserDeleteSerializer

from .models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = [
            'id',
            'name',
            'email',
            'password',
            'is_instructor',
            'is_student',
        ]


class CourseSerializer(ModelSerializer):
    instructor = serializers.CharField(
        source='instructor.name', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'what_you_learn',
            'requirements',
            'description',
            'targeted_audience',
            'instructor',
            'price',
            'duration_in_hours',
        ]
