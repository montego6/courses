from rest_framework import serializers
from .models import Course, Section, Lesson, AdditionalFile, SectionItem, Test, TestQuestion, Homework


class SectionItemCreation:
    def create(self, validated_data):
        option = validated_data.pop('option', 'basic')
        instance = self.Meta.model.objects.create(**validated_data)
        SectionItem.objects.create(content_object=instance, section=instance.section, option=option)
        return instance
    

class ItemOptionSerializer(serializers.Serializer):
    option = serializers.CharField(default='basic')


class LessonSerializer(SectionItemCreation, ItemOptionSerializer, serializers.ModelSerializer):
    type = serializers.CharField(default='lesson', read_only=True)
    
    class Meta:
        model = Lesson
        fields = '__all__'


class AdditionalFileSerializer(SectionItemCreation, ItemOptionSerializer, serializers.ModelSerializer):
    type = serializers.CharField(default='extra_file', read_only=True)

    class Meta:
        model = AdditionalFile
        fields = '__all__'


class TestQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TestQuestion
        fields = '__all__'


class TestSerializer(SectionItemCreation, ItemOptionSerializer, serializers.ModelSerializer):
    type = serializers.CharField(default='test', read_only=True)
    questions = TestQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = '__all__'


class HomeworkSerializer(SectionItemCreation, ItemOptionSerializer, serializers.ModelSerializer):
    type = serializers.CharField(default='homework', read_only=True)

    class Meta:
        model = Homework
        fields = '__all__'




class SectionItemSerializer(serializers.Serializer):
    def to_representation(self, value):
        item = value.content_object
        if isinstance(item, Lesson):
            serializer = LessonSerializer(item)
        elif isinstance(item, AdditionalFile):
            serializer = AdditionalFileSerializer(item)
        elif isinstance(item, Test):
            serializer = TestSerializer(item)
        elif isinstance(item, Homework):
            serializer = HomeworkSerializer(item)        
        else:
            raise Exception('Unexpected type of section item')
        return serializer.data


# class SectionItemSerializer(serializers.ModelSerializer):
#     content_object = SectionItemRelatedField(read_only=True)

#     class Meta:
#         model = SectionItem
#         fields = ['content_object']
    

class SectionSerializer(serializers.ModelSerializer):
    items = SectionItemSerializer(many=True, read_only=True)
    
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
    


