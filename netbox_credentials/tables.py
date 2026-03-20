import django_tables2 as tables

from netbox.tables import NetBoxTable, columns

from .models import Credential, DeviceCredential


class CredentialTable(NetBoxTable):
    name = tables.Column(linkify=True)
    username = tables.Column()
    password_is_set = columns.BooleanColumn(
        verbose_name="Password",
        true_value="✔",
        false_value="—",
    )
    description = tables.Column()
    assignment_count = tables.Column(
        verbose_name="Devices",
        accessor="assignments__count",
        orderable=False,
    )
    tags = columns.TagColumn(url_name="plugins:netbox_credentials:credential_list")
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = Credential
        fields = (
            "pk",
            "id",
            "name",
            "username",
            "password_is_set",
            "description",
            "assignment_count",
            "tags",
            "actions",
        )
        default_columns = (
            "name",
            "username",
            "password_is_set",
            "description",
            "assignment_count",
        )


class DeviceCredentialTable(NetBoxTable):
    credential = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    role = tables.Column()
    tags = columns.TagColumn(
        url_name="plugins:netbox_credentials:devicecredential_list"
    )
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = DeviceCredential
        fields = (
            "pk",
            "id",
            "credential",
            "device",
            "role",
            "tags",
            "actions",
        )
        default_columns = ("credential", "device", "role")
