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


class SubCategoryNotNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategoryNotNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

