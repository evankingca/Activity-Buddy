from django.db import migrations


def create_gym_activity(apps, schema_editor):
    Activity = apps.get_model("browsing", "Activity")

    Activity.objects.get_or_create(
        name="Gym",
        defaults={
            "description": "Gym and fitness training",
            "is_active": True,
        },
    )


def remove_gym_activity(apps, schema_editor):
    Activity = apps.get_model("browsing", "Activity")
    Activity.objects.filter(name="Gym").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("browsing", "0003_remove_preference_preferred_workout_time_and_more"),
    ]

    operations = [
        migrations.RunPython(
            create_gym_activity,
            remove_gym_activity,
        ),
    ]
