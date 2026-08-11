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
                "username": "davis_7",
                "email": "davis_7@example.com",
                "display_name": "Inspector Davis",
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
                "username": "Millar_G",
                "email": "Millar_G@example.com",
                "display_name": "Gavin Millarrrrrrrrr",
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
                "display_name": "Luigi Vercotti",
                "bio_text": "Looking for beginner-friendly workout partners.",
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
                "display_name": "Sir Horace",
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
                "username": "nevilles1",
                "email": "nevilles1@example.com",
                "display_name": "Neville Shunt",
                "bio_text": "Interested in powerlifting and strength training.",
                "preferences": {
                    "experience": "beginner",
                    "goals": ["general_fitness", "build_muscle"],
                    "training_styles": ["weightlifting", "cardio"],
                    "gym_frequency": "1_2",
                    "preferred_workout_times": ["afternoon"],
                    "location_ids": [],
                },
            },
            {
                "username": "vince_sl_11",
                "email": "vince_sl_11@example.com",
                "display_name": "Vince Snetterton-Lewis",
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
                "username": "theoperation",
                "email": "theoperation@example.com",
                "display_name": "Doug Piranha",
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
            {
                "username": "Ernest_12",
                "email": "Ernest_12@example.com",
                "display_name": "Ernest Pythagoras",
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
                "username": "rono_9",
                "email": "rono_9@example.com",
                "display_name": "Ron Obvious",
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
                "username": "Dino",
                "email": "Dino@example.com",
                "display_name": "Dino Vercotti",
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
                "username": "john",
                "email": "john@example.com",
                "display_name": "John Partridge",
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
                "username": "dennis-m",
                "email": "dennis-m@example.com",
                "display_name": "Dennis Moore",
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
            user_a=users["davis_7"],
            user_b=users["Millar_G"],
            defaults={
                "status": Connection.Status.ACCEPTED,
            },
        )

        Connection.objects.update_or_create(
            user_a=users["davis_7"],
            user_b=users["user3"],
            defaults={
                "status": Connection.Status.PENDING,
            },
        )

        DirectMessage.objects.get_or_create(
            sender=users["davis_7"],
            receiver=users["Millar_G"],
            connection=accepted_connection,
            text="Hey, are you available to work out this week?",
        )

        DirectMessage.objects.get_or_create(
            sender=users["Millar_G"],
            receiver=users["davis_7"],
            connection=accepted_connection,
            text="Yes, I am available Thursday evening.",
        )

        DirectMessage.objects.get_or_create(
            sender=users["davis_7"],
            receiver=users["Millar_G"],
            connection=accepted_connection,
            text="Thursday evening works for me.",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo users, preferences, connections, and messages "
                "seeded successfully."
            )
        )
