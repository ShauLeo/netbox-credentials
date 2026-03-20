from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_credentials", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PluginSetting",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("panel_position", models.CharField(
                    choices=[
                        ("left_page", "Left column"),
                        ("right_page", "Right column"),
                        ("full_width_page", "Full width (bottom)"),
                    ],
                    default="left_page",
                    max_length=20,
                )),
            ],
            options={"verbose_name": "Plugin Setting"},
        ),
    ]
