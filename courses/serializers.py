from email.policy import default
from django.db.models import Avg
from numpy import source
from rest_framework import serializers
from rest_framework.fields import empty
from django.contrib.auth import get_user_model
from .models import Course, Section, Lesson, AdditionalFile, SectionItem, Test, TestQuestion, Homework, CoursePayment, TestCompletion
from .consts import COURSE_OPTIONS
from reviews.serializers import ReviewWithFullNameSerializer
from reviews.models import Review
from functools import reduce


User = get_user_model()



class SectionItemGetFieldsMixin(serializers.Serializer):
    def get_field_names(self, *args):
        payment_option = self.context.get('payment')
        is_author = self.context.get('is_author')
        if is_author or not (payment_option and COURSE_OPTIONS.index(payment_option) < COURSE_OPTIONS.index(self.instance.option)):
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
    completed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Test
        fields = '__all__'
    
    def get_completed(self, obj):
        user = self.context.get('user')
        try:
            test_completion = TestCompletion.objects.get(test=obj, student=user)
        except TestCompletion.DoesNotExist:
            return False
        else:
            return test_completion.result
        # return TestCompletion.objects.filter(test=obj, student=user).exists()
    

class TestCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCompletion
        fields = ['test', 'result']
        read_only_fields = ['student']
    
    def create(self, validated_data):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        validated_data['student'] = user
        return super().create(validated_data)


class HomeworkSerializer(SectionItemGetFieldsMixin, serializers.ModelSerializer):
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


class SectionSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    
    class Meta:
        model = Section
        fields = '__all__'

    def get_items(self, obj):
        items = SectionItem.objects.filter(section=obj)
        serializer = SectionItemSerializer(items, many=True, read_only=True, context=self.context)
        return serializer.data



class CourseSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()
    reviews = ReviewWithFullNameSerializer(many=True, read_only=True)

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
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if not isinstance(user, User):
            user = None
        context = {}
        try:
            payment = CoursePayment.objects.get(course=obj, student=user)
        except CoursePayment.DoesNotExist:
            context['payment'] = 'free'
        else:
            context['payment'] = payment.option
        context['is_author'] = user == obj.author
        context['user']  = user
        serializer = SectionSerializer(sections, many=True, read_only=True, context=context)
        return serializer.data
    

class CourseSearchSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    subject = serializers.SlugRelatedField(slug_field='name', read_only=True)
    rating = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    students = serializers.IntegerField(source='students.count', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'cover', 'short_description', 'author', 'price', 'language', 'duration', 'options', 'subject', 'rating', 'students']

    def get_duration(self, obj):
        lessons = Lesson.objects.filter(section__course=obj)
        print(lessons)
        duration = reduce(lambda x,y: x+y.duration, lessons, lessons[0].duration)
        return duration
    
    def get_options(self, obj):
        options_set = set()
        for course_option in obj.options:
            content = course_option.get("content", [])
            options_set.update(content)
        return list(options_set)
    
    def get_rating(self, obj):
        return round(Review.objects.filter(course=obj).aggregate(Avg('rating', default=0))['rating__avg'], 2)
    
    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'name': obj.author.first_name + ' ' + obj.author.last_name
        }


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
    


