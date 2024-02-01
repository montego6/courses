from rest_framework import serializers
from users.helpers import get_user_full_name

from courses.utils import get_user_from_context
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['course', 'student', 'comment', 'rating']
        read_only_fields = ['student']
        extra_kwargs = {
            'course': {
                'write_only': True,
            }
        }

    def create(self, validated_data):
        validated_data['student'] = get_user_from_context(self.context)
        return super().create(validated_data)


class ReviewWithFullNameSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    def get_student(self, obj):
        return get_user_full_name(obj.student)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['student']
