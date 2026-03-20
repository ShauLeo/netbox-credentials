from netbox.plugins import PluginConfig


class NetBoxCredentialsConfig(PluginConfig):
    name = "netbox_credentials"
    verbose_name = "Credentials"
    description = "Manage reusable credentials and assign them to devices"
    version = "0.1.0"
    author = "Your Name"
    author_email = "you@example.com"
    base_url = "credentials"
    min_version = "4.0.0"
    default_settings = {}


config = NetBoxCredentialsConfig
