from rest_framework import serializers
from .models import Course, Section, Lesson, AdditionalFile, SectionItem


class LessonSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='lesson', read_only=True)
    
    class Meta:
        model = Lesson
        fields = '__all__'


class AdditionalFileSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='extra_file', read_only=True)

    class Meta:
        model = AdditionalFile
        fields = '__all__'


# class SectionItemRelatedField(serializers.RelatedField):
#     def to_representation(self, value):
#         if isinstance(value, Lesson):
#             serializer = LessonSerializer(value)
#         elif isinstance(value, AdditionalFile):
#             serializer = AdditionalFileSerializer(value)
#         else:
#             raise Exception('Unexpected type of section item')
#         return serializer.data


class SectionItemSerializer(serializers.Serializer):
    def to_representation(self, value):
        item = value.content_object
        if isinstance(item, Lesson):
            serializer = LessonSerializer(item)
        elif isinstance(item, AdditionalFile):
            serializer = AdditionalFileSerializer(item)
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
    


