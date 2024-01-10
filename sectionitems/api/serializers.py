from django.forms import ValidationError
from rest_framework import serializers
from core.consts import EXCLUDE_FIELDS

from courses.blogic import get_test_completion_result, get_user_from_context, has_user_full_access
from sectionitems.models import AdditionalFile, Homework, Lesson, Test, TestCompletion, TestQuestion


class SectionItemExcludeFieldsMixin(serializers.Serializer):
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
        item = value.content_object
        context = self.context
        if isinstance(item, Lesson):
            serializer = LessonSerializer(item, context=context)
        elif isinstance(item, AdditionalFile):
            serializer = AdditionalFileSerializer(item, context=context)
        elif isinstance(item, Test):
            serializer = TestSerializer(item, context=context)
        elif isinstance(item, Homework):
            serializer = HomeworkSerializer(item, context=context)        
        else:
            raise Exception('Unexpected type of section item')
        return serializer.data