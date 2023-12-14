from rest_framework import serializers

from .models import Category, SubCategory, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'


# class SubCategoryNotNestedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SubCategory
#         fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


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
    class Meta:
        model = Subject
        fields = ['id', 'name', 'courses', 'payments', 'students', 'authors', 'cur_month_payments']

