from rest_framework import serializers

from courses.utils import get_user_from_context
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['student']

    def create(self, validated_data):
        validated_data['student'] = get_user_from_context(self.context)
        return super().create(validated_data)


class ReviewWithFullNameSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    def get_student(self, obj):
        return obj.student.first_name + " " + obj.student.last_name
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['student']
