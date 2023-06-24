from rest_framework import serializers
from .models import Course, Section, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Section
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['author', 'students', 'date_created', 'date_updated']

    def create(self, validated_data):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        validated_data['author'] = user
        return super().create(validated_data)
    


