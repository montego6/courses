from rest_framework import serializers
from .models import TeacherProfile


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['avatar', 'bio']
        read_only_fields = ['balance']
    
    def create(self, validated_data):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        validated_data['user'] = user
        return super().create(validated_data)
