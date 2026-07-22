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
    user = UserSerializer(read_only=True)
    activity = ActivitySerializer()

    class Meta:
        model = UserActivity
        fields = ["id", "user", "activity", "is_active"]


class UserActivityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = [
            "id",
            "user",
            "activity",
            "is_active",
        ]
        read_only_fields = ["id", "user"]


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
