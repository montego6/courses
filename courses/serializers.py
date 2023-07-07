from rest_framework import serializers
from .models import Course, Section, Lesson, AdditionalFile, SectionItem, Test, TestQuestion, Homework, CoursePayment


# class SectionItemCreation:
#     def create(self, validated_data):
#         option = validated_data.pop('option', 'basic')
#         instance = self.Meta.model.objects.create(**validated_data)
#         SectionItem.objects.create(content_object=instance, section=instance.section, option=option)
#         return instance
    

# class ItemOptionSerializer(serializers.Serializer):
#     option = serializers.CharField(default='basic')

class SectionItemFreeSerializer(serializers.Serializer):
    def get_field_names(self, *args):
        payment_option = self.context.get('payment')
        if payment_option == 'free':
            return ['name', 'description', 'option', 'type']
        else:
            return super().get_field_names(*args)


class LessonSerializer(SectionItemFreeSerializer, serializers.ModelSerializer):
    type = serializers.CharField(default='lesson', read_only=True)
    
    class Meta:
        model = Lesson
        fields = '__all__'


class AdditionalFileSerializer(SectionItemFreeSerializer, serializers.ModelSerializer):
    type = serializers.CharField(default='extra_file', read_only=True)

    class Meta:
        model = AdditionalFile
        fields = '__all__'


class TestQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TestQuestion
        fields = '__all__'


class TestSerializer(SectionItemFreeSerializer, serializers.ModelSerializer):
    type = serializers.CharField(default='test', read_only=True)
    questions = TestQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = '__all__'
        # fields = ['name', 'description', 'section', 'option', 'type', 'questions']


class HomeworkSerializer(SectionItemFreeSerializer, serializers.ModelSerializer):
    type = serializers.CharField(default='homework', read_only=True)

    class Meta:
        model = Homework
        fields = '__all__'


class SectionItemSerializer(serializers.Serializer):
    def to_representation(self, value):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        course = value.section.course
        is_paid = CoursePayment.objects.filter(course=course, student=user).exists()
        item = value.content_object
        context = {}
        context['payment'] = 'paid' if is_paid else 'free'
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
    

class CoursePaymentSerializer(serializers.ModelSerializer):
    price = serializers.CharField(source='stripe.price')
    quantity = serializers.IntegerField(default=1, initial=1)

    class Meta:
        model = Course
        fields = ('price', 'quantity')
    


