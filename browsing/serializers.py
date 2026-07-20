from .models import User, Activity, UserActivity, Preference
from rest_framework import serializers
from django.contrib.auth import authenticate


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "display_name",
            "bio_text",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


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
    class Meta:
        model = User
        fields = ["id", "username", "display_name", "bio_text", "creation_date"]
        read_only_fields = ["id", "username", "creation_date"]


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ["id", "name", "description", "is_active"]
        read_only_fields = ["id"]


class UserActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = UserActivity
        fields = ["id", "activity", "is_active", "postal_codes"]


class UserActivityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ["id", "user", "activity", "is_active", "postal_codes"]
        read_only_fields = ["id"]


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
            "preferred_workout_time",
        ]


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

    class Meta:
        model = Preference
        fields = [
            "id",
            "user_activity",
            "experience",
            "goals",
            "training_styles",
            "gym_frequency",
            "preferred_workout_time",
        ]
        read_only_fields = ["id"]

    def validate_user_activity(self, user_activity):
        request = self.context.get("request")

        if request and user_activity.user != request.user:
            raise serializers.ValidationError(
                "You can only manage preferences for your own activities."
            )

        return user_activity

    def validate_goals(self, values):
        if values is None:
            raise serializers.ValidationError("At least one goal must be selected.")

        invalid = set(values) - self.valid_goals

        if invalid:
            raise serializers.ValidationError(f"Invalid goals: {', '.join(invalid)}")

        return values

    def validate_training_styles(self, values):
        if values is None:
            raise serializers.ValidationError(
                "At least one training style must be selected."
            )

        invalid = set(values) - self.valid_training_styles

        if invalid:
            raise serializers.ValidationError(
                f"Invalid training styles: {', '.join(invalid)}"
            )

        return values
