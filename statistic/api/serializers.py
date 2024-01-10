from rest_framework import serializers

from categories.models import Category, SubCategory, Subject


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
