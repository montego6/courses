from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TeacherProfile
from reviews.models import Review

User = get_user_model()


class TeacherProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    
    class Meta:
        model = TeacherProfile
        fields = ['avatar', 'bio', 'name', 'rating', 'students']
        read_only_fields = ['balance']
    
    def get_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    
    def get_rating(self, obj):
        return round(Review.objects.filter(course__author=obj.user).aggregate(Avg('rating'))['rating__avg'], 2)
    
    def get_students(self, obj):
        return User.objects.filter(student_courses__author=obj.user).distinct().count()
    
    def create(self, validated_data):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        validated_data['user'] = user
        return super().create(validated_data)
