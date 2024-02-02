from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.helpers import get_user_full_name

from courses.utils import ExtraContext, get_user_from_context, make_payment_context
from sectionitems.api.serializers import SectionItemSerializer
from sectionitems.models import Lesson, SectionItem
from ..models import Course, CoursePrice, Section
from reviews.api.serializers import ReviewWithFullNameSerializer
from reviews.models import Review
from functools import reduce




User = get_user_model()






class SectionSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    course = serializers.SlugRelatedField(slug_field='slug', queryset=Course.objects.all())
    
    class Meta:
        model = Section
        fields = ['id', 'name', 'description', 'course', 'items']

    def get_items(self, obj):
        items = SectionItem.objects.filter(section=obj)
        serializer = SectionItemSerializer(items, many=True, read_only=True, context=self.context)
        return serializer.data



class CourseSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()
    reviews = ReviewWithFullNameSerializer(many=True, read_only=True)
    options = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'short_description', 'full_description', 'author', 'cover', 
                  'language', 'what_will_learn', 'requirements', 'students', 
                  'date_created', 'date_updated', 'is_published', 
                  'is_free', 'subject', 'sections', 'reviews', 'slug', 'options']
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
    
    def get_options(self, obj):
        options = []
        prices = CoursePrice.objects.filter(course=obj).order_by('amount')
        for price in prices:
            option = {
                'option': price.option,
                'amount': price.amount
            }
            options.append(option)
        return options
    


    

class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name']
        read_only_fields = ['id', 'name']

    def get_name(self, obj):
        return get_user_full_name(obj)


class CourseSearchSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    # options = serializers.SerializerMethodField()
    subject = serializers.SlugRelatedField(slug_field='name', read_only=True)
    rating = serializers.SerializerMethodField()
    author = AuthorSerializer()
    students = serializers.IntegerField(source='students.count')
    cover = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'cover', 'short_description', 'author', 'language', 'duration', 'subject', 'rating', 'students']
        read_only_fields = ['id', 'name', 'cover', 'short_description', 'author', 'language', 'duration', 'subject', 'rating', 'students']

    def get_duration(self, obj):
        lessons = Lesson.objects.filter(section__course=obj)
        duration = reduce(lambda x,y: x+y.duration, lessons, lessons[0].duration) if lessons else 0
        return duration
    
    # def get_options(self, obj):
    #     options_set = set()
    #     for course_option in obj.options:
    #         content = course_option.get("content", [])
    #         options_set.update(content)
    #     return sorted(list(options_set))
    
    def get_rating(self, obj):
        return round(Review.objects.filter(course=obj).aggregate(Avg('rating', default=0))['rating__avg'], 2)
    

class CourseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'cover', 'short_description']


class CourseItemPaymentSerializer(serializers.ModelSerializer):
    price = serializers.CharField(source='stripe.price')
    quantity = serializers.IntegerField(default=1, initial=1)

    class Meta:
        model = Course
        fields = ('price', 'quantity')
    

class CoursePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePrice
        fields = ('course', 'amount', 'option')

