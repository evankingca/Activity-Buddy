from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from browsing.models import (
    Activity,
    Connection,
    DirectMessage,
    Preference,
    User,
    UserActivity,
)


class Command(BaseCommand):
    help = "Create demo users, preferences, connections, and messages"

    def handle(self, *args, **options):
        gym, _ = Activity.objects.get_or_create(
            name="Gym",
            defaults={
                "description": "Find a compatible gym buddy.",
                "is_active": True,
            },
        )

        demo_users = [
            {
                "username": "user1",
                "email": "user1@example.com",
                "display_name": "User 1",
                "bio_text": "Looking for a consistent gym partner.",
                "preferences": {
                    "experience": "intermediate",
                    "goals": ["build_muscle", "strength_training"],
                    "training_styles": ["weightlifting", "bodybuilding"],
                    "gym_frequency": "3_4",
                    "preferred_workout_times": ["evening"],
                    "location_ids": [],
                },
            },
            {
                "username": "user2",
                "email": "user2@example.com",
                "display_name": "User 2",
                "bio_text": "Focused on general fitness and staying active.",
                "preferences": {
                    "experience": "beginner",
                    "goals": ["general_fitness", "weight_loss"],
                    "training_styles": ["cardio", "functional_fitness"],
                    "gym_frequency": "1_2",
                    "preferred_workout_times": ["morning", "afternoon"],
                    "location_ids": [],
                },
            },
            {
                "username": "user3",
                "email": "user3@example.com",
                "display_name": "User 3",
                "bio_text": "Interested in powerlifting and strength training.",
                "preferences": {
                    "experience": "advanced",
                    "goals": ["powerlifting", "strength_training"],
                    "training_styles": ["powerlifting", "weightlifting"],
                    "gym_frequency": "5_plus",
                    "preferred_workout_times": ["early_morning"],
                    "location_ids": [],
                },
            },
            {
                "username": "user4",
                "email": "user4@example.com",
                "display_name": "User 4",
                "bio_text": "Enjoys functional training and evening workouts.",
                "preferences": {
                    "experience": "intermediate",
                    "goals": ["general_fitness", "endurance"],
                    "training_styles": ["functional_fitness", "cardio"],
                    "gym_frequency": "3_4",
                    "preferred_workout_times": ["evening", "late_night"],
                    "location_ids": [],
                },
            },
            {
                "username": "user5",
                "email": "user5@example.com",
                "display_name": "User 5",
                "bio_text": "Looking for beginner-friendly workout partners.",
                "preferences": {
                    "experience": "beginner",
                    "goals": ["general_fitness", "build_muscle"],
                    "training_styles": ["weightlifting", "cardio"],
                    "gym_frequency": "1_2",
                    "preferred_workout_times": ["afternoon"],
                    "location_ids": [],
                },
            },
        ]

        users = {}

        for demo_user in demo_users:
            preference_data = demo_user["preferences"]

            user, created = User.objects.get_or_create(
                username=demo_user["username"],
                defaults={
                    "email": demo_user["email"],
                    "display_name": demo_user["display_name"],
                    "bio_text": demo_user["bio_text"],
                    "password": make_password("DemoPassword123!"),
                    "is_active": True,
                },
            )

            users[user.username] = user

            user_activity, _ = UserActivity.objects.get_or_create(
                user=user,
                activity=gym,
                defaults={
                    "is_active": True,
                },
            )

            Preference.objects.update_or_create(
                user_activity=user_activity,
                defaults=preference_data,
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"{user.username} already exists"))

        accepted_connection, _ = Connection.objects.update_or_create(
            user_a=users["user1"],
            user_b=users["user2"],
            defaults={
                "status": Connection.Status.ACCEPTED,
            },
        )

        Connection.objects.update_or_create(
            user_a=users["user1"],
            user_b=users["user3"],
            defaults={
                "status": Connection.Status.PENDING,
            },
        )

        DirectMessage.objects.get_or_create(
            sender=users["user1"],
            receiver=users["user2"],
            connection=accepted_connection,
            text="Hey, are you available to work out this week?",
        )

        DirectMessage.objects.get_or_create(
            sender=users["user2"],
            receiver=users["user1"],
            connection=accepted_connection,
            text="Yes, I am available Thursday evening.",
        )

        DirectMessage.objects.get_or_create(
            sender=users["user1"],
            receiver=users["user2"],
            connection=accepted_connection,
            text="Thursday evening works for me.",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo users, preferences, connections, and messages "
                "seeded successfully."
            )
        )
