from rest_framework import serializers
from rest_framework.fields import empty
from .models import Course, Section, Lesson, AdditionalFile, SectionItem, Test, TestQuestion, Homework, CoursePayment
from .consts import COURSE_OPTIONS
from functools import reduce

# class SectionItemCreation:
#     def create(self, validated_data):
#         option = validated_data.pop('option', 'basic')
#         instance = self.Meta.model.objects.create(**validated_data)
#         SectionItem.objects.create(content_object=instance, section=instance.section, option=option)
#         return instance
    

# class ItemOptionSerializer(serializers.Serializer):
#     option = serializers.CharField(default='basic')

class SectionItemGetFieldsMixin(serializers.Serializer):
    def get_field_names(self, *args):
        payment_option = self.context.get('payment')
        is_author = self.context.get('is_author')
        payment_include = COURSE_OPTIONS.index(payment_option) < COURSE_OPTIONS.index(self.instance.option)
        if is_author or not (payment_option and payment_include):
            return super().get_field_names(*args)
        else:
            if isinstance(self.instance, Lesson):
                return ['id', 'name', 'description', 'duration', 'option', 'type']
            else:
                return ['id', 'name', 'description', 'option', 'type']



class LessonSerializer(SectionItemGetFieldsMixin, serializers.ModelSerializer):
    type = serializers.CharField(default='lesson', read_only=True)
    
    class Meta:
        model = Lesson
        fields = '__all__'


class AdditionalFileSerializer(SectionItemGetFieldsMixin, serializers.ModelSerializer):
    type = serializers.CharField(default='extra_file', read_only=True)

    class Meta:
        model = AdditionalFile
        fields = '__all__'


class TestQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TestQuestion
        fields = '__all__'


class TestSerializer(SectionItemGetFieldsMixin, serializers.ModelSerializer):
    type = serializers.CharField(default='test', read_only=True)
    questions = TestQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = '__all__'
        # fields = ['name', 'description', 'section', 'option', 'type', 'questions']


class HomeworkSerializer(SectionItemGetFieldsMixin, serializers.ModelSerializer):
    type = serializers.CharField(default='homework', read_only=True)

    class Meta:
        model = Homework
        fields = '__all__'


class SectionItemSerializer(serializers.Serializer):
    def to_representation(self, value):
        # user = None
        # request = self.context.get('request')
        # if request and hasattr(request, 'user'):
        #     user = request.user
        # course = value.section.course
        item = value.content_object
        # is_paid = CoursePayment.objects.filter(course=course, student=user).exists()
        # context = {}
        # context['payment'] = 'paid' if is_paid else 'free'
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


class SectionSerializer(serializers.ModelSerializer):
    # items = SectionItemSerializer(many=True, read_only=True)
    items = serializers.SerializerMethodField()
    
    class Meta:
        model = Section
        fields = '__all__'

    def get_items(self, obj):
        items = SectionItem.objects.filter(section=obj)
        serializer = SectionItemSerializer(items, many=True, read_only=True, context=self.context)
        return serializer.data

    # def __init__(self, instance=None, *args, **kwargs):
    #     super().__init__(instance, *args, **kwargs)
    #     self.fields['items'].context.update(self.context)


class CourseSerializer(serializers.ModelSerializer):
    # sections = SectionSerializer(many=True, read_only=True)
    sections = serializers.SerializerMethodField()

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
    
    def get_sections(self, obj):
        sections = Section.objects.filter(course=obj)
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        # is_paid = CoursePayment.objects.filter(course=obj, student=user).exists()
        context = {}
        try:
            payment = CoursePayment.objects.get(course=obj, student=user)
        except CoursePayment.DoesNotExist:
            context['payment'] = 'free'
        else:
            context['payment'] = payment.option
        context['is_author'] = user == obj.author
        # context['payment'] = payment.option if payment.exists() else 'free'
        serializer = SectionSerializer(sections, many=True, read_only=True, context=context)
        return serializer.data
    

class CourseSearchSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['name', 'cover', 'short_description', 'author', 'price', 'language', 'duration', 'options']

    def get_duration(self, obj):
        lessons = Lesson.objects.filter(section__course=obj)
        duration = reduce(lambda x,y: x+y.duration, lessons, lessons[0].duration)
        return duration
    
    def get_options(self, obj):
        options_set = set()
        for course_option in obj.options:
            content = course_option.get("content", [])
            options_set.update(content)
        return list(options_set)


class CourseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'cover', 'short_description', 'price']


class CourseItemPaymentSerializer(serializers.ModelSerializer):
    price = serializers.CharField(source='stripe.price')
    quantity = serializers.IntegerField(default=1, initial=1)

    class Meta:
        model = Course
        fields = ('price', 'quantity')
    


