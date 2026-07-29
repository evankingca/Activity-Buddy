from .models import User, Activity, UserActivity, Preference, Connection, DirectMessage
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers

from .models import Activity, Preference, User, UserActivity

class PreferenceWriteSerializer(serializers.ModelSerializer):
    valid_goals = {
        "build_muscle",
        "weight_loss",
        "general_fitness",
        "strength_training",
        "powerlifting",
        "bodybuilding",
    }

    valid_training_styles = {choice[0] for choice in Preference.TrainingStyle.choices}

    valid_workout_times = {choice[0] for choice in Preference.WorkoutTime.choices}

    class Meta:
        model = Preference
        fields = [
            "id",
            "user_activity",
            "experience",
            "goals",
            "training_styles",
            "gym_frequency",
            "preferred_workout_times",
            "location_ids",
        ]
        read_only_fields = ["id", "user_activity"]

    def validate_goals(self, values):
        if not values:
            raise serializers.ValidationError("At least one goal must be selected.")

        invalid = set(values) - self.valid_goals

        if invalid:
            raise serializers.ValidationError(
                f"Invalid goals: {', '.join(sorted(invalid))}"
            )

        return values

    def validate_training_styles(self, values):
        if not values:
            raise serializers.ValidationError(
                "At least one training style must be selected."
            )

        invalid = set(values) - self.valid_training_styles

        if invalid:
            raise serializers.ValidationError(
                f"Invalid training styles: {', '.join(sorted(invalid))}"
            )

        return values

    def validate_preferred_workout_times(self, values):
        if not values:
            raise serializers.ValidationError(
                "At least one preferred workout time must be selected."
            )

        invalid = set(values) - self.valid_workout_times

        if invalid:
            raise serializers.ValidationError(
                f"Invalid workout times: {', '.join(sorted(invalid))}"
            )

        return values

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    preferences = PreferenceWriteSerializer(
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "display_name",
            "bio_text",
            "preferences",
        ]
        read_only_fields = ["id"]

    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value

    @transaction.atomic
    def create(self, validated_data):
        preference_data = validated_data.pop("preferences")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        gym = Activity.objects.get(name="Gym")

        user_activity = UserActivity.objects.create(
            user=user,
            activity=gym,
            is_active=True,
        )

        Preference.objects.create(
            user_activity=user_activity,
            **preference_data,
        )

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        attrs["user"] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    activities = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",        # now dynamic
            "display_name",
            "bio_text",
            "creation_date",
            "activities",
        ]

    def get_username(self, obj):
        request = self.context.get("request")

        # If no request context, default to hiding username
        if not request:
            return None

        # Only show username if the logged-in user is the same user
        if request.user == obj:
            return obj.username

        # Otherwise hide it
        return None

    def get_activities(self, obj):
        # Only include ID + name
        user_activities = UserActivity.objects.filter(user=obj, is_active=True)

        return [
            {
                "id": ua.activity.id,
                "name": ua.activity.name,
            }
            for ua in user_activities
        ]


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "id",
            "name",
            "description",
            "is_active",
        ]
        read_only_fields = ["id"]

class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    activity = ActivitySerializer(read_only=True)

    class Meta:
        model = UserActivity
        fields = [
            "id",
            "user",
            "activity",
            "is_active",
        ]

class UserActivityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = [
            "id",
            "user",
            "activity",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "user",
        ]

class PreferenceSerializer(serializers.ModelSerializer):
    user_activity = UserActivitySerializer(read_only=True)

    class Meta:
        model = Preference
        fields = [
            "id",
            "user_activity",
            "experience",
            "goals",
            "training_styles",
            "gym_frequency",
            "preferred_workout_times",
            "location_ids",
        ]

        read_only_fields = ["id", "user_activity"]

    def validate_goals(self, values):
        if not values:
            raise serializers.ValidationError("At least one goal must be selected.")

        invalid = set(values) - self.valid_goals

        if invalid:
            raise serializers.ValidationError(
                f"Invalid goals: {', '.join(sorted(invalid))}"
            )

        return values

    def validate_training_styles(self, values):
        if not values:
            raise serializers.ValidationError(
                "At least one training style must be selected."
            )

        invalid = set(values) - self.valid_training_styles

        if invalid:
            raise serializers.ValidationError(
                f"Invalid training styles: {', '.join(sorted(invalid))}"
            )

        return values

    def validate_preferred_workout_times(self, values):
        if not values:
            raise serializers.ValidationError(
                "At least one preferred workout time must be selected."
            )

        invalid = set(values) - self.valid_workout_times

        if invalid:
            raise serializers.ValidationError(
                f"Invalid workout times: {', '.join(sorted(invalid))}"
            )

        return values

class ConnectionSerializer(serializers.ModelSerializer):
    user_a = UserSerializer(read_only=True)
    user_b = UserSerializer(read_only=True)

    class Meta:
        model = Connection
        fields = [
            "id",
            "user_a",
            "user_b",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class ConnectionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ["user_a", "user_b", "status"]

class DirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ["id", "sender", "receiver", "connection", "text", "timestamp"]
        read_only_fields = ["id", "timestamp", "sender"]

class DirectMessageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ["receiver", "text"]

