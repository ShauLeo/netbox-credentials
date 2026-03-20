from netbox.search import SearchIndex, register_search

from .models import Credential, DeviceCredential


@register_search
class CredentialIndex(SearchIndex):
    model = Credential
    fields = (
        ("name", 100),
        ("username", 80),
        ("description", 60),
        ("comments", 40),
    )


@register_search
class DeviceCredentialIndex(SearchIndex):
    model = DeviceCredential
    fields = (
        ("role", 80),
    )
