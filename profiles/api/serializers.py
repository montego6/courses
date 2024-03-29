from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.helpers import get_user_full_name
from ..models import TeacherProfile
from reviews.models import Review
from courses.models import Course
from courses.api.serializers import CourseSearchSerializer
from courses.utils import get_user_from_context

User = get_user_model()


class TeacherProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    
    class Meta:
        model = TeacherProfile
        fields = ['id', 'avatar', 'bio', 'name', 'rating', 'students', 'courses', 'balance']
        read_only_fields = ['balance', 'rating', 'students', 'courses', 'name']
    
    def get_name(self, obj):
        return get_user_full_name(obj.user)
    
    def get_rating(self, obj):
        agg = Review.objects.filter(course__author=obj.user).aggregate(Avg('rating'))['rating__avg']
        rating = round(agg, 2) if agg else 0
        return rating
    
    def get_students(self, obj):
        return User.objects.filter(student_courses__author=obj.user).distinct().count()
    
    def get_courses(self, obj):
        courses = Course.custom_objects.by_author(author=obj.user)
        return CourseSearchSerializer(courses, many=True).data
    
    def create(self, validated_data):
        validated_data['user'] = get_user_from_context(self.context)
        return super().create(validated_data)
