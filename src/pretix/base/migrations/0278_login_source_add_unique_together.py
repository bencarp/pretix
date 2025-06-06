# Generated by Django 4.2.16 on 2025-02-28 13:25

from django.db import migrations, models


def remove_duplicates(apps, schema_editor):
    UserKnownLoginSource = apps.get_model("pretixbase", "UserKnownLoginSource")
    unique_fields = ["user", "agent_type", "device_type", "os_type", "country"]

    duplicates = (
        UserKnownLoginSource.objects
        .values(*unique_fields)
        .order_by()
        .annotate(latest_id=models.Max('id'), count=models.Count('id'))
        .filter(count__gt=1)
    )

    for duplicate in duplicates:
        (
            UserKnownLoginSource.objects
            .filter(**{x: duplicate[x] for x in unique_fields})
            .exclude(id=duplicate["latest_id"])
            .delete()
        )


class Migration(migrations.Migration):

    dependencies = [
        ("pretixbase", "0277_customerssoclient_require_pkce_and_more"),
    ]

    operations = [
        migrations.RunPython(remove_duplicates, migrations.RunPython.noop),
        migrations.AlterUniqueTogether(
            name="userknownloginsource",
            unique_together={
                ("user", "agent_type", "device_type", "os_type", "country")
            },
        ),
    ]
