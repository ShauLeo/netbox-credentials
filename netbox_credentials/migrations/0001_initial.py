import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("dcim", "0225_gfk_indexes"),
    ]

    operations = [
        migrations.CreateModel(
            name="Credential",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ("name", models.CharField(max_length=200, unique=True)),
                ("username", models.CharField(max_length=200, blank=True, default="")),
                ("password", models.TextField(blank=True, default="", db_column="password")),
                ("description", models.CharField(max_length=500, blank=True, default="")),
                ("comments", models.TextField(blank=True, default="")),
                ("tags", taggit.managers.TaggableManager(through="taggit.TaggedItem", to="taggit.Tag", blank=True)),
            ],
            options={"ordering": ["name"], "verbose_name": "Credential"},
        ),
        migrations.CreateModel(
            name="DeviceCredential",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ("role", models.CharField(max_length=100, blank=True, default="")),
                ("credential", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="assignments", to="netbox_credentials.credential")),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="credential_assignments", to="dcim.device")),
                ("tags", taggit.managers.TaggableManager(through="taggit.TaggedItem", to="taggit.Tag", blank=True)),
            ],
            options={"ordering": ["credential__name"], "unique_together": {("credential", "device", "role")}},
        ),
    ]
