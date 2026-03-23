from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_credentials", "0002_pluginsetting"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="credential",
            options={
                "ordering": ["name"],
                "verbose_name": "Credential",
                "verbose_name_plural": "Credentials",
            },
        ),
        migrations.AlterModelOptions(
            name="devicecredential",
            options={
                "ordering": ["credential__name"],
                "verbose_name": "Device Credential Assignment",
                "verbose_name_plural": "Device Credential Assignments",
            },
        ),
    ]
