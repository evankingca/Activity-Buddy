from .models import User, Activity, UserActivity
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'display_name', 'bio_text', 'creation_date']
        read_only_fields = ['id', 'username', 'creation_date']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'description', 'is_active']
        read_only_fields = ['id']

class UserActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = UserActivity
        fields = ['id', 'activity', 'is_active', 'postal_codes']


class UserActivityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'activity', 'is_active', 'postal_codes']
        read_only_fields = ['id']


