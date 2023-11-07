from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewWithFullNameSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    def get_student(self, obj):
        return obj.student.first_name + " " + obj.student.last_name
    
    class Meta:
        model = Review
        fields = '__all__'
