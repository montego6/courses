from django.forms import ValidationError
from rest_framework import serializers
from core.consts import EXCLUDE_FIELDS

from courses.utils import  get_user_from_context
from ..utils import get_test_completion_result, has_user_full_access
from sectionitems.models import AdditionalFile, Homework, Lesson, Test, TestCompletion, TestQuestion


class SectionItemExcludeFieldsMixin():
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        if not has_user_full_access(self.context, instance):
            for field in EXCLUDE_FIELDS:
                if field in data:
                    data.pop(field)
        return data



class LessonSerializer(SectionItemExcludeFieldsMixin, serializers.ModelSerializer):
    type = serializers.CharField(default='lesson', read_only=True)
    
    class Meta:
        model = Lesson
        fields = '__all__'


class AdditionalFileSerializer(SectionItemExcludeFieldsMixin, serializers.ModelSerializer):
    type = serializers.CharField(default='extra_file', read_only=True)

    class Meta:
        model = AdditionalFile
        fields = '__all__'


class TestQuestionSerializer(serializers.ModelSerializer):
    __test__ = False
    
    class Meta:
        model = TestQuestion
        fields = '__all__'


class TestSerializer(SectionItemExcludeFieldsMixin, serializers.ModelSerializer):
    __test__ = False
    type = serializers.CharField(default='test', read_only=True)
    questions = TestQuestionSerializer(many=True, read_only=True)
    completed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Test
        fields = '__all__'
    
    def get_completed(self, obj):
        return get_test_completion_result(self.context, obj)
    

class TestCompletionSerializer(serializers.ModelSerializer):
    __test__ = False
    
    class Meta:
        model = TestCompletion
        fields = ['id', 'test', 'result']
        read_only_fields = ['student']
    
    def create(self, validated_data):
        user = get_user_from_context(self.context)
        if user:
            validated_data['student'] = user
            return super().create(validated_data)
        else:
            raise ValidationError('User should be logged in')

class HomeworkSerializer(SectionItemExcludeFieldsMixin, serializers.ModelSerializer):
    type = serializers.CharField(default='homework', read_only=True)

    class Meta:
        model = Homework
        fields = '__all__'



class SectionItemSerializer(serializers.Serializer):
    def to_representation(self, value):
        context = self.context
        if value.lesson:
            serializer = LessonSerializer(value.lesson, context=context)
        elif value.additional_file:
            serializer = AdditionalFileSerializer(value.additional_file, context=context)
        elif value.test:
            serializer = TestSerializer(value.test, context=context)
        elif value.homework:
            serializer = HomeworkSerializer(value.homework, context=context)        
        return serializer.data