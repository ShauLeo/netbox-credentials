import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("dcim", "0001_initial"),
        ("extras", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Credential",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200,
                        unique=True,
                        help_text="Friendly name, e.g. 'default-pw' or 'snmp-ro-community'",
                    ),
                ),
                (
                    "username",
                    models.CharField(max_length=200, blank=True, default=""),
                ),
                (
                    "password",
                    models.TextField(
                        blank=True,
                        default="",
                        db_column="password",
                        verbose_name="Password (encrypted)",
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=500, blank=True, default=""),
                ),
                ("comments", models.TextField(blank=True, default="")),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem",
                        blank=True,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "verbose_name": "Credential",
                "verbose_name_plural": "Credentials",
            },
        ),
        migrations.CreateModel(
            name="DeviceCredential",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        max_length=100,
                        blank=True,
                        default="",
                        help_text="Optional role, e.g. 'management', 'snmp', 'api'",
                    ),
                ),
                (
                    "credential",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignments",
                        to="netbox_credentials.credential",
                    ),
                ),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="credential_assignments",
                        to="dcim.device",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem",
                        blank=True,
                    ),
                ),
            ],
            options={
                "ordering": ["credential__name"],
                "unique_together": {("credential", "device", "role")},
                "verbose_name": "Device Credential Assignment",
                "verbose_name_plural": "Device Credential Assignments",
            },
        ),
    ]
