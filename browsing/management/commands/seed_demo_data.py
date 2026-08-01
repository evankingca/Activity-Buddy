from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from browsing.models import Activity, Preference, User, UserActivity


class Command(BaseCommand):
    help = "Create demo users and preference data"

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
        ]

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

            user_activity, _ = UserActivity.objects.get_or_create(
                user=user,
                activity=gym,
                defaults={"is_active": True},
            )

            Preference.objects.get_or_create(
                user_activity=user_activity,
                defaults=preference_data,
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"{user.username} already exists"))

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
