from rest_framework import serializers

from categories.models import Category, SubCategory, Subject
from courses.models import Course


class StatisticsSerializer(serializers.Serializer):
    courses = serializers.IntegerField()
    payments = serializers.DecimalField(max_digits=15, decimal_places=2)
    students = serializers.IntegerField()
    authors = serializers.IntegerField()
    cur_month_payments = serializers.DecimalField(max_digits=15, decimal_places=2)


class CategoryStatisticsSerializer(serializers.ModelSerializer, StatisticsSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'courses', 'payments', 'students', 'authors', 'cur_month_payments']


class SubCategoryStatisticsSerializer(serializers.ModelSerializer, StatisticsSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'courses', 'payments', 'students', 'authors', 'cur_month_payments']


class SubjectStatisticsSerializer(serializers.ModelSerializer, StatisticsSerializer):
    courses_num = courses = serializers.IntegerField()
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'courses_num', 'payments', 'students', 'authors', 'cur_month_payments']


class CourseStatisticsSerializer(serializers.ModelSerializer):
    num_reviews = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_payments = serializers.DecimalField(max_digits=15, decimal_places=2)
    cur_month_payments = serializers.DecimalField(max_digits=15, decimal_places=2)
    num_students = serializers.IntegerField()

    class Meta:
        model = Course
        fields = ['slug', 'name', 'num_reviews', 'rating', 'total_payments', 'cur_month_payments', 'num_students']