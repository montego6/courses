from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from courses.blogic import ExtraContext, get_test_completion_result, get_user_from_context, has_user_full_access, make_payment_context
from .models import Course, Section, Lesson, AdditionalFile, SectionItem, Test, TestQuestion, Homework, TestCompletion
from .consts import EXCLUDE_FIELDS
from reviews.serializers import ReviewWithFullNameSerializer
from reviews.models import Review
from functools import reduce




User = get_user_model()



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
        validated_data['author'] = get_user_from_context(self.context)
        return super().create(validated_data)
    
    def get_sections(self, obj):
        sections = Section.objects.filter(course=obj)
        user = get_user_from_context(self.context)
        context = make_payment_context(obj, user)
        context = ExtraContext(context, user, obj).update_context()
        serializer = SectionSerializer(sections, many=True, read_only=True, context=context)
        return serializer.data
    

class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name']
        read_only_fields = ['id', 'name']

    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name


class CourseSearchSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    subject = serializers.SlugRelatedField(slug_field='name', read_only=True)
    rating = serializers.SerializerMethodField()
    author = AuthorSerializer()
    students = serializers.IntegerField(source='students.count')
    cover = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'cover', 'short_description', 'author', 'price', 'language', 'duration', 'options', 'subject', 'rating', 'students']
        read_only_fields = ['id', 'name', 'cover', 'short_description', 'author', 'price', 'language', 'duration', 'options', 'subject', 'rating', 'students']

    def get_duration(self, obj):
        lessons = Lesson.objects.filter(section__course=obj)
        duration = reduce(lambda x,y: x+y.duration, lessons, lessons[0].duration) if lessons else 0
        return duration
    
    def get_options(self, obj):
        options_set = set()
        for course_option in obj.options:
            content = course_option.get("content", [])
            options_set.update(content)
        return list(options_set)
    
    def get_rating(self, obj):
        return round(Review.objects.filter(course=obj).aggregate(Avg('rating', default=0))['rating__avg'], 2)
    

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
    


