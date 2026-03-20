from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

menu = PluginMenu(
    label="Credentials",
    groups=(
        (
            "Credentials",
            (
                PluginMenuItem(
                    link="plugins:netbox_credentials:credential_list",
                    link_text="Credentials",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_credentials:credential_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                        ),
                    ),
                ),
                PluginMenuItem(
                    link="plugins:netbox_credentials:devicecredential_list",
                    link_text="Assignments",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_credentials:devicecredential_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                        ),
                    ),
                ),
                PluginMenuItem(
                    link="plugins:netbox_credentials:bulk_assign",
                    link_text="Bulk Assign",
                ),
            ),
        ),
    ),
)
